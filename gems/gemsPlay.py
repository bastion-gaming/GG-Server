import random as r
import time as t
import datetime as dt
from DB import SQLite as sql
import sqlite3
from gems import gemsFonctions as GF
from core import level as lvl


def daily(param):
    """Récupère ta récompense journalière!"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    # =======================================================================
    # Initialisation des variables générales de la fonction
    # =======================================================================
    DailyTime = sql.valueAtNumber(PlayerID, "DailyTime", "daily")
    DailyMult = sql.valueAtNumber(PlayerID, "DailyMult", "daily")
    jour = dt.date.today()
    msg = []
    # =======================================================================
    # Détermination du daily
    # =======================================================================
    if DailyTime == str(jour - dt.timedelta(days=1)):
        sql.updateField(PlayerID, "DailyTime", str(jour), "daily")
        sql.updateField(PlayerID, "DailyMult", DailyMult + 1, "daily")

        # Un = 200 × (2.5)^(n-1)
        if DailyMult >= 30:
            f = 200 * (2.5**((DailyMult//30)-1))
            bonus = int(f)
        else:
            bonus = 125
        gain = 100 + bonus*DailyMult
        sql.addGems(PlayerID, gain)
        desc = "Récompense journalière! Tu as gagné 100:gem:`gems`"
        desc += "\nNouvelle série: `{}`, Bonus: {} :gem:`gems`".format(DailyMult, bonus*DailyMult)
        lvl.addxp(PlayerID, 10*(DailyMult/2), "gems")
        if DailyMult % 30 == 0:
            m = (DailyMult//30)*5
            sql.addSpinelles(PlayerID, m)
            desc += "\nBravo pour c'est {0} jours consécutifs :confetti_ball:! Tu as mérité {1}<:spinelle:{2}>`spinelles`".format(DailyMult, m, "{idmoji[spinelle]}")

    elif DailyTime == str(jour):
        desc = "Tu as déja reçu ta récompense journalière aujourd'hui. Reviens demain pour gagner plus de :gem:`gems`"
    else:
        sql.add(PlayerID, "DailyMult", 1, "daily")
        sql.add(PlayerID, "DailyTime", str(jour), "daily")
        desc = "Récompense journalière! Tu as gagné 100 :gem:`gems`"
        lvl.addxp(PlayerID, 10, "gems")
    msg.append("OK")
    msg.append(desc)
    return msg


def bank(param):
    """Compte épargne"""
    # =======================================================================
    # Initialistation des variables générales de la fonction
    # =======================================================================
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    ARG = param["ARG"]
    ARG2 = param["ARG2"]
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []

    jour = dt.date.today()
    if ARG != "None":
        mARG = ARG.lower()
    else:
        mARG = "bal"
    for c in GF.objetOutil:
        if c.type == "bank":
            Taille = c.poids
    desc = ""
    solde = sql.valueAt(PlayerID, "Solde", "bank")
    if solde == 0:
        sql.add(PlayerID, "SoldeMax", Taille, "bank")
    # =======================================================================
    # Affiche le menu principal de la banque
    # !bank bal <nom d'un joueur> permet de visualiser l'état de la banque de ce joueur
    # =======================================================================
    if mARG == "bal":
        if sql.spam(PlayerID, GF.couldown_4s, "bank_bal", "gems"):
            msg.append("bal")
            if ARG2 != "None":
                ID = sql.get_SuperID(sql.nom_ID(param["ARG2"]), param["name_pl"])
                PlayerID = sql.get_PlayerID(ID, "gems")
            solde = sql.valueAtNumber(PlayerID, "Solde", "bank")
            soldeMax = sql.valueAtNumber(PlayerID, "SoldeMax", "bank")
            if soldeMax == 0:
                soldeMax = Taille
            desc = "{} / {} :gem:`gems`\n".format(solde, soldeMax)
            msg.append(desc)

            desc = "bank **bal** *[name]* | Permet de connaitre la balance d'un utilisateur"
            desc += "\nbank **add** *[+/- nombre]* | Permet d'ajouter ou d'enlever des :gem:`gems` de son compte épargne"
            desc += "\nbank **saving** | Permet de calculer son épargne (utilisable toute les 4h)"
            desc += "\n\nLe prix de la <:gem_{0}:{1}>`{0}` dépend du plafond du compte".format("bank_upgrade", "{idmoji[gem_bank_upgrade]}")

            msg.append(desc)
            sql.updateComTime(PlayerID, "bank_bal", "gems")
        else:
            desc = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
            msg.append("couldown")
            msg.append(desc)
        return msg
    # =======================================================================
    # Ajoute ou enlève des Gems sur le compte épargne
    # un nombre positif ajoute des Gems
    # un nombre négatif enlève des Gems
    # =======================================================================
    elif mARG == "add":
        if sql.spam(PlayerID, GF.couldown_4s, "bank_add", "gems"):
            if ARG2 != None:
                ARG2 = int(ARG2)
                gems = sql.valueAtNumber(PlayerID, "gems", "gems")
                solde = sql.valueAtNumber(PlayerID, "Solde", "bank")
                soldeMax = sql.valueAtNumber(PlayerID, "SoldeMax", "bank")
                if soldeMax == 0:
                    soldeMax = Taille

                if ARG2 <= gems:
                    soldeNew = solde + ARG2
                    if soldeNew > soldeMax:
                        ARG2 = ARG2 - (soldeNew - soldeMax)
                        desc = "Plafond de {} :gem:`gems` du compte épargne atteint\n".format(soldeMax)
                    elif soldeNew < 0:
                        desc = "Le solde de ton compte épargne ne peux être négatif.\nSolde du compte: {} :gem:`gems`".format(solde)
                        msg.append("NOK")
                        msg.append(desc)
                        return msg
                    nbgm = -1*ARG2
                    sql.addGems(PlayerID, nbgm)
                    sql.add(PlayerID, "solde", ARG2, "bank")
                    desc += "Ton compte épargne a été crédité de {} :gem:`gems`".format(ARG2)
                    desc += "\nNouveau solde: {} :gem:`gems`".format(sql.valueAtNumber(PlayerID, "Solde", "bank"))
                    msg.append("add")
                    sql.updateComTime(PlayerID, "bank_add", "gems")
                else:
                    desc = "Tu n'as pas assez de :gem:`gems` pour épargner cette somme"
                    msg.append("NOK")
            else:
                desc = "Il manque le nombre de :gem:`gems` à ajouter sur votre compte épargne"
                msg.append("NOK")
        else:
            desc = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
            msg.append("couldown")
        msg.append(desc)
        return msg
    # =======================================================================
    # Fonction d'épargne
    # L'intéret est de 20% avec un bonus de 1% pour chanque bank_upgrade possédée
    # =======================================================================
    elif mARG == "saving":
        if sql.spam(PlayerID, GF.couldown_4h, "bank_saving", "gems"):
            solde = sql.valueAtNumber(PlayerID, "Solde", "bank")
            soldeMax = sql.valueAtNumber(PlayerID, "SoldeMax", "bank")
            if soldeMax == 0:
                soldeMax = Taille
            soldeMult = soldeMax/Taille
            pourcentage = 0.150 + soldeMult*0.002
            if pourcentage > 0.6:
                pourcentage = 0.6
            soldeAdd = pourcentage*solde
            soldeTaxe = GF.taxe(soldeAdd, 0.1)
            soldeAdd = soldeTaxe[1]
            sql.add(PlayerID, "solde", int(soldeAdd), "bank")
            desc = "Tu as épargné {} :gem:`gems`\n".format(int(soldeAdd))
            soldeNew = solde + soldeAdd
            if soldeNew > soldeMax:
                soldeMove = soldeNew - soldeMax
                nbgm = -1 * soldeMove
                sql.addGems(PlayerID, int(soldeMove))
                sql.add(PlayerID, "solde", int(nbgm), "bank")
                desc += "Plafond de {} :gem:`gems` du compte épargne atteint\nTon épargne a été tranférée sur ton compte principal\n\n".format(soldeMax)
            desc += "Nouveau solde: {} :gem:`gems`".format(sql.valueAtNumber(PlayerID, "Solde", "bank"))

            D = r.randint(0, 20)
            if D == 20 or D == 0:
                sql.add(PlayerID, "lootbox_raregems", 1, "inventory")
                desc += "\nTu as trouvé une **Loot Box Gems Rare**! Utilise la commande `boxes open raregems` pour l'ouvrir"
            elif D >= 9 and D <= 11:
                sql.add(PlayerID, "lootbox_commongems", 1, "inventory")
                desc += "\nTu as trouvé une **Loot Box Gems Common**! Utilise la commande `boxes open commongems` pour l'ouvrir"
            elif (jour.month == 12 and jour.day >= 22) and (jour.month == 12 and jour.day <= 25):
                nbgift = 1
                sql.add(PlayerID, "lootbox_gift", nbgift, "inventory")
                desc += "\n\nTu as trouvé {} :gift:`cadeau de Noël (gift)`".format(nbgift)
            elif (jour.month == 12 and jour.day >= 30) or (jour.month == 1 and jour.day <= 2):
                nbgift = 1
                sql.add(PlayerID, "lootbox_gift", nbgift, "inventory")
                desc += "\n\nTu as trouvé {} :gift:`cadeau de la nouvelle année (gift)`:confetti_ball:".format(nbgift)

            try:
                sql.addGems(sql.get_PlayerID(sql.get_SuperID(GF.idBaBot, "discord")), int(soldeTaxe[0]))
            except:
                print("Babot ne fait pas parti de la DB")
            sql.updateComTime(PlayerID, "bank_saving", "gems")
            lvl.addxp(PlayerID, 4, "gems")
        else:
            ComTime = sql.valueAtNumber(PlayerID, "bank_saving", "gems_com_time")
            time = float(ComTime) - (t.time()-GF.couldown_4h)
            timeH = int(time / 60 / 60)
            time = time - timeH * 3600
            timeM = int(time / 60)
            timeS = int(time - timeM * 60)
            desc = "Il te faut attendre :clock2:`{}h {}m {}s` avant d'épargner à nouveau !".format(timeH, timeM, timeS)
        msg.append("saving")
        msg.append(desc)
        return msg


def stealing(param):
    """**[nom]** | Vole des :gem:`gems` aux autres joueurs!"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    name = param["name"]
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []
    if sql.spam(PlayerID, GF.couldown_14h, "stealing", "gems") and name is not None:
        ID_Vol = sql.get_PlayerID(sql.get_SuperID(sql.nom_ID(name), param["name_pl"]))
        # Calcul du pourcentage
        if ID_Vol == sql.get_PlayerID(sql.get_SuperID(GF.idBaBot, "discord")) or ID_Vol == sql.get_PlayerID(sql.get_SuperID(GF.idBaBot, "discord")):
            R = r.randint(1, 6)
        else:
            R = "05"
        P = float("0.0{}".format(R))
        try:
            Solde = sql.valueAtNumber(ID_Vol, "gems", "gems")
            gain = int(Solde*P)
            if r.randint(0, 9) == 0:
                sql.add(PlayerID, "DiscordCop Arrestation", 1, "statgems")
                if int(sql.addGems(PlayerID, int(gain/4))) >= 100:
                    desc = "Vous avez été attrapés par un DiscordCop vous avez donc payé une amende de **{}** :gem:`gems`".format(int(gain/4))
                else:
                    sql.updateField(PlayerID, "gems", 100, "gems")
                    desc = "Vous avez été attrapés par un DiscordCop mais vous avez trop peu de :gem:`gems` pour payer l'intégralité de l'amende! Votre compte est maintenant de 100 :gem:`gems`"
            else:
                sql.addGems(PlayerID, gain)
                sql.addGems(ID_Vol, -gain)
                # Message
                desc = "Tu viens de voler {n} :gem:`gems` à {nom}".format(n=gain, nom=name)
                print("Gems >> PlayerID {author} viens de voler {n} gems à {nom}".format(n=gain, nom=ID_Vol, author=PlayerID))
            sql.updateComTime(PlayerID, "stealing", "gems")
            lvl.addxp(PlayerID, 1, "gems")
        except:
            desc = "Ce joueur est introuvable!"
    else:
        ComTime = sql.valueAtNumber(PlayerID, "stealing", "gems_com_time")
        time = float(ComTime) - (t.time()-GF.couldown_14h)
        timeH = int(time / 60 / 60)
        time = time - timeH * 3600
        timeM = int(time / 60)
        timeS = int(time - timeM * 60)
        desc = "Il te faut attendre :clock2:`{}h {}m {}s` avant de pourvoir voler des :gem:`gems` à nouveau!".format(timeH, timeM, timeS)
        if sql.spam(PlayerID, GF.couldown_14h, "stealing", "gems"):
            desc = "Tu peux voler des :gem:`gems`"
    msg.append("OK")
    msg.append(desc)
    return msg


def crime(param):
    """Commets un crime et gagne des :gem:`gems` Attention au DiscordCop!"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []
    if sql.spam(PlayerID, GF.couldown_6s, "crime", "gems"):
        # si 10 sec c'est écoulé depuis alors on peut en  faire une nouvelle
        if r.randint(0, 9) == 0:
            sql.add(PlayerID, "DiscordCop Arrestation", 1, "statgems")
            if int(sql.addGems(PlayerID, -10)) >= 0:
                desc = "Vous avez été attrapés par un DiscordCop vous avez donc payé une amende de 10 :gem:`gems`"
            else:
                desc = "Vous avez été attrapés par un DiscordCop mais vous avez trop peu de :gem:`gems` pour payer une amende"
        else:
            gain = r.randint(2, 8)
            jour = dt.date.today()
            if (jour.month == 10 and jour.day >= 23) or (jour.month == 11 and jour.day <= 10): # Special Halloween
                desc = "**Halloween** | Des bonbons ou un sort ?\n"
                desc += GF.message_crime[r.randint(0, 3)]+" "+str(gain)
                if r.randint(0, 1) == 0:
                    desc += " :candy:`candy`"
                    sql.add(PlayerID, "candy", gain, "inventory")
                else:
                    desc += " :lollipop:`lollipop`"
                    sql.add(PlayerID, "lollipop", gain, "inventory")
            else:
                desc = "{1} {0} :gem:`gems`".format(gain, GF.message_crime[r.randint(0, 3)])
                sql.addGems(PlayerID, gain)
                try:
                    sql.addGems(sql.get_PlayerID(sql.get_SuperID(GF.idBaBot, param["name_pl"])), -gain) # Vole l'équivalent du crime au bot
                except sqlite3.OperationalError:
                    pass
                if (jour.month == 12 and jour.day >= 22) and (jour.month == 12 and jour.day <= 25):
                    if r.randint(0, 10) == 0:
                        nbgift = r.randint(1, 3)
                        sql.add(PlayerID, "lootbox_gift", nbgift, "inventory")
                        desc += "\n\nTu as trouvé {} :gift:`cadeau de Noël (gift)`".format(nbgift)
                elif (jour.month == 12 and jour.day >= 30) or (jour.month == 1 and jour.day <= 2):
                    if r.randint(0, 10) == 0:
                        nbgift = r.randint(1, 3)
                        sql.add(PlayerID, "lootbox_gift", nbgift, "inventory")
                        desc += "\n\nTu as trouvé {} :gift:`cadeau de la nouvelle année (gift)`:confetti_ball:".format(nbgift)
        sql.updateComTime(PlayerID, "crime", "gems")
        lvl.addxp(PlayerID, 1, "gems")
        msg.append("OK")
    else:
        desc = "Il faut attendre "+str(GF.couldown_6s)+" secondes entre chaque commande !"
        msg.append("couldown")
    msg.append(desc)
    return msg
