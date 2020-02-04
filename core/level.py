from DB import SQLite as sql
from gems import gemsFonctions as GF

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
    msg = []
    try:
        lvl = sql.valueAtNumber(PlayerID, "lvl", "gems")
        xp = sql.valueAtNumber(PlayerID, "xp", "gems")
        palier = lvlPalier(lvl)
        desc = ""
        if xp >= palier:
            sql.updateField(PlayerID, "lvl", lvl+1, "gems")
            desc = "a atteint le niveau **{0}**".format(lvl+1)
            if lvl <= 5:
                nbG = 100*lvl
            else:
                nbG = 3**lvl
            sql.addGems(PlayerID, nbG)
            desc += "\nTu gagne {} :gem:`gems`".format(nbG)
            msg.append("Level UP")
        else:
            msg.append("Level OK")
        msg.append(desc)
    except:
        print("Level >> Le joueur n'existe pas.")
        msg.append("Level NOK")
        msg.append("Le joueur n'existe pas")
    return msg


def lvlPalier(lvl):
    if lvl >= 0:
        return int(100 * (1.4)**lvl)
    else:
        return 60
