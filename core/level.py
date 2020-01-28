import random as r
import datetime as dt
from DB import SQLite as sql
from gems import gemsFonctions as GF
import json

lvlmax = 19
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
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    # print(PlayerID)
    try:
        lvl = sql.valueAtNumber(PlayerID, "lvl", "gems")
        xp = sql.valueAtNumber(PlayerID, "xp", "gems")
        palier = lvlPalier(lvl)
        desc = ""
        if xp >= palier:
            sql.updateField(PlayerID, "lvl", lvl+1, "gems")
            desc = ":tada: {1} a atteint le niveau **{0}**".format(lvl+1, "{PlayerName}")

            nbS = lvl // 5
            nbG = lvl % 5
            if nbS != 0:
                sql.addSpinelles(PlayerID, nbS)
                desc += "\nTu gagne {} <:spinelle:{}>`spinelles`".format(nbS, "{idmoji[spinelle]}")
            if nbG != 0:
                nbG = nbG * 50000
                sql.addGems(PlayerID, nbG)
                desc += "\nTu gagne {} :gem:`gems`".format(nbG)
        return desc
    except:
        print("Le joueur n'existe pas.")
        return ""

def lvlPalier(lvl):
    if lvl >= 0:
        return int(100 * (1.4)**lvl)
    else:
        return 60
