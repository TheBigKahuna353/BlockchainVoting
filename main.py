from hooman import Hooman
import pygame
from core.p2p.P2P import P2P
from core.Node import Miner
from core.Block import from_dict
from core.utils.encryption import generate_key_pair, sign_data, key_to_mnemonic, mnemonic_to_private_key
import sys
import pyperclip
from core.VotingSystem import VotingSystem

PORT = 5002

# check for sys arguments
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print("Invalid port number. Using default port 5001.")

app = Hooman(800, 600)

# Loading Screen for the P2P Network
app.background(255)
app.fill(0)
app.font_size(20)
app.text("P2P Network", 300, 10)
app.text("Port: " + str(PORT), 300, 50)
app.text("Loading...", 300, 200)
app.flip_display()
app.event_loop()

# Start the P2P Network

miner = Miner()
# This will start the server on the specified port, as well as connect to the seed node
p2p = P2P(PORT, miner)
miner.p2p = p2p
vs = VotingSystem()

# user variables
private_key, public_key = None, None
voter_id = 0
mnemonic = None
def create_transaction(voter_id, vote):
    data = {
        "voter_id": voter_id,
        "vote": vote,
        "type": "vote"
    }
    signature = sign_data(private_key, (str(voter_id) + vote))
    data["signature"] = signature
    return data

def create_register_transaction(voter_id, public_key):
    data = {
        "voter_id": voter_id,
        "public_key": public_key,
        "type": "register"
    }
    return data

starting_block_dict = {
    'index': 0, 
    'timestamp': 1730291248.4442232, 
    'data': {"voter_id": "0", "vote": "A"}, 
    'previous_hash': '0', 
    'nonce': 0, 
    'hash': '3c379288510f21b3f4fe2a6f39bc44013391744fbe4fbcd8cc3d89133208b668'}

starting_block = from_dict(starting_block_dict)
miner.blockchain.set_genesis_block(starting_block)

if not p2p.server_connected:
    print("Failed to connect to the seed node.")
    sys.exit(1)

btn_style = {
    "font_size": 18, 
    "background_color": (200, 200, 200), 
    "hover_background_color": (150, 150, 150),
    "curve": 0.5,
    "enlarge": True
}

txt_box_style = {
    "font_size": 18, 
    "background_color": (200, 200, 200), 
    "curve": 0.2, 
    "max_lines": 4,
    "typing": False
}

txt_box_style2 = txt_box_style.copy()
txt_box_style2["max_lines"] = 5

button = app.button(600, 350, 150, 50, "Mine Block", btn_style)

button2 = app.button(600, 450, 150, 50, "Register", btn_style)

button3 = app.button(600, 550, 150, 50, "Show votes", btn_style)

txtBox = app.text_box(100, 250, 600, 0, txt_box_style)

txtBox2 = app.text_box(100, 350, 600, 0, txt_box_style2)

txtBox3 = app.text_box(100, 500, 600, 0, txt_box_style)

copy_btn = app.button(600, 550, 50, 50, "Copy", btn_style)

back_btn = app.button(700, 50, 50, 50, "Back", btn_style)

def main_menu():
    global state, voter_id, private_key, public_key, mnemonic
    app.fill(0)
    app.font_size(20)
    app.text("P2P Network", 300, 10)
    app.text("Port: " + str(PORT), 300, 50)

    app.fill(200)
    app.rect(0, 80, 250, 600)
    app.fill(0)
    app.text("Connected Nodes", 50, 100)
    for i, node in enumerate(p2p.peer_nodes):
        app.text(node, 50, 150 + i * 30)

    app.text("Miner", 650, 100)
    length = len(miner.blockchain)
    app.text(f"Blockchain len: {length}", 600, 150)

    if voter_id != 0 and button.update():
        print(voter_id)
        miner.add_transaction(create_transaction(str(voter_id), "A"))
        print(miner.mine())
        print(sys.getsizeof(miner.blockchain.chain))
        print(miner.blockchain.to_dict())

    if button2.update():
        state = "register"
        private_key, public_key = generate_key_pair()
        voter_id = miner.get_random_voter_id()
        mnemonic = key_to_mnemonic(private_key)
        print(public_key.decode())
        txtBox.set_text(str(public_key.decode()))
        txtBox2.set_text(str(private_key.decode()))
        txtBox3.set_text(str(mnemonic))
        miner.add_transaction(create_register_transaction(str(voter_id), public_key))
        miner.mine()
    
    if button3.update():
        state = "show_votes"
        print("Showing votes...")
        vs.calulate_votes(miner.blockchain.chain)


def register():
    global state
    """
    A function to register the voter.
    Register block needs
    """
    app.fill(0)
    app.font_size(20)
    app.text("Register Voter", 300, 10)
    app.text("Your Voter Id:", 100, 100)
    app.text(str(voter_id), 100, 150)

    app.text("Public Key:", 100, 200)
    txtBox.update()

    app.text("Private Key:", 100, 320)
    txtBox2.update()

    app.text("Mnemonic:", 100, 450)
    txtBox3.update()

    if copy_btn.update():
        pyperclip.copy(txtBox3.get_lines(return_as_string=True))
        print("Mnemonic copied to clipboard.")

    if back_btn.update():
        state = "main_menu"
        txtBox.set_text("")
        txtBox2.set_text("")
        txtBox3.set_text("")


def show_votes():
    """
    A function to show the votes.
    This function will be called by the miner to show the votes.
    """
    if back_btn.update():
        global state
        state = "main_menu"
    votes = vs.get_votes()
    app.fill(0)
    app.font_size(20)
    app.text("Votes", 300, 10)
    app.text("Total Votes: " + str(vs.get_vote_count()), 100, 50)
    y = 100
    for candidate, count in votes.items():
        app.text(f"{candidate}: {count}", 100, y)
        y += 30
    

state = "main_menu"

while app.is_running:

    app.background(255)
    if state == "main_menu":
        main_menu()
    elif state == "register":
        register()
    elif state == "show_votes":
        show_votes()

    app.flip_display()
    app.event_loop()

p2p.stop_server()