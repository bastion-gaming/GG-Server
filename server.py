#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import gg_lib as gg

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = gg.std_receive_command(socket.recv())
    print("Received request: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    if message["name_c"] == "connect":
        print("Le bot : " + message["name_pl"] + " est connecté")
        socket.send_string('1')



    #  Send reply back to client
    elif message["name_c"] == "mine":
        socket.send_string(gg.std_answer_command(message["name_c"], message["name_p"], message["name_pl"], "Vous avez bien miné !"))
    else:
        socket.send_string(message["name_p"])
