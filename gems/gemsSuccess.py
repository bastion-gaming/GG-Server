from DB import SQLite as sql
from languages import lang as lang_P


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
    Success(1, 1, "Gems 500", 0, "gems", 500),
    Success(1, 2, "Gems 1k", 1, "gems", 1000),
    Success(1, 3, "Gems 5k", 2, "gems", 5000),
    Success(1, 4, "Gems 50k", 3, "gems", 50000),
    Success(1, 5, "Gems 200k", 4, "gems", 200000),
    Success(1, 6, "Gems 500k", 5, "gems", 500000),
    Success(1, 7, "Gems 1M", 6, "gems", 1000000),
    Success(1, 8, "Gems 10M", 7, "gems", 10000000),
    Success(1, 9, "Gems 100M", 8, "gems", 100000000),
    Success(1, 10, "Gems 500M", 9, "gems", 500000000),
    Success(1, 11, "Gems 1B", 10, "gems", 1000000000)
]


def checkSuccess(PlayerID, lang):
    result = []
    for x in objetSuccess:
        i = x.id
    for i in range(1, i+1):
        iS = sql.valueAtNumber(PlayerID, i, "success")
        print(iS)
        for x in objetSuccess:
            if x.id == i and x.sid == iS+1:
                print(x.nom)
                if x.type == "gems":
                    solde = sql.valueAtNumber(PlayerID, "gems", "gems")
                    if solde >= x.objectif:
                        sql.add(PlayerID, i, 1, "success")
                        result.append(x.nom)
                        desc = "{0}".format(lang_P.forge_msg(lang, "success desc", None, False, x.desc))
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
            if x.id == i and x.sid == iS+1:
                print(x.nom)
                if x.type == "gems":
                    solde = sql.valueAtNumber(PlayerID, "gems", "gems")
                    result.append(x.nom)
                    desc = "{0} | `{1}`/`{2}`".format(lang_P.forge_msg(lang, "success desc", None, False, x.desc), solde, x.objectif)
                    result.append(desc)
    msg.append("OK")
    msg.append(lang)
    msg.append(result)
    # desc = sql.valueAt(PlayerID, "all", "success")
    # if desc != 0:
    #     msg.append("OK")
    #     msg.append(lang)
    #     for x in desc:
    #         msg.append(str(x))
    # else:
    #     msg.append("NOK")
    #     msg.append(lang)
    return msg
