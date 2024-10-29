"""
Node class for blockchain network
each node has a blockchain, transaction pool and a list of peers
Miner class will inherit from this class
"""
from Blockchain import Blockchain
from Block import Block

class Node:

    def __init__(self):
        self.blockchain = Blockchain()
        self.transaction_pool = []
        self.peers = []
    
    def add_peer(self, peer):
        self.peers.append(peer)
    
    def peer_left(self, peer):
        self.peers.remove(peer)
    
    def add_transaction(self, transaction):
        self.transaction_pool.append(transaction)
    
    def add_block(self, block):
        if self.blockchain.add_block(block):
            # TODO remove transactions from pool that are in the block
            return True
        return False
    
    def validate_chain(self):
        """
        A function to validate the chain.
        This function will be called by the miner to validate the chain
        before mining a new block.
        """
        # Implement your code here
        return True
    
    def sync_chain(self):
        """
        A function to sync the chain with peers.
        This function will be called by the miner to sync the chain
        with the peers before mining a new block.
        """
        # Implement your code here
        return True



class Miner(Node):

    def __init__(self):
        super().__init__()
    
    def mine(self):
        """
        A function to mine a new block.
        This function will be called by the miner to mine a new block.
        """
        # Implement your code here
        return True