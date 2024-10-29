import hashlib as hasher

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8') +
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
    def __init__(self, index, timestamp, data, previous_hash):
        super().__init__(index, timestamp, data, previous_hash)

    def verify_data(self, previous_blocks):
        """
        Verify that the data in the block is valid.
        Checking that each voter_hash is unique across previous blocks to prevent duplicate voting.
        Ensuring each transaction has valid formatting (contains required fields like voter_hash and vote).
        """
        # Check for duplicate voter IDs
        for block in previous_blocks:
            if not isinstance(block, VoteBlock): continue
            if self.data['voter_hash'] in block.data['voter_hash']:
                return False
        # Check for required fields
        if 'voter_hash' not in self.data or 'vote' not in self.data:
            return False
        return True

class RegisterBlock(Block):
    def __init__(self, index, timestamp, data, previous_hash):
        super().__init__(index, timestamp, data, previous_hash)

    def verify_data(self, previous_blocks):
        """
        Verify that the data in the block is valid.
        Checking that each voter_hash is unique across previous blocks to prevent duplicate voting.
        Ensuring each transaction has valid formatting (contains required fields like voter_hash and vote).
        """
        # Check for duplicate voter IDs
        for block in previous_blocks:
            if not isinstance(block, RegisterBlock): continue
            if self.data['voter_hash'] in block.data['voter_hash']:
                return False
        # Check for required fields
        if 'voter_hash' not in self.data:
            return False
        return True