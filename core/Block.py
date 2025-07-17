import hashlib as hasher
from core.utils.encryption import verify_signature
import json

class Block:
    def __init__(self, index, timestamp, data, previousHash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previousHash = previousHash
        self.nonce = 0
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        data = json.dumps(self.data, sort_keys=True, separators=(',', ':')) # Convert data to JSON string
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(data).encode('utf-8') +
                   str(self.previousHash).encode('utf-8') +
                   str(self.nonce).encode('utf-8')) # Add nonce
        return sha.hexdigest()
    
    def verify_data(self, previous_blocks):
        """
        A function to verify the data in the block.
        This function will be called by the add_block method in the Blockchain class.
        This function should be overridden by the child class.
        """
        return False


class VoteBlock(Block):

    """
    data: {
        "voter_id": str
        "vote": str
        "signature": str
    }
    """

    def __init__(self, index, timestamp, data, previousHash):
        super().__init__(index, timestamp, data, previousHash)

    def verify_data(self, previous_blocks, users):
        """
        Verify that the data in the block is valid.
        Checking that each voter_id is unique across previous blocks to prevent duplicate voting.
        Check that the voter_id is registered before voting.
        Ensuring each transaction has valid formatting (contains required fields like voter_id and vote).
        """
        registered = False
        public_key = None
        # Check for duplicate voter IDs
        for block in previous_blocks:
            if block.index == 0: continue   # Skip the genesis block
            if isinstance(block, VoteBlock):
                print(self.data, block.data)
                if self.data['voter_id'] in block.data['voter_id']:
                    print("Duplicate voter ID.")
                    return False
            else:
                if self.data['voter_id'] in block.data['voter_id']:
                    registered = True
                    public_key = block.data['public_key']
        # Check if voter ID is registered
        if not registered:
            print("Voter ID not registered.")
            return False
        # Check for required fields
        if 'voter_id' not in self.data or 'vote' not in self.data:
            print("Missing required fields.")
            return False
        # Check for valid signature
        if not verify_signature(public_key, self.data['signature'], self.data['voter_id'] + self.data['vote']):
            print("Invalid signature.")
            return False
        return True

class RegisterBlock(Block):

    """
    data: {
        "voter_id": str
        "public_key": str
    }
    """

    def __init__(self, index, timestamp, data, previousHash):
        super().__init__(index, timestamp, data, previousHash)

    def verify_data(self, previous_blocks, users):
        """
        Verify that the data in the block is valid.
        Checking that each voter_id is unique across previous blocks to prevent duplicate voting.
        Ensuring each transaction has valid formatting (contains required fields like voter_id and public key).
        """
        # Check for duplicate voter IDs
        if self.data['voter_id'] in users:
            print("Duplicate voter ID.")
            return False
        # Check for required fields
        if 'voter_id' not in self.data:
            return False
        if 'public_key' not in self.data:
            return False
        return True

def to_dict(block):
    return {
        "index": block.index,
        "timestamp": block.timestamp,
        "data": block.data,
        "previousHash": block.previousHash,
        "nonce": block.nonce,
        "hash": block.hash,
        "type": "vote" if isinstance(block, VoteBlock) else "register"
    }

def from_dict(block_dict):
    print(f"Creating block from dict: {block_dict}")
    if block_dict["type"] == "vote":
        block = VoteBlock(block_dict["index"], block_dict["timestamp"], block_dict["data"], block_dict["previousHash"])
    elif block_dict["type"] == "register":
        block = RegisterBlock(block_dict["index"], block_dict["timestamp"], block_dict["data"], block_dict["previousHash"])
    else:
        block = Block(block_dict["index"], block_dict["timestamp"], block_dict["data"], block_dict["previousHash"])
    block.nonce = block_dict["nonce"]
    block.hash = block_dict["hash"]
    return block