import random as r
import time as t
import datetime as dt
from database import SQLite as sql
from gems import gemsFonctions as GF
from core import level as lvl


def daily(param):
    """Récupère ta récompense journalière!"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    # =======================================================================
    # Initialisation des variables générales de la fonction
    # =======================================================================
    DailyTime = sql.value(PlayerID, "gems", "DailyTime")
    DailyMult = sql.value(PlayerID, "gems", "DailyMult")
    jour = dt.date.today()
    # =======================================================================
    # Détermination du daily
    # =======================================================================
    if DailyTime == str(jour - dt.timedelta(days=1)):
        sql.update(PlayerID, "gems", "DailyTime", str(jour))
        sql.update(PlayerID, "gems", "DailyMult", DailyMult + 1)

        f = 100 * (1.1**((DailyMult//20)-1))
        bonus = int(int(f)*DailyMult)
        gain = 100 + bonus
        sql.addGems(PlayerID, gain)
        if DailyMult < 6:
            DailyXP = 5
        else:
            DailyXP = int(5*(DailyMult/6))
        lvl.addxp(PlayerID, DailyXP)
        if DailyMult % 30 == 0:
            m = int(gain*0.2)
            sql.addGems(PlayerID, m)
        else:
            m = 0
        return {'error': 0, 'etat': 'OK', 'lang': lang, 'DailyMult': int(DailyMult), 'bonus': bonus, 'XP': DailyXP, 'Gems': gain, 'm': m}

    elif DailyTime == str(jour):
        return {'error': 1, 'etat': 'NOK', 'lang': lang}
    else:
        sql.update(PlayerID, "gems", "DailyTime", str(jour))
        sql.update(PlayerID, "gems", "DailyMult", 1)
        lvl.addxp(PlayerID, 5)
        sql.addGems(PlayerID, 100)
        return {'error': 2, 'etat': 'OK', 'lang': lang, 'DailyMult': int(DailyMult), 'bonus': 0, 'XP': 5, 'Gems': 100, 'm': 0}


def bank(param):
    """La banque"""
    # =======================================================================
    # Initialistation des variables générales de la fonction
    # =======================================================================
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    ARG = param["ARG"]
    ARG2 = param["ARG2"]
    platform = param["name_pl"]

    if ARG != "None":
        mARG = ARG.lower()
    else:
        mARG = "bal"
    for c in GF.objetUpgrade:
        if c.type == "bank":
            Taille = c.achat
    solde = sql.value(PlayerID, "gems", "BankSolde")
    if solde == 0:
        sql.update(PlayerID, "gems", "SoldeMax", Taille)
    if mARG == "bal":
        msg = bank_bal(PlayerID, lang, ARG, ARG2, Taille, platform)
    elif mARG == "add":
        msg = bank_add(PlayerID, lang, ARG, ARG2, Taille)
    elif mARG == "saving":
        msg = bank_saving(PlayerID, lang, ARG, ARG2, Taille)
    else:
        return {'error': 2, 'etat': 'NOK', 'lang': lang}
    return msg


def bank_bal(PlayerID, lang, ARG, ARG2, Taille, platform):
    """La banque | Balance du compte"""
    # =======================================================================
    # Affiche le menu principal de la banque
    # !bank bal <nom d'un joueur> permet de visualiser l'état de la banque de ce joueur
    # =======================================================================
    if sql.spam(PlayerID, GF.couldown("4s"), "bank_bal"):
        if ARG2 != "None":
            ID = sql.get_PlayerID(sql.nom_ID(ARG2, platform))
            if ID['error'] == 404:
                return {'error': 405, 'etat': 'PlayerID', 'lang': lang}
            PlayerID = ID['ID']
        name = sql.value(PlayerID, "gems", "Pseudo")
        solde = sql.value(PlayerID, "gems", "BankSolde")
        soldeMax = sql.value(PlayerID, "gems", "BankSMax")
        if soldeMax == 0:
            soldeMax = Taille
        soldeMult = int(soldeMax/Taille)
        pourcentage = 0.049 + soldeMult*0.001
        if pourcentage > 0.6:
            pourcentage = 0.6
        sql.updateComTime(PlayerID, "bank_bal")
        return {'error': 0, 'etat': 'OK', 'lang': lang, 'type': 'bal', 'BankSolde': solde, 'BankSMax': soldeMax, '%': pourcentage*100, 'name': name}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'couldown': str(GF.couldown("4s"))}


def bank_add(PlayerID, lang, ARG, ARG2, Taille):
    """La banque | Crédits"""
    # =======================================================================
    # Ajoute ou enlève des Gems sur le compte épargne
    # un nombre positif ajoute des Gems
    # un nombre négatif enlève des Gems
    # =======================================================================
    if sql.spam(PlayerID, GF.couldown("4s"), "bank_add"):
        if ARG2 != "None":
            ARG2 = int(ARG2)
            gems = sql.value(PlayerID, "gems", "Gems")
            solde = sql.value(PlayerID, "gems", "BankSolde")
            soldeMax = sql.value(PlayerID, "gems", "BankSMax")
            if soldeMax == 0:
                soldeMax = Taille
            if ARG2 <= gems:
                soldeNew = solde + ARG2
                if soldeNew > soldeMax:
                    ARG2 = ARG2 - (soldeNew - soldeMax)
                    soldeNew = soldeMax
                elif soldeNew < 0:
                    return {'error': 2, 'etat': 'NOK', 'type': 'add', 'lang': lang, 'BankSolde': solde}
                nbgm = -1*ARG2
                sql.addGems(PlayerID, nbgm)
                sql.update(PlayerID, "gems", "BankSolde", soldeNew)
                sql.updateComTime(PlayerID, "bank_add")
                return {'error': 0, 'etat': 'OK', 'type': 'add', 'lang': lang, 'BankSolde': solde, 'BankSMax': soldeMax, 'BankSNew': soldeNew, 'BankSAdd': ARG2}
            else:
                return {'error': 4, 'etat': 'NOK', 'type': 'add', 'lang': lang}
        else:
            return {'error': 3, 'etat': 'NOK', 'type': 'add', 'lang': lang}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'couldown': str(GF.couldown("4s"))}


def bank_saving(PlayerID, lang, ARG, ARG2, Taille):
    """La banque | Épargne"""
    # =======================================================================
    # Fonction d'épargne
    # L'intéret est de 20% avec un bonus de 1% pour chanque bank_upgrade possédée
    # =======================================================================
    if sql.spam(PlayerID, GF.couldown("4h"), "bank_saving"):
        solde = sql.value(PlayerID, "gems", "BankSolde")
        if solde != 0:
            soldeMax = sql.value(PlayerID, "gems", "BankSMax")
            if soldeMax == 0:
                soldeMax = Taille
            soldeMult = soldeMax/Taille
            pourcentage = 0.049 + soldeMult*0.001
            if pourcentage > 0.6:
                pourcentage = 0.6
            soldeAdd = pourcentage*solde
            Taxe = GF.taxe(soldeAdd, 0.1)
            soldeAdd = Taxe["new solde"]
            sql.update(PlayerID, "gems", "BankSolde", int(solde + soldeAdd))
            soldeNew = solde + soldeAdd
            if soldeNew > soldeMax:
                soldeMove = soldeNew - soldeMax
                sql.addGems(PlayerID, int(soldeMove))
                sql.update(PlayerID, "gems", "BankSolde", soldeMax)
            GF.addStats(PlayerID, ["bank", "bank saving"], 1)
            GF.addStats(PlayerID, ["bank", "bank | saving | gain"], int(soldeAdd))
            try:
                sql.addGems(GF.PlayerID_GetGems, int(Taxe["taxe"]))
            except:
                print("Le bot ne fait pas parti de la DB")
            sql.updateComTime(PlayerID, "bank_saving")
            lvl.addxp(PlayerID, 4)
            return {'error': 0, 'etat': 'OK', 'type': 'saving', 'lang': lang, 'BankSOld': solde, 'BankSMax': soldeMax, 'BankSAdd': int(soldeAdd), 'BankSNew': sql.value(PlayerID, 'gems', "BankSolde"), 'XP': 4}
        else:
            return {'error': 5, 'etat': 'NOK', 'type': 'saving', 'lang': lang, 'BankSolde': sql.value(PlayerID, 'gems', "BankSolde")}
    else:
        ComTime = sql.value(PlayerID, 'gems_com_time', "Com_Time", "Commande", "bank_saving")
        time = float(ComTime) - (t.time()-GF.couldown("4h"))
        timeH = int(time / 60 / 60)
        time = time - timeH * 3600
        timeM = int(time / 60)
        timeS = int(time - timeM * 60)
        return {'error': 6, 'etat': 'NOK', 'type': 'saving', 'lang': lang, 'time': [timeH, timeM, timeS]}


def stealing(param):
    """**[nom]** | Vole des :gem:`gems` aux autres joueurs!"""
    name = param["name"]
    lang = param["lang"]
    PlayerID = param["PlayerID"]

    if sql.value(GF.PlayerID_GetGems, "gems", "DailyMult") == 1:
        return {'error': -1, 'etat': 'Not Activate', 'lang': lang}
    else:
        if sql.spam(PlayerID, GF.couldown("14h"), "stealing") and name != "None":
            ID = sql.get_PlayerID(sql.nom_ID(name), param["name_pl"])
            if ID['error'] == 404:
                return {'error': 405, 'etat': 'PlayerID', 'lang': lang}
            ID_Vol = ID['ID']
            name_Vol = sql.value(ID_Vol, "gems", "Pseudo")
            # Calcul du pourcentage
            if ID_Vol == GF.PlayerID_GetGems:
                R = r.randint(1, 9)
            else:
                R = "05"
            P = float("0.0{}".format(R))
            try:
                Solde = sql.value(ID_Vol, "gems", "Gems")
                Taxe = GF.taxe(int(Solde*P), 0.2)
                gain = int(Taxe["new solde"])
                if gain != 0:
                    try:
                        if ID_Vol != GF.PlayerID_GetGems:
                            sql.addGems(GF.PlayerID_GetGems, int(Taxe["taxe"]))
                    except:
                        print("Le bot ne fait pas parti de la DB")
                    result = {'DiscordCop': False, 'gain': False, 'perte': False}
                    if r.randint(0, 6) == 0:
                        GF.addStats(PlayerID, ["divers", "DiscordCop Arrestation"], 1)
                        if int(sql.addGems(PlayerID, int(gain/4))) >= 100:
                            result['perte'] = int(gain/4)
                        else:
                            result['perte'] = sql.value(PlayerID, "gems", "Gems")
                            sql.update(PlayerID, "gems", "Gems", 0)
                        result['DiscordCop'] = True
                    else:
                        sql.addGems(PlayerID, gain)
                        sql.addGems(ID_Vol, -gain)
                        result['gain'] = gain
                        print("Gems >> PlayerID {2} viens de voler {0} gems à {1}".format(gain, ID_Vol, PlayerID))
                        GF.addStats(PlayerID, ["stealing", "stealing | gain"], gain)
                    sql.updateComTime(PlayerID, "stealing")
                    lvl.addxp(PlayerID, 1)
                    GF.addStats(PlayerID, ["stealing", "stealing"], 1)
                    return {'error': 0, 'etat': 'NOK', 'lang': lang, 'nameVol': name_Vol, 'result': result}
                else:
                    return {'error': 4, 'etat': 'NOK', 'lang': lang, 'nameVol': name_Vol}
            except:
                return {'error': 3, 'etat': 'NOK', 'lang': lang, 'nameVol': name_Vol}
        elif sql.spam(PlayerID, GF.couldown("14h"), "stealing"):
            return {'error': 2, 'etat': 'NOK', 'lang': lang}
        else:
            ComTime = sql.value(PlayerID, 'gems_com_time', "Com_Time", "Commande", "stealing")
            time = float(ComTime) - (t.time()-GF.couldown("14h"))
            timeH = int(time / 60 / 60)
            time = time - timeH * 3600
            timeM = int(time / 60)
            timeS = int(time - timeM * 60)
            return {'error': 1, 'etat': 'NOK', 'lang': lang, 'time': [timeH, timeM, timeS]}
