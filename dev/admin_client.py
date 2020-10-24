import zmq
import gg_lib as gg
import time

name_pl = "Admin" # Nom de la plateforme

check = True
error = 0
AdminCommands = ["update", "add", "value", "addgems", "gems", "addspinelles", "spinelles", "balance total", "playerid", "inventory"]

REQUEST_TIMEOUT = 2500
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://localhost:5555"

context = zmq.Context(1)

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect(SERVER_ENDPOINT)
# TIMEOUT
poll = zmq.Poller()
poll.register(socket, zmq.POLLIN)

socket.send_string(gg.std_send_command("GGconnect", "__client", name_pl))
time.sleep(1)
socks = dict(poll.poll(REQUEST_TIMEOUT))
if socks.get(socket) == zmq.POLLIN:
    msg = gg.std_receive_command(socket.recv())
    if msg['msg']['connect'] is True:
        print("Connected to Get Gems server")
else:
    print("No reply from the server")
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
        elif x == "commands" or x == "help" or x == "?":
            print("=====================================")
            print("======== Liste des commandes ========")
            print("\n=== Commandes générales ===")
            print("• commands")
            print("• stop")
            print("• stop server")
            print("\n=== Commandes administrateur ===")
            for c in AdminCommands:
                print("• {}".format(c))
            print("=====================================")
        elif x in AdminCommands:
            param = dict()
            param["fct"] = x.lower()
            param["ID"] = 620558080551157770
            param["arg2"] = "None"
            param["arg3"] = "None"
            param["arg4"] = "None"
            print("==========================\n===== Admin Commands =====\n==========================\n")
            if x != "balance total" and x != "playerid":
                print("• PlayerID:")
                param["ID"] = input()
            # if x == "update":
            #     # arg2 = nameDB | arg3 = fieldName | arg4 = fieldValue
            #     print("\n• nameDB:")
            #     param["arg2"] = input()
            #     print("\n• fieldName:")
            #     param["arg3"] = input()
            #     print("\n• fieldValue:")
            #     param["arg4"] = input()
            # elif x == "add":
            #     # arg2 = nameDB | arg3 = nameElem | arg4 = nbElem
            #     print("nameDB:")
            #     param["arg2"] = input()
            #     print("\n• nameElem:")
            #     param["arg3"] = input()
            #     print("\n• nbElem:")
            #     param["arg4"] = input()
            # elif x == "value":
            #     # arg2 = nameDB | arg3 = nameElem
            #     print("\n• nameDB:")
            #     param["arg2"] = input()
            #     print("\n• nameElem:")
            #     param["arg3"] = input()
            elif x == "addgems":
                # arg2 = nb gems
                print("\n• Nombre de gems à ajouter:")
                param["arg2"] = input()
            elif x == "addspinelles":
                # arg2 = nb spinelles
                print("Nombre de spinelles à ajouter:")
                param["arg2"] = input()
            elif x == "playerid":
                print("• Platforme:")
                param["arg2"] = input()
                print("\n• ID du joueur sur la platforme:")
                param["ID"] = input()
            socket.send_string(gg.std_send_command("admin", 620558080551157770, name_pl, param))
        elif x == "test":
            print("> test")

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
