#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import gg_lib as gg
import time

context = zmq.Context()

name_pl = "bot" # Nom de la plateforme

#  Socket to talk to server
print("Connecting to Get Gems server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
socket.send_string(gg.std_send_command("connect", "__client", name_pl))
time.sleep(1)
msg = socket.recv()
if msg == "1":
    print("Connected to Get Gems server")

#  Do 10 requests, waiting each time for a response
for request in range(10):
    socket.send_string(gg.std_send_command("mine", "gnouf1", name_pl))

    #  Get the reply.
    message = gg.std_receive_command(socket.recv())
    print(message["msg"])
