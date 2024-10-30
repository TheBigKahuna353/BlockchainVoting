import time
from core.Block import Block

"""
Blockchain class
this holds just the chain (eg list of Blocks from Block.py)
this class will have methods to add blocks to the chain, validate the chain, etc
this class does not handle mining, that is the job of the miner
"""
class Blockchain:

    POF_DIFFICULTY = 4

    def __init__(self):
        self.chain = []
        
    
    def create_genesis_block(self):
        """
        A function to generate the genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def add_block(self, block):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * 1. Checking if the previous_hash refers to the hash of the latest block in the chain
        * 2. Recalculate and validate block hash
        * 3. Verify transactions: Ensure all are legitimate (e.g., unique voter IDs, correct format
        """
        previous_hash = self.chain[-1].hash 
        if previous_hash != block.previous_hash: #* 1
            print("Invalid previous hash.")
            return False
        if not self.is_valid_hash(block): #* 2
            return False
        if not block.verify_data(self.chain): #* 3
            print("Invalid data.")
            return False
        self.chain.append(block)
        return True

    def is_valid_hash(self, block):
        """
        A function to check if the hash of the block is valid.
        Recalculates the hash of the block and compares it with the
        hash in the block.
        """
        # Optional proof-of-work check: ensure hash has required leading zeros
        if not block.hash.startswith("0" * self.POF_DIFFICULTY):
            print("Proof-of-work check failed.")
            return False
        
        # Recalculate hash and compare
        if block.hash != block.hash_block():
            print("Invalid hash.")
            return False
        
        return True

    def __len__(self):
        return len(self.chain)