from database import SQLite as sql
from gems import gemsSuccess as success

# Un = 100 × (1.4)^n


def addxp(ID, nb):
    balXP = sql.value(ID, "gems", "XP")
    if balXP != None:
        ns = balXP + int(nb)
        if ns <= 0:
            ns = 0
        sql.update(ID, "gems", "XP", ns)
        return True
    else:
        return False


def checklevel(ID, platform):
    PlayerID = sql.get_PlayerID(ID, platform)
    lang = sql.value(PlayerID['ID'], "gems", "Lang")
    if lang == None:
        lang = "EN"
    if PlayerID['error'] == 404:
        return {'error': 404, 'etat': 'PlayerID', 'lang': lang, 'gain': False, 'perte': False, 'success': False}
    PlayerID = PlayerID['ID']
    # print(PlayerID)
    msg = dict()
    S = success.checkSuccess(PlayerID, lang)
    try:
        lvl = sql.value(PlayerID, "gems", "Level")
        xp = sql.value(PlayerID, "gems", "XP")
        palier = lvlPalier(lvl)
        if xp >= palier:
            lvl = lvl+1
            sql.update(PlayerID, "gems", "Level", lvl)
            nbG = 100*lvl
            sql.addGems(PlayerID, nbG)
            msg = {'error': 0, 'etat': 'Level UP', 'lang': lang, 'gain': {'gems': nbG, 'level': lvl}, 'perte': False, 'success': False}
        else:
            msg = {'error': 0, 'etat': 'Level OK', 'lang': lang, 'gain': False, 'perte': False, 'success': False}
        if S != []:
            msg['success'] = S
    except:
        print("Level >> Le joueur n'existe pas.")
        msg = {'error': 1, 'etat': 'Level NOK', 'lang': lang, 'gain': False, 'perte': False, 'success': False}
    return msg


def lvlPalier(lvl):
    if lvl > 0:
        return int(100 * (1.4)**lvl)
    else:
        return 60
