"""
Node class for blockchain network
each node has a blockchain, transaction pool and a list of peers
Miner class will inherit from this class
"""
from core.Blockchain import Blockchain
from core.Block import VoteBlock, RegisterBlock, to_dict, from_dict
import time, random

class Node:

    def __init__(self, p2p):
        self.blockchain = Blockchain()
        self.transaction_pool = []
        self.p2p = p2p
    
    def add_peer(self, peer):
        self.peers.append(peer)
    
    def peer_left(self, peer):
        self.peers.remove(peer)
    
    def add_transaction(self, transaction):
        self.transaction_pool.append(transaction)
    
    def add_block(self, block):
        if isinstance(block, dict):
            block = from_dict(block)
        if self.blockchain.add_block(block):
            # TODO remove transactions from pool that are in the block
            print(f"Block {block.index} added to the chain.")
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

    def get_random_voter_id(self):
        """
        A function to get a random voter ID.
        This function will be called by the miner to get a random voter ID.
        """
        id = random.randint(100_000, 999_999)
        while str(id) in self.blockchain.users:
            id = random.randint(100_000, 999_999)
        return str(id)


class Miner(Node):

    def __init__(self, p2p=None):
        super().__init__(p2p)
    
    def mine(self):
        """
        A function to mine a new block.
        This function will be called by the miner to mine a new block.
        """
        transaction = self.transaction_pool.pop(0)
        previousHash = self.blockchain.chain[-1].hash
        if transaction["type"] == "vote":
            block = VoteBlock(len(self.blockchain), time.time(), transaction, previousHash)
        elif transaction["type"] == "register":
            block = RegisterBlock(len(self.blockchain), time.time(), transaction, previousHash)
        else:
            return False
        
        # Proof-of-work
        while not block.hash.startswith("0" * self.blockchain.POF_DIFFICULTY):
            block.nonce += 1
            block.hash = block.hash_block()
        
        if self.add_block(block):
            # Broadcast block to peers
            if self.p2p:
                print(f"Broadcasting block {block.index} to peers.")
                if not self.p2p.broadcast_block(to_dict(block)):
                    # If broadcast fails, remove block from chain
                    self.blockchain.chain.pop()
                    return False
            return True
        return False
