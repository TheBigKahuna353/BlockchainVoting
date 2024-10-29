"""
Node class for blockchain network
each node has a blockchain, transaction pool and a list of peers
Miner class will inherit from this class
"""
from Blockchain import Blockchain
from Block import VoteBlock, RegisterBlock
import time

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
        transaction = self.transaction_pool.pop(0)
        previous_hash = self.blockchain.chain[-1].hash
        if transaction["type"] == "vote":
            block = VoteBlock(len(self.blockchain), time.time(), transaction, previous_hash)
        elif transaction.type == "register":
            block = RegisterBlock(len(self.blockchain), time.time(), transaction, previous_hash)
        else:
            return False
        
        # Proof-of-work
        while not block.hash.startswith("0" * self.blockchain.POF_DIFFICULTY):
            block.nonce += 1
            block.hash = block.hash_block()
        
        if self.add_block(block):
            # Broadcast block to peers
            for peer in self.peers:
                peer.send_block(block)
            return True
        return False
