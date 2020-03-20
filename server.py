import zmq
import gg_lib as gg
from DB import SQLite as sql
from gems import gemsFonctions as GF, gemsItems as GI
from core import level as lvl
from core import manage_seasons as MS
import manage_commands as mc
from languages import lang

# Ouverture du port
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
check = True
msg = ""
VERSION = open("core/version.txt").read().replace("\n", "")


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

sql.newPlayer(GF.idGetGems, "gems", "discord", "Get Gems")
sql.newPlayer(GF.idBaBot, "gems", "discord", "BaBot")

lang.init()

MS.init_season()

try:
    GF.loadItem(True)
except FileNotFoundError:
    # Cas où la bourse n'existait pas
    GI.initBourse()
    GF.loadItem()

while check:
    skip = False
    #  Wait for next request from client
    message = gg.std_receive_command(socket.recv())

    print("\n•••••\nReceived request: %s" % message)

    if message["name_c"] == "GGconnect":
        print(">>> Client " + message["name_pl"] + " est connecté")
        socket.send_string('1')
        skip = True

    if message["name_pl"] == "babot" or message["name_pl"] == "get gems":
        message["name_pl"] = "discord"

    if not skip:
        if message["name_c"] == "stop":
            print("Arret de GG Serveur ...")
            check = False
            socket.send_string(gg.std_answer_command(message["name_c"], message["name_p"], message["name_pl"], "GG serveur c'est arrêté"))
        elif message["name_c"] == "level":
            ID = sql.get_SuperID(message["name_p"], message["name_pl"])
            socket.send_string(gg.std_answer_command(message["name_c"], message["name_p"], message["name_pl"], lvl.checklevel(ID)))
        elif message["name_c"] == "NewServer":
            NewServer = sql.newGuild(message["param_c"])
            msg = []
            if NewServer == "Le serveur a été ajouté !":
                msg.append("OK")
            else:
                msg.append("NOK")
            socket.send_string(gg.std_answer_command(message["name_c"], message["name_p"], message["name_pl"], msg))

        # Send reply back to client
        else:
            retDict = mc.exec_commands(message)

            if retDict is not None:
                socket.send_string(gg.std_answer_command(retDict["name_c"], retDict["name_p"], retDict["name_pl"], retDict["reponse"]))

            else:
                socket.send_string(gg.std_answer_command(message["name_c"], message["name_p"], message["name_pl"], ["404", "Commande non reconnu"]))
