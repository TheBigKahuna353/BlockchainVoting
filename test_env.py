from Block import Block
from Blockchain import Blockchain
import time

def test_block():
    block = Block(0, time.time(), "Genesis Block", "0")
    assert block.index == 0
    assert block.timestamp is not None
    assert block.data == "Genesis Block"
    assert block.previous_hash == "0"
    assert block.hash is not None
    assert block.nonce == 0
    assert block.hash_block() == block.hash

def test_blockchain():
    blockchain = Blockchain()
    blockchain.create_genesis_block()
    assert len(blockchain.chain) == 1
    assert blockchain.chain[0].index == 0
    assert blockchain.chain[0].data == "Genesis Block"
    assert blockchain.chain[0].previous_hash == "0"
    assert blockchain.chain[0].hash is not None
    assert blockchain.chain[0].nonce == 0
    assert blockchain.chain[0].hash_block() == blockchain.chain[0].hash
    block = Block(1, time.time(), "Block 1", blockchain.chain[-1].hash)
    assert blockchain.add_block(block) == True
    assert len(blockchain.chain) == 2
    assert blockchain.chain[-1].index == 1
    assert blockchain.chain[-1].data == "Block 1"
    assert blockchain.chain[-1].previous_hash == blockchain.chain[-2].hash
    assert blockchain.chain[-1].hash is not None
    assert blockchain.chain[-1].nonce == 0
    assert blockchain.chain[-1].hash_block() == blockchain.chain[-1].hash
    block = Block(2, time.time(), "Block 2", "0")
    assert blockchain.add_block(block) == False
    assert len(blockchain.chain) == 2
    block = Block(2, time.time(), "Block 2", blockchain.chain[-1].hash)
    assert blockchain.add_block(block) == True
    assert len(blockchain.chain) == 3
    assert blockchain.chain[-1].index == 2
    assert blockchain.chain[-1].data == "Block 2"
    assert blockchain.chain[-1].previous_hash == blockchain.chain[-2].hash
    assert blockchain.chain[-1].hash is not None
    assert blockchain.chain[-1].nonce == 0
    assert blockchain.chain[-1].hash_block() == blockchain.chain[-1].hash


def run_tests():
    test_block()
    test_blockchain()
    print("All tests pass.")

if __name__ == "__main__":
    run_tests()
