#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import gg_lib as gg
import time

name_pl = "bot" # Nom de la plateforme

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
msg = socket.recv()
if msg.decode() == "1":
    print("Connected to Get Gems server")

check = True
error = 0
ListCommands = ["mine", "fish"]

#  Do 10 requests, waiting each time for a response
while check:
    print("\nCommande:")
    x = input()
    x = x.lower()

    if x == "stop":
        check = False
    else:
        if x == "stop server":
            socket.send_string(gg.std_send_command("stop", "gnouf1", name_pl))
            # check = False
        elif x in ListCommands:
            socket.send_string(gg.std_send_command(x, "gnouf1", name_pl))

        #  Get the reply.
        socks = dict(poll.poll(REQUEST_TIMEOUT))
        print(socks)
        print(zmq.POLLIN)
        if socks.get(socket) == zmq.POLLIN:
            message = gg.std_receive_command(socket.recv())
            print(message['msg'])
        else:
            print("W: No response from server, retrying…")
            # Socket is confused. Close and remove it.
            socket.setsockopt(zmq.LINGER, 0)
            socket.close()
            poll.unregister(socket)
            # Create new connection
            socket = context.socket(zmq.REQ)
            socket.connect(SERVER_ENDPOINT)
            poll.register(socket, zmq.POLLIN)
