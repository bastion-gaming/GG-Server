from DB import SQLite as sql
from languages import lang as lang_P
from core import level as lvl
import random as r


# ========== Success ==========
class Success:

    def __init__(self, id, sid, nom, desc, type, objectif):
        self.id = id
        self.sid = sid
        self.nom = nom
        self.desc = desc
        self.type = type
        self.objectif = objectif # nombre de gems minimum necessaire


objetSuccess = [
    # Gems
    Success(1, 1, "Gems I", 0, "gems|1", 500),
    Success(1, 2, "Gems II", 1, "gems|2", 1000),
    Success(1, 3, "Gems III", 2, "gems|3", 5000),
    Success(1, 4, "Gems IV", 3, "gems|4", 50000),
    Success(1, 5, "Gems V", 4, "gems|5", 200000),
    Success(1, 6, "Gems VI", 5, "gems|6", 500000),
    Success(1, 7, "Gems VII", 6, "gems|7", 1000000),
    Success(1, 8, "Gems VIII", 7, "gems|8", 10000000),
    Success(1, 9, "Gems IX", 8, "gems|9", 100000000),
    Success(1, 10, "Gems X", 9, "gems|10", 500000000),
    Success(1, 11, "Gems XI", 10, "gems|11", 1000000000),


    # Mine
    Success(2, 1, "Pickaxe I", 11, "broken|mine|pickaxe", 1),
    Success(2, 2, "Pickaxe II", 11, "broken|mine|pickaxe", 10),
    Success(2, 3, "Pickaxe III", 11, "broken|mine|pickaxe", 100),

    Success(3, 1, "Miner I", 12, "mine|cobblestone", 300),
    Success(3, 2, "Miner II", 12, "mine|cobblestone", 500),
    Success(3, 3, "Miner III", 12, "mine|iron", 200),
    Success(3, 4, "Miner IV", 12, "mine|gold", 200),
    Success(3, 5, "Miner V", 12, "mine|iron", 400),
    Success(3, 6, "Miner VI", 12, "mine|diamond", 300),
    Success(3, 7, "Miner VII", 12, "mine|emerald", 400),


    # Dig
    Success(4, 1, "Shovel I", 11, "broken|dig|shovel", 1),
    Success(4, 2, "Shovel II", 11, "broken|dig|shovel", 10),
    Success(4, 3, "Shovel III", 11, "broken|dig|shovel", 100),

    Success(5, 1, "Digger I", 13, "dig|seed", 100),
    Success(5, 2, "Digger II", 13, "dig|cacao", 200),
    Success(5, 3, "Digger III", 13, "dig|potato", 600),
    Success(5, 4, "Digger IV", 13, "dig|seed", 2000),
    Success(5, 5, "Digger V", 13, "dig|potato", 3500),


    # Fish
    Success(6, 1, "Fishingrod I", 11, "broken|fish|fishingrod", 1),
    Success(6, 2, "Fishingrod II", 11, "broken|fish|fishingrod", 10),
    Success(6, 3, "Fishingrod III", 11, "broken|fish|fishingrod", 100),

    Success(7, 1, "Fisher I", 14, "fish|fish", 200),
    Success(7, 2, "Fisher II", 14, "fish|fish", 500),
    Success(7, 3, "Fisher III", 14, "fish|tropicalfish", 150),
    Success(7, 4, "Fisher IV", 14, "fish|blowfish", 300),
    Success(7, 5, "Fisher V", 14, "fish|octopus", 500),
    Success(7, 6, "Fisher VI", 14, "fish|fish", 8000),


    # Marché
    Success(8, 1, "Buy I", 15, "buy|total", 20),
    Success(8, 2, "Buy II", 15, "buy|total", 60),
    Success(8, 3, "Buy III", 15, "buy|total", 180),
    Success(8, 4, "Buy IV", 15, "buy|total", 400),
    Success(8, 5, "Buy V", 15, "buy|total", 1000),
    Success(8, 6, "Buy VI", 15, "buy|total", 2500),
    Success(8, 7, "Buy VII", 15, "buy|total", 4800),
    Success(8, 8, "Buy VIII", 15, "buy|total", 10000),
    Success(8, 9, "Buy IX", 15, "buy|total", 22000),
    Success(8, 10, "Buy X", 15, "buy|total", 50000),

    Success(9, 1, "Sell I", 16, "sell|total", 50),
    Success(9, 2, "Sell II", 16, "sell|total", 500),
    Success(9, 3, "Sell III", 16, "sell|total", 2000),
    Success(9, 4, "Sell IV", 16, "sell|total", 6000),
    Success(9, 5, "Sell V", 16, "sell|total", 13000),
    Success(9, 6, "Sell VI", 16, "sell|total", 30000),
    Success(9, 7, "Sell VII", 16, "sell|total", 55000),
    Success(9, 8, "Sell VIII", 16, "sell|total", 13000),
    Success(9, 9, "Sell IX", 16, "sell|total", 400000),
    Success(9, 10, "Sell X", 16, "sell|total", 1000000)
]


def checkSuccess(PlayerID, lang):
    result = []
    for x in objetSuccess:
        i = x.id
    nom = ""
    myStat = 0
    for i in range(1, i+1):
        iS = sql.valueAtNumber(PlayerID, i, "success")
        for x in objetSuccess:
            if x.id == i and x.sid == iS+1:
                type = x.type.split("|")

                if type[0] == "gems":
                    solde = sql.valueAtNumber(PlayerID, "gems", "gems")
                    if solde >= x.objectif:
                        nom = x.nom

                elif type[0] == "broken":
                    myStat = sql.valueAtNumber(PlayerID, "{0} | broken | {1}".format(type[1], type[2]), "statgems")
                    if myStat >= x.objectif:
                        nom = x.nom

                elif type[0] == "mine" or type[0] == "dig" or type[0] == "fish":
                    myStat = sql.valueAtNumber(PlayerID, "{0} | item | {1}".format(type[0], type[1]), "statgems")
                    if myStat >= x.objectif:
                        nom = x.nom

                elif type[0] == "buy" or type[0] == "sell":
                    myStat = sql.valueAtNumber(PlayerID, "{0} | {1}".format(type[0], type[1]), "statgems")
                    if myStat >= x.objectif:
                        nom = x.nom

#                 elif type[0] == "":
#                     myStat = sql.valueAtNumber(PlayerID, "", "statgems")
#                     if myStat >= x.objectif:
#                         nom = x.nom

                if nom != "":
                    sql.add(PlayerID, i, 1, "success")
                    result.append(x.nom)
                    desc = "{0}".format(lang_P.forge_msg(lang, "success", [x.nom], False, 0))
                    result.append(desc)
                    gain = r.randint(5, 15)**(iS+1)
                    lvl.addxp(PlayerID, gain, "gems")
                    desc = "{0} XP".format(lang_P.forge_msg(lang, "success", [gain], False, 1))
                    result.append(desc)
                    return result
    return result


# Commandes
def stats(param):
    nom = param["nom"]
    if nom != "None":
        nom = sql.nom_ID(nom)
        ID = sql.get_SuperID(nom, param["name_pl"])
    else:
        ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []
    desc = sql.valueAt(PlayerID, "all", "statgems")
    if desc != 0:
        msg.append("OK")
        msg.append(lang)
        for x in desc:
            msg.append(str(x))
    else:
        msg.append("NOK")
        msg.append(lang)
    return msg


def success(param):
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []
    result = []
    for x in objetSuccess:
        i = x.id
    for i in range(1, i+1):
        iS = sql.valueAtNumber(PlayerID, i, "success")
        for x in objetSuccess:
            arg = None
            if x.id == i and x.sid == iS+1:
                # print(x.nom)
                type = x.type.split("|")
                if type[0] == "gems":
                    myStat = sql.valueAtNumber(PlayerID, "gems", "gems")
                    arg = None
                elif type[0] == "broken":
                    myStat = sql.valueAtNumber(PlayerID, "{0} | broken | {1}".format(type[1], type[2]), "statgems")
                    arg = [x.objectif, type[2], "{idmoji[gem_" + type[2] + "]}"]
                elif type[0] == "mine" or type[0] == "dig" or type[0] == "fish":
                    myStat = sql.valueAtNumber(PlayerID, "{0} | item | {1}".format(type[0], type[1]), "statgems")
                    arg = [x.objectif, type[1], "{idmoji[gem_" + type[1] + "]}"]
                elif type[0] == "buy" or type[0] == "sell":
                    myStat = sql.valueAtNumber(PlayerID, "{0} | {1}".format(type[0], type[1]), "statgems")
                    arg = [x.objectif]
                result.append(x.nom)
                desc = "{0} | `{1}`/`{2}`".format(lang_P.forge_msg(lang, "success desc", arg, False, x.desc), myStat, x.objectif)
                result.append(desc)
    msg.append("OK")
    msg.append(lang)
    msg.append(result)
    return msg
