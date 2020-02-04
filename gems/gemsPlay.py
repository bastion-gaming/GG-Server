import random as r
import time as t
import datetime as dt
from DB import SQLite as sql
import sqlite3
from gems import gemsFonctions as GF, gemsEvent as GE
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
    Lang = sql.get_lang(param["IDGuild"])
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
            # sql.addSpinelles(PlayerID, m)
            sql.addGems(PlayerID, m*250000)
            # desc += "\nBravo pour c'est {0} jours consécutifs :confetti_ball:! Tu as mérité {1}<:spinelle:{2}>`spinelles`".format(DailyMult, m, "{idmoji[spinelle]}")
            desc += "\nBravo pour c'est {0} jours consécutifs :confetti_ball:! Tu as mérité {1}:gem:`gems`".format(DailyMult, m*250000)

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
    Lang = sql.get_lang(param["IDGuild"])

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

            # =====================================
            # Bonus
            # =====================================
            desc += GE.lootbox(PlayerID)
            desc += GE.gift(PlayerID)

            try:
                sql.addGems(GF.PlayerID_GetGems, int(soldeTaxe[0]))
            except:
                print("Le bot ne fait pas parti de la DB")
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
    Lang = sql.get_lang(param["IDGuild"])

    if sql.valueAtNumber(GF.PlayerID_GetGems, "DailyMult", "daily") == 1:
        desc = ""
    else:
        if sql.spam(PlayerID, GF.couldown_14h, "stealing", "gems") and name is not None:
            ID_Vol = sql.get_PlayerID(sql.get_SuperID(sql.nom_ID(name), param["name_pl"]))
            # Calcul du pourcentage
            if ID_Vol == GF.PlayerID_GetGems or ID_Vol == GF.PlayerID_Babot:
                R = r.randint(1, 6)
            else:
                R = "05"
            P = float("0.0{}".format(R))
            try:
                Solde = sql.valueAtNumber(ID_Vol, "gems", "gems")
                gain = int(Solde*P)
                if gain != 0:
                    if r.randint(0, 9) == 0:
                        sql.add(PlayerID, "DiscordCop Arrestation", 1, "statgems")
                        if int(sql.addGems(PlayerID, int(gain/4))) >= 100:
                            desc = "Vous avez été attrapés par un DiscordCop vous avez donc payé une amende de **{}** :gem:`gems`".format(int(gain/4))
                        else:
                            sql.updateField(PlayerID, "gems", 0, "gems")
                            desc = "Vous avez été attrapés par un DiscordCop mais vous avez trop peu de :gem:`gems` pour payer l'intégralité de l'amende! Votre compte est maintenant de 0 :gem:`gems`"
                    else:
                        sql.addGems(PlayerID, gain)
                        sql.addGems(ID_Vol, -gain)
                        # Message
                        desc = "Tu viens de voler {n} :gem:`gems` à {nom}".format(n=gain, nom=name)
                        print("Gems >> PlayerID {author} viens de voler {n} gems à {nom}".format(n=gain, nom=ID_Vol, author=PlayerID))
                    sql.updateComTime(PlayerID, "stealing", "gems")
                    lvl.addxp(PlayerID, 1, "gems")
                else:
                    desc = "Tu es un piètre voleur de :gem:`gems`"
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
    Lang = sql.get_lang(param["IDGuild"])

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
                    sql.addGems(GF.PlayerID_GetGems, -gain) # Vole l'équivalent du crime au bot
                except sqlite3.OperationalError:
                    pass
                desc += GE.gift(PlayerID)
        sql.updateComTime(PlayerID, "crime", "gems")
        lvl.addxp(PlayerID, 1, "gems")
        msg.append("OK")
    else:
        desc = "Il faut attendre "+str(GF.couldown_6s)+" secondes entre chaque commande !"
        msg.append("couldown")
    msg.append(desc)
    return msg


def gamble(param):
    """**[valeur]** | Avez vous l'ame d'un parieur ?"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    valeur = param["valeur"]
    msg = []
    valeur = int(valeur)
    Lang = sql.get_lang(param["IDGuild"])

    gems = sql.valueAtNumber(PlayerID, "gems", "gems")
    if valeur < 0:
        desc = ":no_entry: Anti-cheat! Je vous met un amende de 100 :gem:`gems` pour avoir essayé de tricher !"
        sql.add(PlayerID, "DiscordCop Amende", 1, "statgems")
        if gems > 100 :
            sql.addGems(PlayerID, -100)
        else :
            sql.addGems(PlayerID, -gems)
        msg.append("anticheat")
        msg.append(desc)
        return msg

    elif valeur > 0 and gems >= valeur:
        if sql.spam(PlayerID, GF.couldown_8s, "gamble", "gems"):
            if r.randint(0, 3) == 0:
                gain = valeur*3
                # l'espérence est de 0 sur la gamble
                desc = "{1} {0} :gem:`gems`".format(gain, GF.message_gamble[r.randint(0, 4)])
                sql.add(PlayerID, "Gamble Win", 1, "statgems")
                for x in GF.objetTrophy:
                    if x.nom == "Gamble Jackpot":
                        jackpot = x.mingem
                    elif x.nom == "Super Gamble Jackpot":
                        superjackpot = x.mingem
                    elif x.nom == "Hyper Gamble Jackpot":
                        hyperjackpot = x.mingem
                if gain >= jackpot and gain < superjackpot:
                    sql.add(PlayerID, "Gamble Jackpot", 1, "trophy")
                    desc += "\nFélicitation! Tu as l'ame d'un parieur, nous t'offrons le prix :trophy:`Gamble Jackpot`."
                elif gain >= superjackpot and gain < hyperjackpot:
                    sql.add(PlayerID, "Super Gamble Jackpot", 1, "trophy")
                    desc += "\nFélicitation! Tu as l'ame d'un parieur, nous t'offrons le prix :trophy::trophy:`Super Gamble Jackpot`."
                elif gain >= hyperjackpot:
                    sql.add(PlayerID, "Hyper Gamble Jackpot", 1, "trophy")
                    desc += "\nFélicitation! Tu as l'ame d'un parieur, nous t'offrons le prix :trophy::trophy::trophy:`Hyper Gamble Jackpot`."
                sql.addGems(PlayerID, gain)
                # =====================================
                # Bonus
                # =====================================
                desc += GE.lootbox(PlayerID)
            else:
                val = 0-valeur
                sql.addGems(PlayerID, val)
                sql.addGems(GF.PlayerID_GetGems, int(valeur))
                desc = "Dommage tu as perdu {} :gem:`gems`".format(valeur)

            sql.updateComTime(PlayerID, "gamble", "gems")
            lvl.addxp(PlayerID, 1, "gems")
            msg.append("OK")
        else:
            desc = "Il faut attendre "+str(GF.couldown_8s)+" secondes entre chaque commande !"
            msg.append("couldown")
    elif gems < valeur:
        desc = "Tu n'as pas assez de :gem:`gems` en banque"
        msg.append("NOK")
    else:
        desc = "La valeur rentré est incorrect"
        msg.append("NOK")
    msg.append(desc)
    return msg


def mine(param):
    """Minez compagnons !!"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []
    nbMax = 0
    desc = ""
    Lang = sql.get_lang(param["IDGuild"])

    if sql.spam(PlayerID, GF.couldown_6s, "mine", "gems"):
        if GF.testInvTaille(PlayerID):
            # =====================================
            # Détection du meilleur outil
            # =====================================
            if sql.valueAtNumber(PlayerID, "diamond_pickaxe", "inventory") >= 1:
                nbMax = 800
                outil = "diamond_pickaxe"
                mult = 5

            elif sql.valueAtNumber(PlayerID, "iron_pickaxe", "inventory") >= 1:
                nbMax = 300
                outil = "iron_pickaxe"
                mult = 2

            elif sql.valueAtNumber(PlayerID, "pickaxe", "inventory") >= 1:
                nbMax = 100
                outil = "pickaxe"
                mult = 1

            nbrand = r.randint(1, nbMax)
            add_item = ""
            if nbMax != 0:
                # =====================================
                # Gestion de la durabilité de l'outil
                # =====================================
                Durability = sql.valueAtNumber(PlayerID, outil, "durability")
                if Durability == 0:
                    sql.add(PlayerID, outil, -1, "inventory")
                    if sql.valueAtNumber(PlayerID, outil, "inventory") > 1:
                        for c in GF.objetOutil:
                            if c.nom == outil:
                                sql.add(PlayerID, c.nom, c.durabilite, "durability")
                    desc = "Pas de chance tu as cassé ta <:gem_{nom}:{idmoji}>`{nom}` !".format(nom = outil, idmoji = "{idmoji[gem_" + outil + "]}")
                    msg.append("OK")
                    msg.append(desc)
                    return msg
                else :
                    sql.add(PlayerID, outil, -1, "durability")

                # =====================================
                # Gestion des résultats
                # =====================================
                print(nbrand)
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
                        add_item = "cobblestone"
                        nbrand = r.randint(1, 40)
                else:
                    if nbrand <= int(nbMax*(0.50)):
                        add_item = "iron"
                        nbrand = r.randint(1, 6)
                    else:
                        add_item = "cobblestone"
                        nbrand = r.randint(1, 40)

                if nbrand != 0:
                    sql.add(PlayerID, add_item, nbrand*mult, "inventory")
                    desc = "Tu as obtenu {nb} <:gem_{item}:{idmoji}>`{item}`".format(nb = nbrand*mult, item = add_item, idmoji = "{idmoji[gem_" + add_item + "]}")
                if add_item != "cobblestone":
                    nbcobble = r.randint(1, 32)
                    sql.add(PlayerID, "cobblestone", nbcobble*mult, "inventory")
                    desc += "\nTu as obtenu {} bloc de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble*mult, "{idmoji[gem_cobblestone]}")

                # =====================================
                # Bonus
                # =====================================
                desc += GE.lootbox(PlayerID)
                desc += GE.gift(PlayerID)

            else:
                desc = "Il faut acheter ou forger une pioche pour miner!"

            sql.updateComTime(PlayerID, "mine", "gems")
            lvl.addxp(PlayerID, 1, "gems")
            msg.append("OK")
        else:
            desc = "Ton inventaire est plein"
            msg.append("NOK")
    else:
        desc = "Il faut attendre " + str(GF.couldown_6s) + " secondes entre chaque commande !"
        msg.append("couldown")
    msg.append(desc)
    return msg


def dig(param):
    """Creusons compagnons !!"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []
    nbMax = 0
    desc = ""
    Lang = sql.get_lang(param["IDGuild"])

    if sql.spam(PlayerID, GF.couldown_6s, "dig", "gems"):
        if GF.testInvTaille(PlayerID):
            # =====================================
            # Détection du meilleur outil
            # =====================================
            if sql.valueAtNumber(PlayerID, "diamond_shovel", "inventory") >= 1:
                nbMax = 400
                outil = "diamond_shovel"
                mult = 5

            elif sql.valueAtNumber(PlayerID, "iron_shovel", "inventory") >= 1:
                nbMax = 200
                outil = "iron_shovel"
                mult = 2

            elif sql.valueAtNumber(PlayerID, "shovel", "inventory") >= 1:
                nbMax = 100
                outil = "shovel"
                mult = 1

            nbrand = r.randint(1, nbMax)
            add_item = ""
            if nbMax != 0:
                # =====================================
                # Gestion de la durabilité de l'outil
                # =====================================
                Durability = sql.valueAtNumber(PlayerID, outil, "durability")
                if Durability == 0:
                    sql.add(PlayerID, outil, -1, "inventory")
                    if sql.valueAtNumber(PlayerID, outil, "inventory") > 1:
                        for c in GF.objetOutil:
                            if c.nom == outil:
                                sql.add(PlayerID, c.nom, c.durabilite, "durability")
                    desc = "Pas de chance tu as cassé ta <:gem_{nom}:{idmoji}>`{nom}` !".format(nom = outil, idmoji = "{idmoji[gem_" + outil + "]}")
                    msg.append("OK")
                    msg.append(desc)
                    return msg
                else :
                    sql.add(PlayerID, outil, -1, "durability")

                # =====================================
                # Gestion des résultats
                # =====================================
                print(nbrand)
                if nbrand <= int(nbMax*(0.25)):
                    add_item = "cacao"
                    nbrand = r.randint(0, 3)
                elif nbrand <= int(nbMax*(0.65)):
                    add_item = "seed"
                    nbrand = r.randint(0, 6)
                elif nbrand <= int(nbMax*(0.80)):
                    add_item = "potato"
                    nbrand = r.randint(2, 5)
                else:
                    nbrand = 0

                if nbrand != 0:
                    sql.add(PlayerID, add_item, nbrand*mult, "inventory")
                    desc = "Tu as obtenu {nb} <:gem_{item}:{idmoji}>`{item}`".format(nb = nbrand*mult, item = add_item, idmoji = "{idmoji[gem_" + add_item + "]}")
                else:
                    desc = "Tu as creusé toute la journée pour ne trouver que de la terre."

                # =====================================
                # Bonus
                # =====================================
                desc += GE.lootbox(PlayerID)
                desc += GE.gift(PlayerID)

            else:
                desc = "Il faut acheter ou forger une pelle pour creuser!"

            sql.updateComTime(PlayerID, "dig", "gems")
            lvl.addxp(PlayerID, 1, "gems")
            msg.append("OK")
        else:
            desc = "Ton inventaire est plein"
            msg.append("NOK")
    else:
        desc = "Il faut attendre " + str(GF.couldown_6s) + " secondes entre chaque commande !"
        msg.append("couldown")
    msg.append(desc)
    return msg


def fish(param):
    """Péchons compagnons !!"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []
    nbMax = 0
    desc = ""
    Lang = sql.get_lang(param["IDGuild"])

    if sql.spam(PlayerID, GF.couldown_6s, "fish", "gems"):
        if GF.testInvTaille(PlayerID):
            # =====================================
            # Détection du meilleur outil
            # =====================================
            if sql.valueAtNumber(PlayerID, "fishingrod", "inventory") >= 1:
                nbMax = 100
                outil = "fishingrod"
                nbfishhook = sql.valueAtNumber(PlayerID, "fishhook", "inventory")
                if nbfishhook >= 1:
                    mult = r.randint(-1, 5)
                    if mult < 2:
                        mult = 2
                    sql.add(PlayerID, "fishhook", -1, "inventory")
                else:
                    mult = 1

            nbrand = r.randint(1, nbMax)
            add_item = ""
            if nbMax != 0:
                # =====================================
                # Gestion de la durabilité de l'outil
                # =====================================
                Durability = sql.valueAtNumber(PlayerID, outil, "durability")
                if Durability == 0:
                    sql.add(PlayerID, outil, -1, "inventory")
                    if sql.valueAtNumber(PlayerID, outil, "inventory") > 1:
                        for c in GF.objetOutil:
                            if c.nom == outil:
                                sql.add(PlayerID, c.nom, c.durabilite, "durability")
                    desc = "Pas de chance tu as cassé ta <:gem_{nom}:{idmoji}>`{nom}` !".format(nom = outil, idmoji = "{idmoji[gem_" + outil + "]}")
                    msg.append("OK")
                    msg.append(desc)
                    return msg
                else :
                    sql.add(PlayerID, outil, -1, "durability")

                # =====================================
                # Gestion des résultats
                # =====================================
                print(nbrand)
                if nbrand <= int(nbMax*(0.10)):
                    add_item = "octopus"
                    nbrand = r.randint(0, 1)
                elif nbrand <= int(nbMax*(0.25)):
                    add_item = "blowfish"
                    nbrand = r.randint(1, 4)
                elif nbrand <= int(nbMax*(0.40)):
                    add_item = "tropicalfish"
                    nbrand = r.randint(1, 4)
                elif nbrand <= int(nbMax*(0.90)):
                    add_item = "fish"
                    nbrand = r.randint(1, 16)
                else:
                    nbrand = 0

                if nbrand != 0:
                    sql.add(PlayerID, add_item, nbrand*mult, "inventory")
                    desc = "Tu as obtenu {nb} <:gem_{item}:{idmoji}>`{item}`".format(nb = nbrand*mult, item = add_item, idmoji = "{idmoji[gem_" + add_item + "]}")
                    if add_item != "fish":
                        nb = r.randint(1, 16)
                        sql.add(PlayerID, "fish", nb*mult, "inventory")
                        desc += "\nTu as obtenu {} <:gem_fish:{}>`fish`".format(nb*mult, "{idmoji[gem_fish]}")
                else:
                    desc = "Pas de poisson pour toi aujourd'hui :cry:"
                    if mult >= 2:
                        sql.add(PlayerID, "fishhook", 1, "inventory")

                # =====================================
                # Bonus
                # =====================================
                desc += GE.lootbox(PlayerID)
                desc += GE.gift(PlayerID)

            else:
                desc = "Il te faut une <:gem_fishingrod:{}>`fishingrod` pour pécher, tu en trouvera une au marché !".format("{idmoji[fishingrod]}")

            sql.updateComTime(PlayerID, "fish", "gems")
            lvl.addxp(PlayerID, 1, "gems")
            msg.append("OK")
        else:
            desc = "Ton inventaire est plein"
            msg.append("NOK")
    else:
        desc = "Il faut attendre " + str(GF.couldown_6s) + " secondes entre chaque commande !"
        msg.append("couldown")
    msg.append(desc)
    return msg


def slots(param):
    """**[mise]** | La machine à sous, la mise minimum est de 10 :gem:`gems`"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    imise = param["imise"]
    msg = []
    Lang = sql.get_lang(param["IDGuild"])

    gems = sql.valueAtNumber(PlayerID, "gems", "gems")
    misemax = 200
    if imise != "None":
        if int(imise) < 0:
            desc = ":no_entry: Anti-cheat! Je vous met un amende de 100 :gem:`gems` pour avoir essayé de tricher !"
            lvl.addxp(PlayerID, -10, "gems")
            sql.add(PlayerID, "DiscordCop Amende", 1, "statgems")
            if gems > 100 :
                sql.addGems(PlayerID, -100)
            else :
                sql.addGems(PlayerID, -gems)
            msg.append("anticheat")
            msg.append(desc)
            return msg
        elif int(imise) < 10:
            mise = 10
        elif int(imise) > misemax:
            mise = misemax
        else:
            mise = int(imise)
    else:
        mise = 10

    if sql.spam(PlayerID, GF.couldown_8s, "slots", "gems"):
        tab = []
        result = []
        desc = "Votre mise: {} :gem:`gems`\n\n".format(mise)
        val = 0-mise
        for i in range(0, 9): # Creation de la machine à sous
            if i == 3:
                desc += "\n"
            elif i == 6:
                desc += " :arrow_backward:\n"
            tab.append(r.randint(0, 344))
            if tab[i] < 15 :
                result.append("zero")
            elif tab[i] >= 15 and tab[i] < 30:
                result.append("one")
            elif tab[i] >= 30 and tab[i] < 45:
                result.append("two")
            elif tab[i] >= 45 and tab[i] < 60:
                result.append("three")
            elif tab[i] >= 60 and tab[i] < 75:
                result.append("four")
            elif tab[i] >= 75 and tab[i] < 90:
                result.append("five")
            elif tab[i] >= 90 and tab[i] < 105:
                result.append("six")
            elif tab[i] >= 105 and tab[i] < 120:
                result.append("seven")
            elif tab[i] >= 120 and tab[i] < 135:
                result.append("eight")
            elif tab[i] >= 135 and tab[i] < 150:
                result.append("nine")
            elif tab[i] >= 150 and tab[i] < 170:
                result.append("gem")
            elif tab[i] >= 170 and tab[i] < 190:
                result.append("ticket")
            elif tab[i] >= 190 and tab[i] < 210:
                result.append("boom")
            elif tab[i] >= 210 and tab[i] < 220:
                result.append("apple")
            elif tab[i] >= 220 and tab[i] < 230:
                result.append("green_apple")
            elif tab[i] >= 230 and tab[i] < 240:
                result.append("cherries")
            elif tab[i] >= 240 and tab[i] < 250:
                result.append("tangerine")
            elif tab[i] >= 250 and tab[i] < 260:
                result.append("banana")
            elif tab[i] >= 260 and tab[i] < 280:
                result.append("grapes")
            elif tab[i] >= 280 and tab[i] < 310:
                result.append("cookie")
            elif tab[i] >= 310 and tab[i] < 340:
                result.append("beer")
            elif tab[i] >= 340 and tab[i] < 343:
                result.append("backpack")
            elif tab[i] >= 343:
                result.append("ruby")
            if tab[i] < 340:
                desc += ":{}:".format(result[i])
            else:
                desc += "<:gem_{}:{}>".format(result[i], "{idmoji[gem_" + result[i] + "]}")
        desc += "\n"

        # ===================================================================
        # Attribution des prix
        # ===================================================================
        # Ruby (hyper rare)
        if result[3] == "ruby" or result[4] == "ruby" or result[5] == "ruby":
            sql.add(PlayerID, "ruby", 1, "inventory")
            sql.add(PlayerID, "Mineur de Merveilles", 1, "statgems")
            sql.add(PlayerID, "Mineur de Merveilles", 1, "trophy")
            gain = 42
            desc += "\nEn trouvant ce <:gem_ruby:{}>`ruby` tu deviens un Mineur de Merveilles".format("{idmoji[gem_ruby]}")
            D = r.randint(0, 20)
            if D == 0:
                sql.add(PlayerID, "lootbox_legendarygems", 1, "inventory")
                desc += "\nTu as trouvé une **Loot Box Gems Légendaire**! Utilise la commande `boxes open legendarygems` pour l'ouvrir"
            elif D >= 19:
                sql.add(PlayerID, "lootbox_raregems", 1, "inventory")
                desc += "\nTu as trouvé une **Loot Box Gems Rare**! Utilise la commande `boxes open raregems` pour l'ouvrir"
            elif D >= 8 and D <= 12:
                sql.add(PlayerID, "lootbox_commongems", 1, "inventory")
                desc += "\nTu as trouvé une **Loot Box Gems Common**! Utilise la commande `boxes open commongems` pour l'ouvrir"
        # ===================================================================
        # Super gain, 3 chiffres identique
        elif result[3] == "seven" and result[4] == "seven" and result[5] == "seven":
            gain = 1000
            sql.add(PlayerID, "Super Jackpot :seven::seven::seven:", 1, "statgems")
            sql.add(PlayerID, "Super Jackpot :seven::seven::seven:", 1, "trophy")
            desc += "\nBravo <@{}>! Le Super Jackpot :seven::seven::seven: est tombé :tada: ".format(param["ID"])
        elif result[3] == "one" and result[4] == "one" and result[5] == "one":
            gain = 100
        elif result[3] == "two" and result[4] == "two" and result[5] == "two":
            gain = 150
        elif result[3] == "three" and result[4] == "three" and result[5] == "three":
            gain = 200
        elif result[3] == "four" and result[4] == "four" and result[5] == "four":
            gain = 250
        elif result[3] == "five" and result[4] == "five" and result[5] == "five":
            gain = 300
        elif result[3] == "six" and result[4] == "six" and result[5] == "six":
            gain = 350
        elif result[3] == "eight" and result[4] == "eight" and result[5] == "eight":
            gain = 400
        elif result[3] == "nine" and result[4] == "nine" and result[5] == "nine":
            gain = 450
        elif result[3] == "zero" and result[4] == "zero" and result[5] == "zero":
            gain = 500
        # ===================================================================
        # Beer
        elif (result[3] == "beer" and result[4] == "beer") or (result[4] == "beer" and result[5] == "beer") or (result[3] == "beer" and result[5] == "beer"):
            sql.add(PlayerID, "La Squelatitude", 1, "statgems")
            sql.add(PlayerID, "La Squelatitude", 1, "trophy")
            gain = 4
            desc += "\n<@{}> paye sa tournée :beer:".format(param["ID"])
        # ===================================================================
        # Explosion de la machine
        elif result[3] == "boom" and result[4] == "boom" and result[5] == "boom":
            gain = -50
        elif (result[3] == "boom" and result[4] == "boom") or (result[4] == "boom" and result[5] == "boom") or (result[3] == "boom" and result[5] == "boom"):
            gain = -10
        elif result[3] == "boom" or result[4] == "boom" or result[5] == "boom":
            gain = -2
        # ===================================================================
        # Gain de gem
        elif result[3] == "gem" and result[4] == "gem" and result[5] == "gem":
            gain = 50
        elif (result[3] == "gem" and result[4] == "gem") or (result[4] == "gem" and result[5] == "gem") or (result[3] == "gem" and result[5] == "gem"):
            gain = 15
        elif result[3] == "gem" or result[4] == "gem" or result[5] == "gem":
            gain = 5
        # ===================================================================
        # Tichet gratuit
        elif result[3] == "ticket" and result[4] == "ticket" and result[5] == "ticket":
            gain = 10
        elif (result[3] == "ticket" and result[4] == "ticket") or (result[4] == "ticket" and result[5] == "ticket") or (result[3] == "ticket" and result[5] == "ticket"):
            gain = 5
        elif result[3] == "ticket" or result[4] == "ticket" or result[5] == "ticket":
            gain = 2
        else:
            gain = 0
        # ===================================================================
        # Cookie
        nbCookie = 0
        if result[3] == "cookie" and result[4] == "cookie" and result[5] == "cookie":
            nbCookie = 3
        elif (result[3] == "cookie" and result[4] == "cookie") or (result[4] == "cookie" and result[5] == "cookie") or (result[3] == "cookie" and result[5] == "cookie"):
            nbCookie = 2
        elif result[3] == "cookie" or result[4] == "cookie" or result[5] == "cookie":
            nbCookie = 1
        if nbCookie != 0:
            if GF.testInvTaille(PlayerID):
                desc += "\nTu a trouvé {} :cookie:`cookie`".format(nbCookie)
                sql.add(PlayerID, "cookie", nbCookie, "inventory")
            else:
                desc += "\nTon inventaire est plein"
            D = r.randint(0, 20)
            if D == 0:
                sql.add(PlayerID, "lootbox_legendarygems", 1, "inventory")
                desc += "\nTu as trouvé une **Loot Box Gems Légendaire**! Utilise la commande `boxes open legendarygems` pour l'ouvrir"
            elif D >= 19:
                sql.add(PlayerID, "lootbox_raregems", 1, "inventory")
                desc += "\nTu as trouvé une **Loot Box Gems Rare**! Utilise la commande `boxes open raregems` pour l'ouvrir"
            elif D >= 8 and D <= 12:
                sql.add(PlayerID, "lootbox_commongems", 1, "inventory")
                desc += "\nTu as trouvé une **Loot Box Gems Common**! Utilise la commande `boxes open commongems` pour l'ouvrir"
        # ===================================================================
        # grappe
        nbGrapes = 0
        if result[3] == "grapes" and result[4] == "grapes" and result[5] == "grapes":
            nbGrapes = 3
        elif (result[3] == "grapes" and result[4] == "grapes") or (result[4] == "grapes" and result[5] == "grapes") or (result[3] == "grapes" and result[5] == "grapes"):
            nbGrapes = 2
        elif result[3] == "grapes" or result[4] == "grapes" or result[5] == "grapes":
            nbGrapes = 1
        if nbGrapes != 0:
            if GF.testInvTaille(PlayerID):
                desc += "\nTu a trouvé {} :grapes:`grapes`".format(nbGrapes)
                sql.add(PlayerID, "grapes", nbGrapes, "inventory")
            else:
                desc += "\nTon inventaire est plein"
        # ===================================================================
        # Backpack (hyper rare)
        if result[3] == "backpack" or result[4] == "backpack" or result[5] == "backpack":
            sql.add(PlayerID, "backpack", 1, "inventory")
            p = 0
            for c in GF.objetItem:
                if c.nom == "backpack":
                    p = c.poids * (-1)
            desc += "\nEn trouvant ce <:gem_backpack:{0}>`backpack` tu gagnes {1} points d'inventaire".format("{idmoji[gem_backpack]}", p)

        # Calcul du prix
        prix = gain * mise
        if gain != 0 and gain != 1:
            if prix > 400:
                desc += "\n:slot_machine: Jackpot! Tu viens de gagner {} :gem:`gems`".format(prix)
            elif prix > 0:
                desc += "\nBravo, tu viens de gagner {} :gem:`gems`".format(prix)
            else:
                desc += "\nLa machine viens d'exploser :boom:\nTu as perdu {} :gem:`gems`".format(-1*prix)
            sql.addGems(PlayerID, prix)
            sql.addGems(GF.PlayerID_GetGems, -prix)
        elif gain == 1:
            desc += "\nBravo, voici un ticket gratuit pour relancer la machine à sous"
            sql.addGems(PlayerID, prix)
        else:
            desc += "\nLa machine à sous ne paya rien ..."
            sql.addGems(PlayerID, val)
        sql.updateComTime(PlayerID, "slots", "gems")
        if gain >= 0:
            lvl.addxp(PlayerID, gain + 1, "gems")
        msg.append("OK")
    else:
        desc = "Il faut attendre "+str(GF.couldown_8s)+" secondes entre chaque commande !"
        msg.append("couldown")
    msg.append(desc)
    return msg


def boxes(param):
    """**open [nom]** | Ouverture de Loot Box"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    fct = param["fct"]
    name = param["name"]
    msg = []
    Lang = sql.get_lang(param["IDGuild"])

    if fct == "open":
        if name != "None":
            for lootbox in GF.objetBox:
                if name == "lootbox_{}".format(lootbox.nom):
                    name = lootbox.nom
            if sql.valueAtNumber(PlayerID, "lootbox_{}".format(name), "inventory") > 0:
                for lootbox in GF.objetBox:
                    if name == lootbox.nom:
                        titre = lootbox.titre
                        gain = r.randint(lootbox.min, lootbox.max)
                        sql.add(PlayerID, "lootbox_{}".format(lootbox.nom), -1, "inventory")

                        sql.addGems(PlayerID, gain)
                        desc = "{} :gem:`gems`\n".format(gain)
                        if name == "gift":
                            if r.randint(0,6) == 0:
                                nb = r.randint(-2, 3)
                                if nb < 1:
                                    nb = 1
                                # sql.addSpinelles(PlayerID, nb)
                                # desc += "{nombre} <:spinelle:{idmoji}>`spinelle`\n".format(idmoji="{idmoji[spinelle]}", nombre=nb)
                            for x in GF.objetItem:
                                if r.randint(0,10) <= 1:
                                    if x.nom == "hyperpack":
                                        nbgain = 1
                                    else:
                                        nbgain = r.randint(3, 8)
                                    sql.add(PlayerID, x.nom, nbgain, "inventory")
                                    if x.type != "emoji":
                                        desc += "\n<:gem_{0}:{2}>`{0}` x{1}".format(x.nom, nbgain, "{idmoji[gem_" + x.nom + "]}")
                                    else:
                                        desc += "\n:{0}:`{0}` x{1}".format(x.nom, nbgain)
                        elif name == "gift_heart":
                            for x in GF.objetItem:
                                if r.randint(0,15) >= 14:
                                    if x.nom == "hyperpack":
                                        nbgain = r.randint(1,2)
                                    else:
                                        nbgain = r.randint(4, 10)
                                    sql.add(PlayerID, x.nom, nbgain, "inventory")
                                    if x.type != "emoji":
                                        desc += "\n<:gem_{0}:{2}>`{0}` x{1}".format(x.nom, nbgain, "{idmoji[gem_" + x.nom + "]}")
                                    else:
                                        desc += "\n:{0}:`{0}` x{1}".format(x.nom, nbgain)
                        lvl.addxp(PlayerID, lootbox.xp, "gems")
                        msg.append("OK")
                        msg.append(desc)
                        msg.append(titre)
                        return msg

                desc = "Cette box n'existe pas"
                msg.append("NOK")
            else:
                desc = "Tu ne possèdes pas cette Loot Box"
                msg.append("NOK")
        else:
            desc = "Commande `boxes open` incomplète"
            msg.append("NOK")
    elif fct == "None":
        desc = "Commande `boxes` incomplète"
        msg.append("NOK")
    else:
        desc = "Commande `boxes` invalide"
        msg.append("NOK")
    msg.append(desc)
    return msg


def hothouse(param):
    """**[harvest / plant]** {_n° plantation / item à planter_} | Plantons compagnons !!"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    fct = param["fct"]
    arg = param["arg"]
    arg2 = param["arg2"]
    msg = []
    desc = ""
    Lang = sql.get_lang(param["IDGuild"])

    maxplanting = 50
    if sql.spam(PlayerID, GF.couldown_4s, "hothouse", "gems"):
        nbplanting = int(sql.valueAtNumber(PlayerID, "planting_plan", "inventory")) + 1
        if nbplanting >= maxplanting:
            nbplanting = maxplanting
        i = 1
        sql.updateComTime(PlayerID, "hothouse", "gems")
        if fct == "None" or fct == "harvest":
            if arg != "None":
                if int(arg) <= nbplanting:
                    nbplanting = int(arg)
                else:
                    desc = "Tu n'as pas assez de plantations ou cette plantation n'est pas disponible!"
                    msg.append("NOK")
                    msg.append(desc)
                    return msg
            msg.append("OK")
            msg.append("{}".format(nbplanting))
            while i <= nbplanting:
                data = []
                valuePlanting = sql.valueAt(PlayerID, i, "hothouse")
                if valuePlanting != 0:
                    valueTime = float(valuePlanting[0])
                    valueItem = valuePlanting[1]
                else:
                    valueTime = 0
                    valueItem = ""
                if valueItem == "cacao":
                    couldown = GF.couldown_4h
                else:
                    couldown = GF.couldown_6h
                if valueTime == 0:
                    desc = "Cette plantation est vide!"
                else:
                    PlantingTime = float(valueTime)
                    InstantTime = t.time()
                    time = PlantingTime - (InstantTime-couldown)
                    if time <= 0:
                        De = r.randint(1, 15)
                        jour = dt.date.today()
                        if valueItem == "seed" or valueItem == "":
                            if (jour.month == 10 and jour.day >= 23) or (jour.month == 11 and jour.day <= 10): # Special Halloween
                                if De <= 2:
                                    nbHarvest = r.randint(1, 2)
                                    item = "oak"
                                elif De > 2 and De <= 7:
                                    nbHarvest = r.randint(2, 4)
                                    item = "pumpkin"
                                elif De > 7 and De <= 10:
                                    nbHarvest = r.randint(1, 2)
                                    item = "spruce"
                                elif De > 10 and De <= 12:
                                    nbHarvest = r.randint(1, 2)
                                    item = "palm"
                                elif De > 12 and De <= 14:
                                    nbHarvest = r.randint(4, 10)
                                    item = "wheat"
                                elif De > 14:
                                    nbHarvest = r.randint(6, 12)
                                    item = "grapes"
                            else:
                                if De <= 5:
                                    nbHarvest = r.randint(1, 2)
                                    item = "oak"
                                elif De > 5 and De <= 9:
                                    nbHarvest = r.randint(1, 2)
                                    item = "spruce"
                                elif De > 9 and De <= 12:
                                    nbHarvest = r.randint(1, 2)
                                    item = "palm"
                                elif De > 12 and De <= 14:
                                    nbHarvest = r.randint(4, 10)
                                    item = "wheat"
                                elif De > 14:
                                    nbHarvest = r.randint(6, 12)
                                    item = "grapes"
                        elif valueItem == "cacao":
                            nbHarvest = r.randint(1, 4)
                            item = "chocolate"
                        data = []
                        data.append(0)
                        data.append("")
                        sql.add(PlayerID, item, nbHarvest, "inventory")
                        sql.updateField(PlayerID, i, data, "hothouse")
                        if item == "grapes":
                            desc = "Ta plantation à fini de pousser, en la coupant tu gagnes {2} :{1}:`{1}`".format("{idmoji[gem_" + item + "]}", item, nbHarvest)
                        else:
                            desc = "Ta plantation à fini de pousser, en la coupant tu gagnes {2} <:gem_{1}:{0}>`{1}`".format("{idmoji[gem_" + item + "]}", item, nbHarvest)
                        lvl.addxp(PlayerID, 1, "gems")
                        if i > 1:
                            if sql.valueAtNumber(PlayerID, "planting_plan", "inventory") > 0:
                                if sql.valueAt(PlayerID, "planting_plan", "durability") == 0:
                                    for c in GF.objetOutil:
                                        if c.nom == "planting_plan":
                                            sql.add(PlayerID, "planting_plan", c.durabilite, "durability")
                                sql.add(PlayerID, "planting_plan", -1, "durability")
                                if sql.valueAt(PlayerID, "planting_plan", "durability")[0] <= 0:
                                    for c in GF.objetOutil:
                                        if c.nom == "planting_plan":
                                            sql.add(PlayerID, "planting_plan", c.durabilite, "durability")
                                    sql.add(PlayerID, "planting_plan", -1, "inventory")

                    else:
                        timeH = int(time / 60 / 60)
                        time = time - timeH * 3600
                        timeM = int(time / 60)
                        timeS = int(time - timeM * 60)
                        desc = "<:gem_{3}:{4}>`{3}` | Ta plantation aura fini de pousser dans :clock2:`{0}h {1}m {2}s`".format(timeH, timeM, timeS, valueItem, "{idmoji[gem_" + valueItem + "]}")
                msg.append("{}".format(i))
                msg.append(desc)
                i += 1
            # << while i <= nbplanting:
            return msg
        elif fct == "plant":
            if sql.valueAtNumber(GF.PlayerID_GetGems, "DailyMult", "daily") == 1:
                desc = "Plantations endommagées! Un violent orage :cloud_lightning: à détruit tes plantations\nTes plantations seront réparrées au plus vite"
                msg.append("NOK")
                msg.append(desc)
                return msg
            if arg != "seed" and arg != "cacao":
                arg = "seed"
            if arg2 != "None":
                try:
                    arg2 = int(arg2)
                except:
                    msg.append("NOK")
                    msg.append("Veuillez indiquer un numéro de plantation valide")
                    return msg
                if arg2 > nbplanting:
                    desc = "Tu n'as pas assez de plantations ou cette plantation n'est pas disponible!"
                    msg.append("NOK")
                    msg.append(desc)
                    return msg
                elif int(arg2) < 0:
                    sql.addGems(PlayerID, -100)
                    lvl.addxp(PlayerID, -10, "gems")
                    desc = ":no_entry: Anti-cheat! Je vous met un amende de 100 :gem:`gems` pour avoir essayé de tricher !"
                    sql.add(PlayerID, "DiscordCop Amende", 1, "statgems")
                    msg.append("anticheat")
                    msg.append(desc)
                    return msg
                data = []
                valuePlanting = sql.valueAt(PlayerID, i, "hothouse")
                if valuePlanting != 0:
                    valueTime = float(valuePlanting[0])
                    valueItem = valuePlanting[1]
                else:
                    valueTime = 0
                    valueItem = ""
                if valueItem == "cacao":
                    couldown = "4h"
                else:
                    couldown = "6h"
                if valueTime == 0:
                    PlantingItemValue = sql.valueAtNumber(PlayerID, arg, "inventory")
                    if PlantingItemValue >= 1:
                        data = []
                        data.append(str(t.time()))
                        data.append(arg)
                        sql.add(PlayerID, arg2, data, "hothouse")
                        sql.add(PlayerID, arg, -1, "inventory")
                        desc = "<:gem_{0}:{1}>`{0}` plantée. Elle aura fini de pousser dans :clock2:`{2}`".format(arg, "{idmoji[gem_" + arg + "]}", couldown)
                    else:
                        desc = "Tu n'as pas de <:gem_{0}:{1}>`{0}` à planter dans ton inventaire".format(arg, "{idmoji[gem_" + arg + "]}")
                else:
                    desc = "Tu as déjà planté une <:gem_{0}:{1}>`{0}` dans cette plantation".format(valueItem, "{idmoji[gem_" + valueItem + "]}")
                msg.append("OK")
                msg.append("{}".format(nbplanting))
                msg.append("{}".format(arg2))
                msg.append(desc)
                return msg
            else:
                j = 0
                msg.append("OK")
                msg.append("{}".format(nbplanting))
                while i <= nbplanting:
                    data = []
                    valuePlanting = sql.valueAt(PlayerID, i, "hothouse")
                    if valuePlanting != 0:
                        valueTime = float(valuePlanting[0])
                        valueItem = valuePlanting[1]
                    else:
                        valueTime = 0
                        valueItem = ""
                    PlantingItemValue = sql.valueAtNumber(PlayerID, arg, "inventory")
                    if valueItem == "cacao" or (valueItem == "" and arg == "cacao"):
                        couldown = "4h"
                    else:
                        couldown = "6h"
                    if valueTime == 0:
                        if PlantingItemValue >= 1:
                            data = []
                            data.append(str(t.time()))
                            data.append(arg)
                            sql.add(PlayerID, i, data, "hothouse")
                            sql.add(PlayerID, arg, -1, "inventory")
                            desc = "<:gem_{0}:{1}>`{0}` plantée. Elle aura fini de pousser dans :clock2:`{2}`".format(arg, "{idmoji[gem_" + arg + "]}", couldown)
                        else:
                            desc = "Tu n'as pas de <:gem_{0}:{1}>`{0}` à planter dans ton inventaire".format(arg, "{idmoji[gem_" + arg + "]}")
                            if j == 0:
                                j = -1
                                if arg == "seed":
                                    arg = "cacao"
                                else:
                                    arg = "seed"
                    else:
                        desc = "Tu as déjà planté une <:gem_{0}:{1}>`{0}` dans cette plantation".format(valueItem, "{idmoji[gem_" + valueItem + "]}")
                    msg.append("{}".format(i))
                    msg.append(desc)
                    if j == -1:
                        j = 1
                    else:
                        i += 1
            return msg
        else:
            desc = "Fonction inconnu"
            msg.append("NOK")
            msg.append(desc)
            return msg
    else:
        desc = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
        msg.append("couldown")
        msg.append(desc)
        return msg
