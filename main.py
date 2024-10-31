from hooman import Hooman
import pygame
from core.p2p.P2P import P2P
from core.Node import Miner
from core.Block import from_dict
import sys

PORT = 5008

app = Hooman(800, 600)

# Loading Screen for the P2P Network
app.background(255)
app.fill(0)
app.font_size(20)
app.text("P2P Network", 300, 10, )
app.text("Port: " + str(PORT), 300, 50)
app.text("Loading...", 300, 200)
app.flip_display()
app.event_loop()

# Start the P2P Network

miner = Miner()
# This will start the server on the specified port, as well as connect to the seed node
p2p = P2P(PORT, miner)
miner.p2p = p2p

starting_block_dict = {
    'index': 0, 
    'timestamp': 1730291248.4442232, 
    'data': {"voter_hash": "0", "vote": "A"}, 
    'previous_hash': '0', 
    'nonce': 0, 
    'hash': '3c379288510f21b3f4fe2a6f39bc44013391744fbe4fbcd8cc3d89133208b668'}

starting_block = from_dict(starting_block_dict)
miner.blockchain.set_genesis_block(starting_block)

if not p2p.server_connected:
    print("Failed to connect to the seed node.")
    sys.exit(1)

print(p2p)

button = app.button(600, 350, 150, 50, "Mine Block", {
    "font_size": 18, 
    "background_color": (200, 200, 200), 
    "hover_background_color": (150, 150, 150),
    "curve": 0.5,
    "enlarge": True})

while app.is_running:

    app.background(255)

    app.fill(0)
    app.font_size(20)
    app.text("P2P Network", 300, 10)
    app.text("Port: " + str(PORT), 300, 50)

    app.fill(200)
    app.rect(0, 80, 250, 600)
    app.fill(0)
    app.text("Connected Nodes", 50, 100)
    for i, node in enumerate(p2p.peer_nodes + ['sdfsf', 'sdfsdf']):
        app.text(node, 50, 150 + i * 30)

    app.text("Miner", 650, 100)
    length = len(miner.blockchain)
    app.text(f"Blockchain len: {length}", 600, 150)

    if button.update():
        voter_hash = int(miner.blockchain.chain[-1].data['voter_hash']) + 1
        print(voter_hash)
        miner.add_transaction({"type": "vote", "voter_hash": str(voter_hash), "vote": "A"})
        print(miner.mine())
        print(sys.getsizeof(miner.blockchain.chain))

    app.flip_display()
    app.event_loop()

p2p.stop_server()