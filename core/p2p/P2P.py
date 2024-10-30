import time
import socketio
import threading
from gevent import pywsgi
from socketio.exceptions import ConnectionError

class P2P:

    seed_node = 5000 # for development purposes, it is only the port number

    def __init__(self, port, node=None):
        """
        On initialization, the P2P class will start a server on the specified port.
        It will also connect to the seed node and share its port number with the seed node.
        The seed node will then share its list of peers with this Node.
        this will only return when the server has started and connected to the seed node.
        unless the server is the seed node, in which case it will return immediately.
        """
        self.server = socketio.Server(async_mode='gevent')
        self.client = socketio.Client()
        self.app = socketio.WSGIApp(self.server)
        self._server = None
        self.node = node

        self.port = port
        self.peer_nodes = []
        self.client_connected = False
        self.server_connected = False
        self.response = None
        self.connecting = True

        self.error = False

        # On Seperate Thread ---------------------------------------------
        # Set up server events
        @self.server.event
        def connect(sid, environ):
            print(f'SERVER: {self.port}: Node connected: {sid}')
        
        @self.server.event
        def receive_block(sid, block_data):
            print(f'SERVER: {self.port}: Received new block: {block_data}')
            # Logic to validate and add block to chain goes here
            if self.node:
                return self.node.add_block(block_data)
            return True
        
        @self.server.event
        def connect_to_network(sid, port):
            print(f'SERVER: {self.port}: Node connected to network: {port}')
            self.share_peers(port)
            self.peer_nodes.append(port)
            return self.peer_nodes[:-1]
        
        @self.server.event
        def share_peers(sid, peers):
            print(f'SERVER: {self.port}: Received new peers: {peers}')
            if isinstance(peers, list):
                self.peer_nodes.extend(peers)
            else:
                self.peer_nodes.append(peers)
        
        # ----------------------------------------------------------------

        # Start the server on a separate thread
        thread = threading.Thread(target=self.start_server)
        thread.start()

        if port != self.seed_node:
            self.peer_nodes.append(self.seed_node)
            print("Connecting to seed node")
            while not self.server_connected: pass
            print(f"Connecting to seed node: {self.seed_node}")
            connected = self.connect_to_network()
            if not connected:
                print(f"Failed to connect to network")
                self.stop_server()
                self.error = True
                return
        else:
            # wait for the server to start
            while not self.server_connected: pass
        
    
    def stop_server(self):
        # Stop the server
        if self._server:
            self._server.stop()
        self.server_connected = False
        print(f"Server stopped on port {self.port}")
    
    # On Seperate Thread ---------------------------------------------
    def start_server(self):
        # Start the server to listen for incoming connections
        try:
            self._server = pywsgi.WSGIServer(('', self.port), self.app)
            print(f"Server started on port {self.port}")
            self.server_connected = True
            self._server.serve_forever()
        except Exception as e:
            print(f"Failed to start server on port {self.port}: {e}")
            self.stop_server()
    # ----------------------------------------------------------------
    
    def broadcast_block(self, block_data):
        # Connect to each peer and send the block data
        for node_address in self.peer_nodes:
            passed = self.send_to(node_address, 'receive_block', block_data)
            if passed != "Accepted":
                print(f"Failed to send block to {node_address}: {passed}")
                return False
                
    
    def __str__(self):
        return f"Port: {self.port}, Server Connected: {self.server_connected}"

    def callback(self, *args):
        self.response = args[0]
        self.client_connected = False 

    def connecting_callback(self, peers):
        print(f"Connected to network: {peers}")
        self.peer_nodes.extend(peers)
        self.client_connected = False

    def connect_to_network(self):
        # Connect to the seed node
        print(f"Connecting to seed node: {self.seed_node}")
        try:
            self.client_connected = True
            self.client.connect(f'http://localhost:{self.seed_node}')
            self.client.emit('connect_to_network', self.port, callback=self.connecting_callback)
            while self.client_connected: pass
            return True
        except ConnectionError as e:
            print(f"Failed to connect to seed node")
            self.client_connected = False
            self.client.disconnect()
            return False
    
    def share_peers(self, new_peer):
        # Share new peers with the network
        for node_address in self.peer_nodes:
            self.send_to(node_address, 'share_peers', new_peer)

    def send_to(self, node_address, event, data):
        # Send data to a specific node
        while self.client_connected: pass
        try:
            self.client_connected = True
            self.client.connect(f'http://localhost:{node_address}')
            self.client.emit(event, data, callback=self.callback)
            while self.client_connected: pass
            self.client.disconnect()
            return self.response if self.response else "Accepted"
        except ConnectionError as e:
            print(f"Failed to connect to {node_address}")
            self.client_connected = False
            self.client.disconnect()
            return "Could Not Connect"
        except Exception as e:
            print(f"Failed to send data to {node_address}: {e}")
            self.client_connected = False
            self.client.disconnect()
            return "Failed"
        

if __name__ == "__main__":
    p2p = P2P(5000)
    while True:
        if p2p.server_connected:
            break