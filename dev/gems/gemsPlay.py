import random as r
import time as t
import datetime as dt
from database import SQLite as sql
import sqlite3
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
                    return {'error': 0, 'etat': 'OK', 'lang': lang, 'nameVol': name_Vol, 'result': result}
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


def crime(param):
    """Commets un crime et gagne des :gem:`gems` Attention au DiscordCop!"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    result = {'DiscordCop': False, 'gain': False, 'perte': False, 'event': False}

    if sql.spam(PlayerID, GF.couldown("6s"), "crime"):
        # si 10 sec c'est écoulé depuis alors on peut en  faire une nouvelle
        if r.randint(0, 9) == 0:
            GF.addStats(PlayerID, ["divers", "DiscordCop Arrestation"], 1)
            if int(sql.addGems(PlayerID, -10)) >= 100:
                result['perte'] = 10
            else:
                result['perte'] = sql.value(PlayerID, "gems", "Gems")
                sql.update(PlayerID, "gems", "Gems", 0)
            result['DiscordCop'] = True
        else:
            gain = result['gain'] = r.randint(2, 8)
            jour = dt.date.today()
            if (jour.month == 10 and jour.day >= 23) or (jour.month == 11 and jour.day <= 10): # Special Halloween
                # desc = lang_P.forge_msg(lang, "crime event")
                # desc += "{1} {0}".format(gain, lang_P.forge_msg(lang, "crime array", None, True))
                if r.randint(0, 1) == 0:
                    # desc += " :candy:`candy`"
                    result['event'] = 'candy'
                    GF.addInventory(PlayerID, 'candy', gain)
                    GF.addStats(PlayerID, ["Halloween", "Halloween | crime | candy"], gain)
                else:
                    # desc += " :lollipop:`lollipop`"
                    result['event'] = 'lollipop'
                    GF.addInventory(PlayerID, 'lollipop', gain)
                    GF.addStats(PlayerID, ["Halloween", "Halloween | crime | lollipop"], gain)
            else:
                # desc = "{1} {0} :gem:`gems`".format(gain, lang_P.forge_msg(lang, "crime array", None, True))
                sql.addGems(PlayerID, gain)
                GF.addStats(PlayerID, ["crime", "crime | gain"], gain)
                try:
                    sql.addGems(GF.PlayerID_GetGems, -gain) # Vole l'équivalent du crime au bot
                except sqlite3.OperationalError:
                    pass
        sql.updateComTime(PlayerID, "crime")
        lvl.addxp(PlayerID, 1)
        GF.addStats(PlayerID, ["crime", "crime"], 1)
        return {'error': 0, 'etat': 'OK', 'lang': lang, 'result': result}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'couldown': str(GF.couldown("6s"))}


def mine(param):
    """Minez compagnons !!"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    nbMax = 0
    gain = {}

    if sql.spam(PlayerID, GF.couldown("6s"), "mine"):
        if GF.testInvTaille(PlayerID):
            # =====================================
            # Détection du meilleur outil
            # =====================================
            if sql.value(PlayerID, "inventory", "Stock", "Item", "diamond_pickaxe") >= 1:
                nbMax = 600
                outil = "diamond_pickaxe"
                mult = 2.5

            elif sql.value(PlayerID, "inventory", "Stock", "Item", "iron_pickaxe") >= 1:
                nbMax = 250
                outil = "iron_pickaxe"
                mult = 1.5

            elif sql.value(PlayerID, "inventory", "Stock", "Item", "pickaxe") >= 1:
                nbMax = 100
                outil = "pickaxe"
                mult = 1

            sql.updateComTime(PlayerID, "mine")
            lvl.addxp(PlayerID, 1)
            add_item = ""
            if nbMax != 0:
                nbrand = r.randint(1, nbMax)
                # =====================================
                # Gestion de la durabilité de l'outil
                # =====================================
                Durability = GF.durability(PlayerID, outil)
                if Durability:
                    GF.addStats(PlayerID, ["mine", "mine | broken | {}".format(outil)], 1)
                    return {'error': 3, 'etat': 'Item Broken', 'lang': lang, 'broken': outil}

                # =====================================
                # Gestion des résultats
                # =====================================
                # print(nbrand)
                if mult > 1:
                    if nbrand <= int(nbMax*(0.01)):
                        add_item = "ruby"
                        nbrand = r.randint(0, 1)
                    elif nbrand <= int(nbMax*(0.05)):
                        add_item = "emerald"
                        nbrand = r.randint(0, 2)
                    elif nbrand <= int(nbMax*(0.10)):
                        add_item = "diamond"
                        nbrand = r.randint(0, 3)
                    elif nbrand <= int(nbMax*(0.25)):
                        add_item = "gold"
                        nbrand = r.randint(0, 5)
                    elif nbrand <= int(nbMax*(0.50)):
                        add_item = "iron"
                        nbrand = r.randint(1, 8)
                    else:
                        nbrand = 0
                else:
                    if nbrand <= int(nbMax*(0.50)):
                        add_item = "iron"
                        nbrand = r.randint(1, 5)
                    else:
                        nbrand = 0

                if nbrand != 0:
                    nbrand = int(nbrand*mult)
                    GF.addInventory(PlayerID, add_item, nbrand)
                    GF.addStats(PlayerID, ["mine", "mine | item | {}".format(add_item)], nbrand)
                    gain[add_item] = nbrand

                nbcobble = r.randint(1, 10)
                nbcobble = int(nbcobble*mult)
                GF.addInventory(PlayerID, "cobblestone", nbcobble)
                GF.addStats(PlayerID, ["mine", "mine | item | cobblestone"], nbcobble)
                gain["cobblestone"] = nbcobble

                GF.addStats(PlayerID, ["mine", "mine"], 1)
                return {'error': 0, 'etat': 'OK', 'lang': lang, 'gain': gain}

            else:
                return {'error': 4, 'etat': 'NOK', 'lang': lang}

        else:
            return {'error': 2, 'etat': 'NOK', 'lang': lang}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'couldown': str(GF.couldown("6s"))}


def dig(param):
    """Creusons compagnons !!"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    nbMax = 0
    gain = {}

    if sql.spam(PlayerID, GF.couldown("6s"), "dig"):
        if GF.testInvTaille(PlayerID):
            # =====================================
            # Détection du meilleur outil
            # =====================================
            if sql.value(PlayerID, "inventory", "Stock", "Item", "diamond_shovel") >= 1:
                nbMax = 400
                outil = "diamond_shovel"
                mult = 2.5

            elif sql.value(PlayerID, "inventory", "Stock", "Item", "iron_shovel") >= 1:
                nbMax = 200
                outil = "iron_shovel"
                mult = 1.5

            elif sql.value(PlayerID, "inventory", "Stock", "Item", "shovel") >= 1:
                nbMax = 100
                outil = "shovel"
                mult = 1

            sql.updateComTime(PlayerID, "dig")
            lvl.addxp(PlayerID, 1)
            add_item = ""
            if nbMax != 0:
                nbrand = r.randint(1, nbMax)
                # =====================================
                # Gestion de la durabilité de l'outil
                # =====================================
                Durability = GF.durability(PlayerID, outil)
                if Durability:
                    GF.addStats(PlayerID, ["dig", "dig | broken | {}".format(outil)], 1)
                    return {'error': 3, 'etat': 'Item Broken', 'lang': lang, 'broken': outil}

                # =====================================
                # Gestion des résultats
                # =====================================
                # print(nbrand)
                if nbrand <= int(nbMax*(0.25)):
                    add_item = "cacao"
                    nbrand = r.randint(0, 2)
                elif nbrand <= int(nbMax*(0.65)):
                    add_item = "seed"
                    nbrand = r.randint(0, 4)
                elif nbrand <= int(nbMax*(0.95)):
                    add_item = "potato"
                    nbrand = r.randint(1, 4)
                else:
                    nbrand = 0

                if nbrand != 0:
                    nbrand = int(nbrand*mult)
                    GF.addInventory(PlayerID, add_item, nbrand)
                    GF.addStats(PlayerID, ["dig", "dig | item | {}".format(add_item)], nbrand)
                    gain[add_item] = nbrand

                GF.addStats(PlayerID, ["dig", "dig"], 1)
                return {'error': 0, 'etat': 'OK', 'lang': lang, 'gain': gain}

            else:
                return {'error': 4, 'etat': 'NOK', 'lang': lang}
        else:
            return {'error': 2, 'etat': 'NOK', 'lang': lang}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'couldown': str(GF.couldown("6s"))}


def fish(param):
    """Péchons compagnons !!"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    nbMax = 0
    gain = {}

    if sql.spam(PlayerID, GF.couldown("6s"), "fish"):
        if GF.testInvTaille(PlayerID):
            # =====================================
            # Détection du meilleur outil
            # =====================================
            if sql.value(PlayerID, "inventory", "Stock", "Item", "fishingrod") >= 1:
                nbMax = 100
                outil = "fishingrod"
                nbfishhook = sql.value(PlayerID, "inventory", "Stock", "Item", "fishhook")
                if nbfishhook >= 1:
                    mult = r.randint(-1, 5)
                    if mult < 2:
                        mult = 2
                    GF.addInventory(PlayerID, "fishhook", -1)
                    GF.addStats(PlayerID, ["fish", "fish | fishhook utilisé"], 1)
                else:
                    mult = 1

            sql.updateComTime(PlayerID, "fish")
            lvl.addxp(PlayerID, 1)
            add_item = ""
            if nbMax != 0:
                nbrand = r.randint(1, nbMax)
                # =====================================
                # Gestion de la durabilité de l'outil
                # =====================================
                Durability = GF.durability(PlayerID, outil)
                if Durability:
                    GF.addStats(PlayerID, ["fish", "fish | broken | {}".format(outil)], 1)
                    return {'error': 3, 'etat': 'Item Broken', 'lang': lang, 'broken': outil}

                # =====================================
                # Gestion des résultats
                # =====================================
                # print(nbrand)
                if nbrand <= int(nbMax*(0.10)):
                    add_item = "octopus"
                    nbrand = r.randint(0, 1)
                elif nbrand <= int(nbMax*(0.25)):
                    add_item = "blowfish"
                    nbrand = r.randint(0, 3)
                elif nbrand <= int(nbMax*(0.40)):
                    add_item = "tropicalfish"
                    nbrand = r.randint(0, 3)
                elif nbrand <= int(nbMax*(0.90)):
                    add_item = "fish"
                else:
                    nbrand = 0

                if nbrand != 0 or add_item == "fish":
                    if add_item != "fish":
                        nbrand = int(nbrand*mult)
                        GF.addInventory(PlayerID, add_item, nbrand)
                        GF.addStats(PlayerID, ["fish", "fish | item | {}".format(add_item)], nbrand)
                        gain[add_item] = nbrand
                    nb = r.randint(1, 8)
                    nb = int(nb*mult)
                    GF.addInventory(PlayerID, "fish", nb)
                    GF.addStats(PlayerID, ["fish", "fish | item | fish"], nb)
                    gain["fish"] = nb
                else:
                    if mult >= 2:
                        GF.addInventory(PlayerID, "fishhook", 1)
                        GF.addStats(PlayerID, ["fish", "fish | fishhook utilisé"], -1)

                GF.addStats(PlayerID, ["fish", "fish"], 1)
                return {'error': 0, 'etat': 'OK', 'lang': lang, 'gain': gain}

            else:
                return {'error': 4, 'etat': 'NOK', 'lang': lang}
        else:
            return {'error': 2, 'etat': 'NOK', 'lang': lang}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'couldown': str(GF.couldown("6s"))}


def prod_HFC(PlayerID, lang, item, commande, i):
    jour = dt.date.today()
    if commande == "hothouse":
        itemlist = ["seed"]
        if (jour.month == 10 and jour.day >= 26) or (jour.month == 11 and jour.day <= 10):
            itemlist.append("pumpkin")
        outil = "planting_plan"
    elif commande == "ferment":
        itemlist = ["grapes", "wheat"]
        outil = "barrel"
    elif commande == "cooking":
        itemlist = ["potato", "cacao"]
        if (jour.month == 10 and jour.day >= 26) or (jour.month == 11 and jour.day <= 10):
            itemlist.append("pumpkin")
        if (jour.month == 12 and jour.day >= 21) or (jour.month == 1 and jour.day <= 14):
            itemlist.append("chocolate")
        outil = "furnace"

    valueOutil = sql.value(PlayerID, "hfc", "Time, Stock, IDhfc", ["IDhfc", "Type"], [i, commande])
    if valueOutil != 0:
        valueTime = float(valueOutil[0])
        valueItem = valueOutil[1]
    else:
        valueTime = 0
        valueItem = ""

    OutilItem = sql.value(PlayerID, "inventory", "Stock", "Item", item)

    if valueItem == "" and item == "None":
        return {'fct': False, 'item': True}

    elif item in itemlist:
        if commande == "hothouse" and item == "pumpkin":
            prod = GF.param_prod("{0}H".format(item))
        else:
            prod = GF.param_prod(item)
        nbitem = prod["nbitem"]
        gain = prod["gain"]
        couldownMsg = prod["couldownMsg"]
        if valueTime == 0:
            if OutilItem >= nbitem:
                GF.updateHFC(PlayerID, commande, i, str(t.time()), item)
                GF.addInventory(PlayerID, item, -nbitem)
                GF.addStats(PlayerID, [commande, "{1} | plant | item | {0}".format(item, commande)], nbitem)
        return {'fct': 'hfc', 'item': item, 'nbitem': nbitem, 'time': valueTime, 'couldownMsg': couldownMsg, 'OutilItem': OutilItem, 'valueItem': valueItem, 'gain': gain}

    elif item == "None":
        prod = GF.param_prod(valueItem)
        nbitem = prod["nbitem"]
        gain = prod["gain"]
        couldown = prod["couldown"]
        nbgain = prod["nbgain"]

        EndTime = float(valueTime)
        InstantTime = t.time()
        time = EndTime - (InstantTime-couldown)
        if time <= 0:
            GF.updateHFC(PlayerID, commande, i, 0, "")
            GF.addInventory(PlayerID, gain, nbgain)
            GF.addStats(PlayerID, [commande, "{1} | harvest | item | {0}".format(gain, commande)], nbgain)

            lvl.addxp(PlayerID, 1)
            if i > 1:
                GF.durability(PlayerID, outil)

        return {'fct': 'time', 'item': valueItem, 'time': time, 'gain': gain, 'nbgain': nbgain}
    else:
        return {'fct': False, 'item': False}


def hothouse(param):
    """**{seed/pumpkin}** | Plantons compagnons !!"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    item = param["item"]
    result = dict()
    i = 1
    max = 50

    if sql.spam(PlayerID, GF.couldown("4s"), "hothouse"):
        sql.updateComTime(PlayerID, "hothouse")
        nboutil = sql.value(PlayerID, "inventory", "Stock", "Item", "planting_plan") + 1
        if nboutil >= max:
            nboutil = max
        while i <= nboutil+1:
            # print(i)
            result[i] = prod_HFC(PlayerID, lang, item, "hothouse", i)
            i += 1
        return {'error': 0, 'etat': 'OK', 'lang': lang, 'nboutil': nboutil, 'result': result}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'couldown': str(GF.couldown("6s"))}


def ferment(param):
    """**{grapes/wheat}** | Cave de fermentation. Alcool illimité !!"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    item = param["item"]
    result = dict()
    i = 1
    max = 20

    if sql.spam(PlayerID, GF.couldown("4s"), "ferment"):
        sql.updateComTime(PlayerID, "ferment")
        nboutil = sql.value(PlayerID, "inventory", "Stock", "Item", "barrel") + 1
        if nboutil >= max:
            nboutil = max
        while i <= nboutil:
            result[i] = prod_HFC(PlayerID, lang, item, "ferment", i)
            i += 1
        return {'error': 0, 'etat': 'OK', 'lang': lang, 'nboutil': nboutil, 'result': result}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'couldown': str(GF.couldown("6s"))}


def cooking(param):
    """**{potato/pumpkin/chocolate}** | Cuisinons compagnons !!"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    item = param["item"]
    result = dict()
    i = 1
    jour = dt.date.today()
    max = 20
    if item == "pumpkin":
        if not ((jour.month == 10 and jour.day >= 26) or (jour.month == 11 and jour.day <= 10)):
            # msg["desc"] = lang_P.forge_msg(lang, "cooking", None, False, 11)
            return {'error': 1, 'etat': 'NOK', 'lang': lang, 'event': "halloween"}
    elif item == "chocolate":
        if not ((jour.month == 12 and jour.day >= 21) or (jour.month == 1 and jour.day <= 14)):
            # msg["desc"] = lang_P.forge_msg(lang, "cooking", None, False, 12)
            return {'error': 1, 'etat': 'NOK', 'lang': lang, 'event': "christmas"}

    if sql.spam(PlayerID, GF.couldown("4s"), "cooking"):
        sql.updateComTime(PlayerID, "cooking")
        nboutil = sql.value(PlayerID, "inventory", "Stock", "Item", "furnace") + 1
        if nboutil >= max:
            nboutil = max
        while i <= nboutil:
            result[i] = prod_HFC(PlayerID, lang, item, "cooking", i)
            i += 1
        return {'error': 0, 'etat': 'OK', 'lang': lang, 'nboutil': nboutil, 'result': result}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'couldown': str(GF.couldown("6s"))}
