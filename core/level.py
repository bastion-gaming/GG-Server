from DB import SQLite as sql
from languages import lang as lang_P
from gems import gemsSuccess as success

# Un = 100 × (1.4)^n


def addxp(ID, nb, nameDB):
    balXP = sql.valueAtNumber(ID, "xp", nameDB)
    if balXP != None:
        ns = balXP + int(nb)
        if ns <= 0:
            ns = 0
        sql.updateField(ID, "xp", ns, nameDB)
        return True
    else:
        return False


def checklevel(ID):
    lang = sql.valueAtNumber(ID, "LANG", "IDs")
    if lang == None:
        lang = "EN"
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    # print(PlayerID)
    msg = []
    S = success.checkSuccess(PlayerID, lang)
    try:
        lvl = sql.valueAtNumber(PlayerID, "lvl", "gems")
        xp = sql.valueAtNumber(PlayerID, "xp", "gems")
        palier = lvlPalier(lvl)
        desc = ""
        if xp >= palier:
            lvl = lvl+1
            sql.updateField(PlayerID, "lvl", lvl, "gems")
            desc = lang_P.forge_msg(lang, "level", [lvl], False, 0)
            nbG = 100*lvl
            sql.addGems(PlayerID, nbG)
            desc += lang_P.forge_msg(lang, "level", [nbG], False, 1)
            msg.append("Level UP")
        else:
            msg.append("Level OK")
        msg.append(desc)
        if S != []:
            msg.append(S)
    except:
        print("Level >> Le joueur n'existe pas.")
        msg.append("Level NOK")
        msg.append("Le joueur n'existe pas")
    return msg


def lvlPalier(lvl):
    if lvl > 0:
        return int(100 * (1.4)**lvl)
    else:
        return 60
