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

    Success(3, 1, "Mine I", 12, "mine|cobblestone", 300),
    Success(3, 2, "Mine II", 12, "mine|cobblestone", 500),
    Success(3, 3, "Mine III", 12, "mine|iron", 200),
    Success(3, 4, "Mine IV", 12, "mine|gold", 200),
    Success(3, 5, "Mine V", 12, "mine|iron", 400),
    Success(3, 6, "Mine VI", 12, "mine|diamond", 300),
    Success(3, 7, "Mine VII", 12, "mine|emerald", 400),


    # Dig
    Success(4, 1, "Shovel I", 11, "broken|dig|shovel", 1),
    Success(4, 2, "Shovel II", 11, "broken|dig|shovel", 10),
    Success(4, 3, "Shovel III", 11, "broken|dig|shovel", 100),

    Success(5, 1, "Dig I", 13, "dig|seed", 100),
    Success(5, 2, "Dig II", 13, "dig|cacao", 200),
    Success(5, 3, "Dig III", 13, "dig|potato", 500),
    Success(5, 4, "Dig IV", 13, "dig|seed", 2000),
    Success(5, 5, "Dig V", 13, "dig|potato", 3000),


    # Fish
    Success(6, 1, "Fishingrod I", 11, "broken|fish|fishingrod", 1),
    Success(6, 2, "Fishingrod II", 11, "broken|fish|fishingrod", 10),
    Success(6, 3, "Fishingrod III", 11, "broken|fish|fishingrod", 100),

    Success(7, 1, "Fish I", 14, "fish|fish", 200),
    Success(7, 2, "Fish II", 14, "fish|fish", 500),
    Success(7, 3, "Fish III", 14, "fish|tropicalfish", 150),
    Success(7, 4, "Fish IV", 14, "fish|blowfish", 300),
    Success(7, 5, "Fish V", 14, "fish|octopus", 500),
    Success(7, 6, "Fish VI", 14, "fish|fish", 8000)
]


def checkSuccess(PlayerID, lang):
    result = []
    for x in objetSuccess:
        i = x.id
    print(i)
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

#                 elif type[0] == "":
#                     myStat = sql.valueAtNumber(PlayerID, "", "statgems")
#                     if myStat >= x.objectif:
#                         nom = x.nom

                if nom != "":
                    sql.add(PlayerID, i, 1, "success")
                    result.append(x.nom)
                    desc = "{0}".format(lang_P.forge_msg(lang, "success", [x.nom], False, 0))
                    result.append(desc)
                    gain = r.randint(10, 30)*(iS+1)
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
                    arg = [x.objectif, type[2]]
                elif type[0] == "mine" or type[0] == "dig" or type[0] == "fish":
                    myStat = sql.valueAtNumber(PlayerID, "{0} | item | {1}".format(type[0], type[1]), "statgems")
                    arg = [x.objectif, type[1]]
                result.append(x.nom)
                desc = "{0} | `{1}`/`{2}`".format(lang_P.forge_msg(lang, "success desc", arg, False, x.desc), myStat, x.objectif)
                result.append(desc)
    msg.append("OK")
    msg.append(lang)
    msg.append(result)
    return msg
