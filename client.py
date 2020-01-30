#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import gg_lib as gg
import time

name_pl = "bot" # Nom de la plateforme

check = True
error = 0
ListCommands = ["mine", "crime"]

REQUEST_TIMEOUT = 2500
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://localhost:5555"

context = zmq.Context(1)

#  Socket to talk to server
print("Connecting to Get Gems server…")
socket = context.socket(zmq.REQ)
socket.connect(SERVER_ENDPOINT)
# TIMEOUT
poll = zmq.Poller()
poll.register(socket, zmq.POLLIN)

socket.send_string(gg.std_send_command("connect", "__client", name_pl))
time.sleep(1)
socks = dict(poll.poll(REQUEST_TIMEOUT))
if socks.get(socket) == zmq.POLLIN:
    msg = socket.recv()
    if msg.decode() == "1":
        print("Connected to Get Gems server")
else:
    print("Aucune réponse du serveur")
    check = False
    # Socket is confused. Close and remove it.
    socket.setsockopt(zmq.LINGER, 0)
    socket.close()
    poll.unregister(socket)


while check:
    print("\nCommande:")
    x = input()
    x = x.lower()

    if x == "stop":
        check = False
    else:
        if x == "stop server":
            socket.send_string(gg.std_send_command("stop", "admin", name_pl))
        elif x in ListCommands:
            socket.send_string(gg.std_send_command(x, 129362501187010561, name_pl))

        #  Get the reply.
        socks = dict(poll.poll(REQUEST_TIMEOUT))
        if socks.get(socket) == zmq.POLLIN:
            message = gg.std_receive_command(socket.recv())
            print(message['msg'])
        else:
            print("Aucune réponse du serveur")
            # Socket is confused. Close and remove it.
            socket.setsockopt(zmq.LINGER, 0)
            socket.close()
            poll.unregister(socket)
            # Create new connection
            socket = context.socket(zmq.REQ)
            socket.connect(SERVER_ENDPOINT)
            poll.register(socket, zmq.POLLIN)
