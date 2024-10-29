import socketio
import threading
from gevent import pywsgi
import time

class P2P:

    seed_node = 5000 # for development purposes, it is only the port number

    def __init__(self, port):
        self.server = socketio.Server(async_mode='gevent')
        self.client = socketio.Client()
        self.app = socketio.WSGIApp(self.server)
        self._server = None

        self.port = port
        self.peer_nodes = []
        self.client_connected = False

        # Set up server events
        @self.server.event
        def connect(sid, environ):
            print(f'SERVER: {self.port}: Node connected: {sid}')
        
        @self.server.event
        def receive_block(sid, block_data):
            print(f'SERVER: {self.port}: Received new block: {block_data}')
            # Logic to validate and add block to chain goes here
        
        @self.server.event
        def connect_to_network(sid, port):
            print(f'SERVER: {self.port}: Node connected to network: {port}')
            self.peer_nodes.append(port)
            
        # Run server in a background thread
        threading.Thread(target=self.start_server).start()

        if port != self.seed_node:
            self.peer_nodes.append(self.seed_node)
            try:
                self.connect_to_network()
            except Exception as e:
                print(f"Failed to connect to seed node", self.seed_node)
                self.stop_server()
            
    def stop_server(self):
        # Stop the server
        self._server.stop()
    
    def start_server(self):
        # Start the server to listen for incoming connections
        self._server = pywsgi.WSGIServer(('', self.port), self.app)
        self._server.serve_forever()
    
    def broadcast_block(self, block_data):
        # Connect to each peer and send the block data
        for node_address in self.peer_nodes:
            while self.client_connected: pass # wait for client to disconnect
            try:
                self.client.connect(f'http://localhost:{node_address}') # for development purposes, it is localhost
                self.client.emit('receive_block', block_data, callback=self.callback)
                print(f'Broadcasted block to {node_address}')
            except Exception as e:
                print(f"Failed to connect to {node_address}: {e}")
    
    def callback(self, *args):
        self.client.disconnect()   
        self.client_connected = False 

    def connect_to_network(self):
        # Connect to a node in the network
        while self.client_connected: pass # wait for client to disconnect
        self.client.connect(f'http://localhost:{self.seed_node}') # for development purposes, it is localhost
        self.client_connected = True
        print(f'Connecting to network through seed node: {self.seed_node}')
        self.client.emit('connect_to_network', self.port, callback=self.callback)

