import time
import zmq
import gg_lib as gg
from core import level as lvl
from gems import gemsPlay as GGplay, gemsBase as GGbase, gemsFonctions as GF, gemsItems as GI
from DB import SQLite as sql

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
check = True
msg = ""
VERSION = open("core/version.txt").read().replace("\n","")

# Initialisation
print('\nGet Gems - Server '+VERSION)
print(sql.init())
flag = sql.checkField()
if flag == 0:
    print("SQL >> Aucun champ n'a été ajouté, supprimé ou modifié.")
elif "add" in flag:
    print("SQL >> Un ou plusieurs champs ont été ajoutés à la DB.")
elif "sup" in flag:
    print("SQL >> Un ou plusieurs champs ont été supprimés de la DB.")
elif "type" in flag:
    print("SQL >> Un ou plusieurs type ont été modifié sur la DB.")

try :
    GF.loadItem()
except FileNotFoundError :
    GI.initBourse() # Cas où la bourse n'existait pas

while check:
    #  Wait for next request from client
    platform = ""
    message = gg.std_receive_command(socket.recv())
    print("\n•••••\nReceived request: %s" % message)

    if message["name_c"] == "connect":
        print("Le bot : " + message["name_pl"] + " est connecté")
        socket.send_string('1')
    elif message["name_c"] == "stop":
        print("Arret de GG Serveur ...")
        check = False
        socket.send_string(gg.std_answer_command(message["name_c"], message["name_p"], message["name_pl"], "GG serveur c'est arrêté"))


    #  Send reply back to client
    else:
        if message["name_pl"] == "discord" or message["name_pl"] == "babot":
            platform = "discord"
        elif message["name_pl"] == "messenger":
            platform = "messenger"
        ID = sql.get_SuperID(message["name_p"], platform)

        # Daily
        if message["name_c"] == "daily":
            socket.send_string(gg.std_answer_command(message["name_c"], message["name_p"], message["name_pl"], GGplay.daily(ID)))

        # Begin
        elif message["name_c"] == "begin":
            socket.send_string(gg.std_answer_command(message["name_c"], message["name_p"], message["name_pl"], GGbase.begin(message["name_p"], platform)))

        # Crime
        elif message["name_c"] == "crime":
            socket.send_string(gg.std_answer_command(message["name_c"], message["name_p"], message["name_pl"], GGplay.crime(ID)))

        # Stealing
        elif message["name_c"] == "stealing":
            print(message["param_c"])
            socket.send_string(gg.std_answer_command(message["name_c"], message["name_p"], message["name_pl"], GGplay.stealing(ID, message["param_c"])))

        # Mine
        elif message["name_c"] == "mine":
            socket.send_string(gg.std_answer_command(message["name_c"], message["name_p"], message["name_pl"], "Vous avez bien miné !"))

        # Bal
        elif message["name_c"] == "bal":
            socket.send_string(gg.std_answer_command(message["name_c"], message["name_p"], message["name_pl"], GGbase.bal(ID)))

        # Autre
        elif message["name_c"] == "level":
            socket.send_string(gg.std_answer_command(message["name_c"], message["name_p"], message["name_pl"], lvl.checklevel(ID)))
        else:
            socket.send_string(gg.std_answer_command(message["name_c"], message["name_p"], message["name_pl"], "Commande non reconnu"))
