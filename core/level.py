import random as r
import datetime as dt
from DB import SQLite as sql
from gems import gemsFonctions as GF
import json

lvlmax = 19
# Un = 100 × (1.4)^n

class XP:

    def __init__(self,level,somMsg):
        self.level = level
        self.somMsg = somMsg

objetXP = [XP(0,100)
,XP(1,256)
,XP(2,625)
,XP(3,1210)
,XP(4,2401)
,XP(5,4096)
,XP(6,6561)
,XP(7,10930)
,XP(8,16342)
,XP(9,20000)
,XP(10,27473)
,XP(11,34965)
,XP(12,42042)
,XP(13,55739)
,XP(14,66778)
,XP(15,78912)
,XP(16,86493)
,XP(17,95105)
,XP(18,10187)
,XP(19,111111)]


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
