from Block import Block
from Blockchain import Blockchain
from Node import Miner, Node
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

def test_mine_block():
    miner = Miner()
    miner.blockchain.create_genesis_block()
    transaction = {
        "type": "vote",
        "voter_hash": "hash",
        "vote": "candidate"
    }
    miner.add_transaction(transaction)
    assert miner.mine() == True


def test_validating_incoming_block():
    miner = Miner()
    miner.blockchain.create_genesis_block()
    peer = Node()
    peer.blockchain.chain = miner.blockchain.chain.copy()
    transaction = {
        "type": "vote",
        "voter_hash": "hash",
        "vote": "candidate"
    }
    miner.add_transaction(transaction)
    assert miner.mine() == True

    assert peer.add_block(miner.blockchain.chain[-1]) == True


def run_tests():
    test_block()
    test_blockchain()
    test_mine_block()
    test_validating_incoming_block()
    print("All tests pass.")

if __name__ == "__main__":
    run_tests()
