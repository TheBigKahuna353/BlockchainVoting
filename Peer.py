


class Peer:
    def __init__(self, id, ip, port):
        self.id = id
        self.ip = ip
        self.port = port

    def __str__(self):
        return f"Peer {self.id} at {self.ip}:{self.port}"

    def send_block(self, block):
        # Implement your code here
        return True