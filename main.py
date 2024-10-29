from hooman import Hooman
import pygame
from core.p2p.P2P import P2P

PORT = 5001

app = Hooman(800, 600)
p2p = P2P(PORT)


while app.is_running:

    app.background(255)

    app.fill(0)
    app.font_size(20)
    app.text("P2P Network", 300, 10, )
    app.text("Port: " + str(PORT), 300, 100)

    app.text("Connected Nodes", 300, 200)
    for i, node in enumerate(p2p.peer_nodes):
        app.text(node, 300, 250 + i * 50)

    app.flip_display()
    app.event_loop()

p2p.stop_server()