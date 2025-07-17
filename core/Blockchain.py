import time
from core.Block import Block
from core.Block import VoteBlock, RegisterBlock, to_dict, from_dict

"""
Blockchain class
this holds just the chain (eg list of Blocks from Block.py)
this class will have methods to add blocks to the chain, validate the chain, etc
this class does not handle mining, that is the job of the miner
NEW: this class will also hold a hashmap of users ids to public keys
"""
class Blockchain:

    POF_DIFFICULTY = 4

    def __init__(self):
        self.chain = []
        self.users = {}
        
    
    def create_genesis_block(self):
        """
        A function to generate the genesis block and appends it to
        the chain. The block has index 0, previousHash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def set_genesis_block(self, block):
        """
        A function to set the genesis block.
        """
        if block.index != 0 or block.previousHash != "0":
            print("Invalid genesis block.")
            return False
        if len(self.chain) == 0:
            self.chain.append(block)
            return True
        elif len(self.chain) == 1:
            self.chain[0] = block
            return True
        else:
            if self.chain[1].previousHash == block.hash:
                self.chain[0] = block
                return True
            else:
                print("Invalid genesis block. Previous hash does not match.")
                return False

    def add_block(self, block):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * 1. Checking if the previousHash refers to the hash of the latest block in the chain
        * 2. Recalculate and validate block hash
        * 3. Verify transactions: Ensure all are legitimate (e.g., unique voter IDs, correct format
        """
        previousHash = self.chain[-1].hash 
        if previousHash != block.previousHash: #* 1
            print("Invalid previous hash.")
            return False
        if not self.is_valid_hash(block): #* 2
            return False
        if not block.verify_data(self.chain, self.users): #* 3
            print("Invalid data.")
            return False
        self.chain.append(block)
        self.update_users_from_last_block()
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
    
    def to_dict(self):
        return [to_dict(block) for block in self.chain]
    
    def from_dict(self, chain):
        self.chain = [from_dict(block) for block in chain]
        self.update_users()

    def update_users(self):
        for block in self.chain:
            if isinstance(block, RegisterBlock):
                self.users[block.data['voter_id']] = block.data['public_key']
    
    def update_users_from_last_block(self):
        block = self.chain[-1]
        if isinstance(block, RegisterBlock):
            self.users[block.data['voter_id']] = block.data['public_key']