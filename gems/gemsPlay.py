import random as r
import time as t
import datetime as dt
from DB import SQLite as sql
import sqlite3
from gems import gemsFonctions as GF
from core import level as lvl
from languages import lang as lang_P


def daily(param):
    """Récupère ta récompense journalière!"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
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
        desc = lang_P.forge_msg(lang, "daily", None, False, 0)
        desc += lang_P.forge_msg(lang, "daily", [DailyMult, bonus*DailyMult], False, 1)
        lvl.addxp(PlayerID, 10*(DailyMult/2), "gems")
        if DailyMult % 30 == 0:
            m = (DailyMult//30)*5
            # sql.addSpinelles(PlayerID, m)
            sql.addGems(PlayerID, m*250000)
            desc += lang_P.forge_msg(lang, "daily", [DailyMult, m*250000], False, 2)

    elif DailyTime == str(jour):
        desc = lang_P.forge_msg(lang, "daily", None, False, 3)
    else:
        sql.add(PlayerID, "DailyMult", 1, "daily")
        sql.add(PlayerID, "DailyTime", str(jour), "daily")
        desc = lang_P.forge_msg(lang, "daily", None, False, 0)
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
    lang = param["lang"]
    ARG = param["ARG"]
    ARG2 = param["ARG2"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    platform = param["name_pl"]

    if ARG != "None":
        mARG = ARG.lower()
    else:
        mARG = "bal"
    for c in GF.objetOutil:
        if c.type == "bank":
            Taille = c.poids
    solde = sql.valueAt(PlayerID, "Solde", "bank")
    if solde == 0:
        sql.add(PlayerID, "SoldeMax", Taille, "bank")
    if mARG == "bal":
        bank_bal(PlayerID, lang, ARG, ARG2, Taille, platform)
    elif mARG == "add":
        bank_add(PlayerID, lang, ARG, ARG2, Taille)
    elif mARG == "saving":
        bank_saving(PlayerID, lang, ARG, ARG2, Taille)


def bank_bal(PlayerID, lang, ARG, ARG2, Taille, platform):
    """Compte épargne | Balance du compte"""
    msg = []
    desc = ""
    # =======================================================================
    # Affiche le menu principal de la banque
    # !bank bal <nom d'un joueur> permet de visualiser l'état de la banque de ce joueur
    # =======================================================================
    if sql.spam(PlayerID, GF.couldown_4s, "bank_bal", "gems"):
        msg.append("bal")
        msg.append(lang)
        if ARG2 != "None":
            ID = sql.get_SuperID(sql.nom_ID(ARG2), platform)
            PlayerID = sql.get_PlayerID(ID, "gems")
        solde = sql.valueAtNumber(PlayerID, "Solde", "bank")
        soldeMax = sql.valueAtNumber(PlayerID, "SoldeMax", "bank")
        if soldeMax == 0:
            soldeMax = Taille
        desc = "{} / {} :gem:`gems`\n".format(solde, soldeMax)
        msg.append(desc)
        desc = lang_P.forge_msg(lang, "bank", None, False, 0)
        desc += lang_P.forge_msg(lang, "bank", None, False, 1)
        desc += lang_P.forge_msg(lang, "bank", None, False, 2)
        desc += lang_P.forge_msg(lang, "bank", ["bank_upgrade", "{idmoji[gem_bank_upgrade]}"], False, 3)
        msg.append(desc)
        sql.updateComTime(PlayerID, "bank_bal", "gems")
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)])
        msg.append("couldown")
        msg.append(desc)
    return msg


def bank_add(PlayerID, lang, ARG, ARG2, Taille):
    """Compte épargne | Crédits"""
    msg = []
    desc = ""
    # =======================================================================
    # Ajoute ou enlève des Gems sur le compte épargne
    # un nombre positif ajoute des Gems
    # un nombre négatif enlève des Gems
    # =======================================================================
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
                    desc = lang_P.forge_msg(lang, "bank", [soldeMax], False, 4)
                elif soldeNew < 0:
                    desc = lang_P.forge_msg(lang, "bank", [solde], False, 5)
                    msg.append("NOK")
                    msg.append(desc)
                    return msg
                nbgm = -1*ARG2
                sql.addGems(PlayerID, nbgm)
                sql.add(PlayerID, "solde", ARG2, "bank")
                desc += lang_P.forge_msg(lang, "bank", [ARG2], False, 6)
                desc += lang_P.forge_msg(lang, "bank", [sql.valueAtNumber(PlayerID, "Solde", "bank")], False, 7)
                msg.append("add")
                sql.updateComTime(PlayerID, "bank_add", "gems")
            else:
                desc = lang_P.forge_msg(lang, "bank", None, False, 8)
                msg.append("NOK")
        else:
            desc = lang_P.forge_msg(lang, "bank", None, False, 9)
            msg.append("NOK")
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)])
        msg.append("couldown")
    msg.append(desc)
    return msg


def bank_saving(PlayerID, lang, ARG, ARG2, Taille):
    """Compte épargne | Épargne"""
    msg = []
    desc = ""
    # =======================================================================
    # Fonction d'épargne
    # L'intéret est de 20% avec un bonus de 1% pour chanque bank_upgrade possédée
    # =======================================================================
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
        desc = lang_P.forge_msg(lang, "bank", [int(soldeAdd)], False, 10)
        soldeNew = solde + soldeAdd
        if soldeNew > soldeMax:
            soldeMove = soldeNew - soldeMax
            nbgm = -1 * soldeMove
            sql.addGems(PlayerID, int(soldeMove))
            sql.add(PlayerID, "solde", int(nbgm), "bank")
            desc += lang_P.forge_msg(lang, "bank", [soldeMax], False, 11)
        desc += lang_P.forge_msg(lang, "bank", [sql.valueAtNumber(PlayerID, "Solde", "bank")], False, 7)
        sql.add(PlayerID, "bank saving", 1, "statgems")
        sql.add(PlayerID, "bank saving | gain", int(soldeAdd), "statgems")
        # =====================================
        # Bonus
        # =====================================
        desc += GF.lootbox(PlayerID, lang)
        desc += GF.gift(PlayerID, lang)
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
        desc = lang_P.forge_msg(lang, "bank", [timeH, timeM, timeS], False, 12)
    msg.append("saving")
    msg.append(desc)
    return msg


def stealing(param):
    """**[nom]** | Vole des :gem:`gems` aux autres joueurs!"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    name = param["name"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []

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
                            desc = lang_P.forge_msg(lang, "DiscordCop Arrestation", [int(gain/4)], False, 0)
                        else:
                            sql.updateField(PlayerID, "gems", 0, "gems")
                            desc = lang_P.forge_msg(lang, "DiscordCop Arrestation", None, False, 1)
                    else:
                        sql.addGems(PlayerID, gain)
                        sql.addGems(ID_Vol, -gain)
                        # Message
                        desc = lang_P.forge_msg(lang, "stealing", [gain, name], False, 1)
                        print("Gems >> PlayerID {2} viens de voler {0} gems à {1}".format(gain, ID_Vol, PlayerID))
                    sql.updateComTime(PlayerID, "stealing", "gems")
                    lvl.addxp(PlayerID, 1, "gems")
                    sql.add(PlayerID, "stealing", 1, "statgems")
                    sql.add(PlayerID, "stealing | gain", gain, "statgems")
                else:
                    desc = lang_P.forge_msg(lang, "stealing", None, False, 2)
            except:
                desc = lang_P.forge_msg(lang, "stealing", None, False, 3)
        else:
            ComTime = sql.valueAtNumber(PlayerID, "stealing", "gems_com_time")
            time = float(ComTime) - (t.time()-GF.couldown_14h)
            timeH = int(time / 60 / 60)
            time = time - timeH * 3600
            timeM = int(time / 60)
            timeS = int(time - timeM * 60)
            desc = lang_P.forge_msg(lang, "stealing", [timeH, timeM, timeS], False, 0)
            if sql.spam(PlayerID, GF.couldown_14h, "stealing", "gems"):
                desc = lang_P.forge_msg(lang, "stealing", None, False, 4)
    msg.append("OK")
    msg.append(desc)
    return msg


def crime(param):
    """Commets un crime et gagne des :gem:`gems` Attention au DiscordCop!"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")

    msg = []
    if sql.spam(PlayerID, GF.couldown_6s, "crime", "gems"):
        # si 10 sec c'est écoulé depuis alors on peut en  faire une nouvelle
        if r.randint(0, 9) == 0:
            sql.add(PlayerID, "DiscordCop Arrestation", 1, "statgems")
            if int(sql.addGems(PlayerID, -10)) >= 0:
                desc = lang_P.forge_msg(lang, "DiscordCop Arrestation", [10], False, 0)
            else:
                desc = lang_P.forge_msg(lang, "DiscordCop Arrestation", None, False, 1)
        else:
            gain = r.randint(2, 8)
            jour = dt.date.today()
            if (jour.month == 10 and jour.day >= 23) or (jour.month == 11 and jour.day <= 10): # Special Halloween
                desc = lang_P.forge_msg(lang, "crime event")
                desc += "{1} {0}".format(gain, lang_P.forge_msg(lang, "crime array", None, True))
                if r.randint(0, 1) == 0:
                    desc += " :candy:`candy`"
                    sql.add(PlayerID, "candy", gain, "inventory")
                    sql.add(PlayerID, "Halloween | crime | candy", gain, "statgems")
                else:
                    desc += " :lollipop:`lollipop`"
                    sql.add(PlayerID, "lollipop", gain, "inventory")
                    sql.add(PlayerID, "Halloween | crime | lollipop", gain, "statgems")
            else:
                desc = "{1} {0} :gem:`gems`".format(gain, lang_P.forge_msg(lang, "crime array", None, True))
                sql.addGems(PlayerID, gain)
                sql.add(PlayerID, "crime | gain", gain, "statgems")
                try:
                    sql.addGems(GF.PlayerID_GetGems, -gain) # Vole l'équivalent du crime au bot
                except sqlite3.OperationalError:
                    pass
                desc += GF.gift(PlayerID, lang)
        sql.updateComTime(PlayerID, "crime", "gems")
        lvl.addxp(PlayerID, 1, "gems")
        sql.add(PlayerID, "crime", 1, "statgems")
        msg.append("OK")
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_6s)])
        msg.append("couldown")
    msg.append(desc)
    return msg


def gamble(param):
    """**[valeur]** | Avez vous l'ame d'un parieur ?"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    valeur = param["valeur"]
    msg = []
    valeur = int(valeur)

    gems = sql.valueAtNumber(PlayerID, "gems", "gems")
    if valeur < 0:
        desc = lang_P.forge_msg(lang, "DiscordCop Amende")
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
                desc = "{1} {0} :gem:`gems`".format(gain, lang_P.forge_msg(lang, "gamble array", None, True))
                sql.add(PlayerID, "gamble | win", 1, "statgems")
                for x in GF.objetTrophy:
                    if x.nom == "Gamble Jackpot":
                        jackpot = x.mingem
                    elif x.nom == "Super Gamble Jackpot":
                        superjackpot = x.mingem
                    elif x.nom == "Hyper Gamble Jackpot":
                        hyperjackpot = x.mingem
                if gain >= jackpot and gain < superjackpot:
                    sql.add(PlayerID, "Gamble Jackpot", 1, "trophy")
                    desc += lang_P.forge_msg(lang, "gamble", None, False, 1)
                elif gain >= superjackpot and gain < hyperjackpot:
                    sql.add(PlayerID, "Super Gamble Jackpot", 1, "trophy")
                    desc += lang_P.forge_msg(lang, "gamble", None, False, 2)
                elif gain >= hyperjackpot:
                    sql.add(PlayerID, "Hyper Gamble Jackpot", 1, "trophy")
                    desc += lang_P.forge_msg(lang, "gamble", None, False, 3)
                sql.addGems(PlayerID, gain)
                sql.add(PlayerID, "gamble | gain", gain, "statgems")
                # =====================================
                # Bonus
                # =====================================
                desc += GF.lootbox(PlayerID, lang)
            else:
                val = 0-valeur
                sql.addGems(PlayerID, val)
                sql.addGems(GF.PlayerID_GetGems, int(valeur))
                sql.add(PlayerID, "gamble | perte", valeur, "statgems")
                desc = lang_P.forge_msg(lang, "gamble", [valeur], False, 0)

            sql.updateComTime(PlayerID, "gamble", "gems")
            lvl.addxp(PlayerID, 1, "gems")
            sql.add(PlayerID, "gamble", 1, "statgems")
            msg.append("OK")
        else:
            desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_8s)])
            msg.append("couldown")
    elif gems < valeur:
        desc = lang_P.forge_msg(lang, "gamble", None, False, 4)
        msg.append("NOK")
    else:
        desc = lang_P.forge_msg(lang, "gamble", None, False, 5)
        msg.append("NOK")
    msg.append(desc)
    return msg


def mine(param):
    """Minez compagnons !!"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []
    nbMax = 0
    desc = ""

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
                    desc = lang_P.forge_msg(lang, "mine", [outil, "{idmoji[gem_" + outil + "]}"], False, 0)
                    sql.add(PlayerID, "mine | {} cassé".format(outil), 1, "statgems")
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
                        nbrand = r.randint(1, 30)
                else:
                    if nbrand <= int(nbMax*(0.50)):
                        add_item = "iron"
                        nbrand = r.randint(1, 5)
                    else:
                        add_item = "cobblestone"
                        nbrand = r.randint(1, 30)

                if nbrand != 0:
                    sql.add(PlayerID, add_item, nbrand*mult, "inventory")
                    sql.add(PlayerID, "mine | item {}".format(add_item), nbrand*mult, "statgems")
                    desc = lang_P.forge_msg(lang, "mine", [nbrand*mult, add_item, "{idmoji[gem_" + add_item + "]}"], False, 1)
                if add_item != "cobblestone":
                    nbcobble = r.randint(1, 30)
                    sql.add(PlayerID, "cobblestone", nbcobble*mult, "inventory")
                    sql.add(PlayerID, "mine | item cobblestone", nbcobble*mult, "statgems")
                    desc += lang_P.forge_msg(lang, "mine", [nbcobble*mult, "{idmoji[gem_cobblestone]}"], False, 2)

                sql.add(PlayerID, "mine", 1, "statgems")
                # =====================================
                # Bonus
                # =====================================
                desc += GF.lootbox(PlayerID, lang)
                desc += GF.gift(PlayerID, lang)

            else:
                desc = lang_P.forge_msg(lang, "mine", None, False, 3)

            sql.updateComTime(PlayerID, "mine", "gems")
            lvl.addxp(PlayerID, 1, "gems")
            msg.append("OK")
        else:
            desc = lang_P.forge_msg(lang, "WarningMsg", None, False, 2)
            msg.append("NOK")
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_6s)])
        msg.append("couldown")
    msg.append(desc)
    return msg


def dig(param):
    """Creusons compagnons !!"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []
    nbMax = 0
    desc = ""

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
                    desc = lang_P.forge_msg(lang, "dig", [outil, "{idmoji[gem_" + outil + "]}"], False, 0)
                    sql.add(PlayerID, "dig | {} cassé".format(outil), 1, "statgems")
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
                    nbrand = r.randint(0, 2)
                elif nbrand <= int(nbMax*(0.65)):
                    add_item = "seed"
                    nbrand = r.randint(0, 4)
                elif nbrand <= int(nbMax*(0.80)):
                    add_item = "potato"
                    nbrand = r.randint(0, 3)
                else:
                    nbrand = 0

                if nbrand != 0:
                    sql.add(PlayerID, add_item, nbrand*mult, "inventory")
                    sql.add(PlayerID, "dig | item {}".format(add_item), nbrand*mult, "statgems")
                    desc = lang_P.forge_msg(lang, "dig", [nbrand*mult, add_item, "{idmoji[gem_" + add_item + "]}"], False, 1)
                else:
                    desc = lang_P.forge_msg(lang, "dig", None, False, 2)

                sql.add(PlayerID, "dig", 1, "statgems")
                # =====================================
                # Bonus
                # =====================================
                desc += GF.lootbox(PlayerID, lang)
                desc += GF.gift(PlayerID, lang)

            else:
                desc = lang_P.forge_msg(lang, "dig", None, False, 3)

            sql.updateComTime(PlayerID, "dig", "gems")
            lvl.addxp(PlayerID, 1, "gems")
            msg.append("OK")
        else:
            desc = lang_P.forge_msg(lang, "WarningMsg", None, False, 2)
            msg.append("NOK")
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_6s)])
        msg.append("couldown")
    msg.append(desc)
    return msg


def fish(param):
    """Péchons compagnons !!"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []
    nbMax = 0
    desc = ""

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
                    sql.add(PlayerID, "fish | fishhook utilisé", 1, "statgems")
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
                    desc = lang_P.forge_msg(lang, "fish", [outil, "{idmoji[gem_" + outil + "]}"], False, 0)
                    sql.add(PlayerID, "fish | {} cassé".format(outil), 1, "statgems")
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
                    nbrand = r.randint(0, 4)
                elif nbrand <= int(nbMax*(0.40)):
                    add_item = "tropicalfish"
                    nbrand = r.randint(0, 4)
                elif nbrand <= int(nbMax*(0.90)):
                    add_item = "fish"
                    nbrand = r.randint(1, 16)
                else:
                    nbrand = 0

                if nbrand != 0:
                    sql.add(PlayerID, add_item, nbrand*mult, "inventory")
                    sql.add(PlayerID, "fish | item {}".format(add_item), nbrand*mult, "statgems")
                    desc = lang_P.forge_msg(lang, "fish", [nbrand*mult, add_item, "{idmoji[gem_" + add_item + "]}"], False, 1)
                    if add_item != "fish":
                        nb = r.randint(1, 16)
                        sql.add(PlayerID, "fish", nb*mult, "inventory")
                        sql.add(PlayerID, "fish | item fish", nb*mult, "statgems")
                        desc += lang_P.forge_msg(lang, "fish", [nb*mult, "{idmoji[gem_fish]}"], False, 2)
                else:
                    desc = lang_P.forge_msg(lang, "fish", None, False, 3)
                    if mult >= 2:
                        sql.add(PlayerID, "fishhook", 1, "inventory")
                        sql.add(PlayerID, "fish | fishhook utilisé", -1, "statgems")

                sql.add(PlayerID, "fish", 1, "statgems")
                # =====================================
                # Bonus
                # =====================================
                desc += GF.lootbox(PlayerID, lang)
                desc += GF.gift(PlayerID, lang)

            else:
                desc = lang_P.forge_msg(lang, "fish", ["{idmoji[fishingrod]}"], False, 4)

            sql.updateComTime(PlayerID, "fish", "gems")
            lvl.addxp(PlayerID, 1, "gems")
            msg.append("OK")
        else:
            desc = lang_P.forge_msg(lang, "WarningMsg", None, False, 2)
            msg.append("NOK")
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_6s)])
        msg.append("couldown")
    msg.append(desc)
    return msg


def slots(param):
    """**[mise]** | La machine à sous, la mise minimum est de 10 :gem:`gems`"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    imise = param["imise"]
    msg = []

    gems = sql.valueAtNumber(PlayerID, "gems", "gems")
    misemax = 200
    if imise != "None":
        if int(imise) < 0:
            desc = lang_P.forge_msg(lang, "DiscordCop Amende")
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
        desc = lang_P.forge_msg(lang, "slots", [mise], False, 0)
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
            desc += lang_P.forge_msg(lang, "slots", ["{idmoji[gem_ruby]}"], False, 1)
            GF.lootbox(PlayerID, lang)
        # ===================================================================
        # Super gain, 3 chiffres identique
        elif result[3] == "seven" and result[4] == "seven" and result[5] == "seven":
            gain = 1000
            sql.add(PlayerID, "Super Jackpot :seven::seven::seven:", 1, "statgems")
            sql.add(PlayerID, "Super Jackpot :seven::seven::seven:", 1, "trophy")
            desc += lang_P.forge_msg(lang, "slots", [param["ID"]], False, 2)
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
            desc += lang_P.forge_msg(lang, "slots", [param["ID"]], False, 3)
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
                desc += lang_P.forge_msg(lang, "slots", [nbCookie], False, 4)
                sql.add(PlayerID, "cookie", nbCookie, "inventory")
                sql.add(PlayerID, "slots | cookie", nbCookie, "statgems")
            else:
                desc += lang_P.forge_msg(lang, "slots", None, False, 5)
            GF.lootbox(PlayerID, lang)
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
                desc += lang_P.forge_msg(lang, "slots", [nbGrapes], False, 6)
                sql.add(PlayerID, "grapes", nbGrapes, "inventory")
                sql.add(PlayerID, "slots | grapes", nbGrapes, "statgems")
            else:
                desc += lang_P.forge_msg(lang, "slots", None, False, 5)
        # ===================================================================
        # Backpack (hyper rare)
        if result[3] == "backpack" or result[4] == "backpack" or result[5] == "backpack":
            sql.add(PlayerID, "backpack", 1, "inventory")
            sql.add(PlayerID, "slots | backpack", 1, "statgems")
            p = 0
            for c in GF.objetItem:
                if c.nom == "backpack":
                    p = c.poids * (-1)
            desc += lang_P.forge_msg(lang, "slots", ["{idmoji[gem_backpack]}", p], False, 7)

        # Calcul du prix
        prix = gain * mise
        if gain != 0 and gain != 1:
            if prix > 400:
                desc += lang_P.forge_msg(lang, "slots", [prix], False, 8)
            elif prix > 0:
                desc += lang_P.forge_msg(lang, "slots", [prix], False, 9)
                sql.add(PlayerID, "slots | gain", prix, "statgems")
            else:
                desc += lang_P.forge_msg(lang, "slots", [-1*prix], False, 10)
                sql.add(PlayerID, "slots | perte", -prix, "statgems")
            sql.addGems(PlayerID, prix)
            sql.addGems(GF.PlayerID_GetGems, -prix)
        elif gain == 1:
            desc += lang_P.forge_msg(lang, "slots", None, False, 11)
            sql.addGems(PlayerID, prix)
        else:
            desc += lang_P.forge_msg(lang, "slots", None, False, 12)
            sql.addGems(PlayerID, val)
            sql.add(PlayerID, "slots | perte", mise, "statgems")
        sql.updateComTime(PlayerID, "slots", "gems")
        sql.add(PlayerID, "slots", 1, "statgems")
        if gain >= 0:
            lvl.addxp(PlayerID, gain + 1, "gems")
        msg.append("OK")
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_8s)])
        msg.append("couldown")
    msg.append(desc)
    return msg


def boxes(param):
    """**open [nom]** | Ouverture de Loot Box"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    fct = param["fct"]
    name = param["name"]
    msg = []

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
                            # if r.randint(0, 6) == 0:
                            #     nb = r.randint(-2, 3)
                            #     if nb < 1:
                            #         nb = 1
                            #     sql.addSpinelles(PlayerID, nb)
                            #     desc += "{nombre} <:spinelle:{idmoji}>`spinelle`\n".format(idmoji="{idmoji[spinelle]}", nombre=nb)
                            for x in GF.objetItem:
                                if r.randint(0, 10) <= 1:
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
                                if r.randint(0, 15) >= 14:
                                    if x.nom == "hyperpack":
                                        nbgain = r.randint(1, 2)
                                    else:
                                        nbgain = r.randint(4, 10)
                                    sql.add(PlayerID, x.nom, nbgain, "inventory")
                                    if x.type != "emoji":
                                        desc += "\n<:gem_{0}:{2}>`{0}` x{1}".format(x.nom, nbgain, "{idmoji[gem_" + x.nom + "]}")
                                    else:
                                        desc += "\n:{0}:`{0}` x{1}".format(x.nom, nbgain)
                        lvl.addxp(PlayerID, lootbox.xp, "gems")
                        sql.add(PlayerID, "boxes | open {}".format(lootbox.titre), 1, "statgems")
                        sql.add(PlayerID, "boxes", 1, "statgems")
                        msg.append("OK")
                        msg.append(desc)
                        msg.append(titre)
                        return msg

                desc = lang_P.forge_msg(lang, "boxes", None, False, 0)
                msg.append("NOK")
            else:
                desc = lang_P.forge_msg(lang, "boxes", None, False, 1)
                msg.append("NOK")
        else:
            desc = lang_P.forge_msg(lang, "boxes", None, False, 2)
            msg.append("NOK")
    elif fct == "None":
        desc = lang_P.forge_msg(lang, "boxes", None, False, 3)
        msg.append("NOK")
    else:
        desc = lang_P.forge_msg(lang, "boxes", None, False, 4)
        msg.append("NOK")
    msg.append(desc)
    return msg


def hothouse(param):
    """**[harvest / plant]** {_n° plantation / item à planter_} | Plantons compagnons !!"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    fct = param["fct"]
    arg = param["arg"]
    arg2 = param["arg2"]
    msg = []
    desc = ""

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
                    desc = lang_P.forge_msg(lang, "hothouse", None, False, 0)
                    msg.append("NOK")
                    msg.append(desc)
                    return msg
            msg.append("OK")
            msg.append(lang)
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
                    desc = lang_P.forge_msg(lang, "hothouse", None, False, 1)
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
                        sql.add(PlayerID, "hothouse | harvest | item {}".format(item), nbHarvest, "statgems")
                        sql.updateField(PlayerID, i, data, "hothouse")
                        if item == "grapes":
                            desc = lang_P.forge_msg(lang, "hothouse", ["{idmoji[gem_" + item + "]}", item, nbHarvest], False, 2)
                        else:
                            desc = lang_P.forge_msg(lang, "hothouse", ["{idmoji[gem_" + item + "]}", item, nbHarvest], False, 3)
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
                        desc = lang_P.forge_msg(lang, "hothouse", [timeH, timeM, timeS, valueItem, "{idmoji[gem_" + valueItem + "]}"], False, 4)
                msg.append("{}".format(i))
                msg.append(desc)
                i += 1
            # << while i <= nbplanting:
            return msg
        elif fct == "plant":
            if sql.valueAtNumber(GF.PlayerID_GetGems, "DailyMult", "daily") == 1:
                desc = lang_P.forge_msg(lang, "hothouse", None, False, 5)
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
                    desc = lang_P.forge_msg(lang, "hothouse", None, False, 6)
                    msg.append(desc)
                    return msg
                if arg2 > nbplanting:
                    desc = lang_P.forge_msg(lang, "hothouse", None, False, 7)
                    msg.append("NOK")
                    msg.append(desc)
                    return msg
                elif int(arg2) < 0:
                    sql.addGems(PlayerID, -100)
                    lvl.addxp(PlayerID, -10, "gems")
                    desc = lang_P.forge_msg(lang, "DiscordCop Amende")
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
                    couldown = ":clock4:`4h`"
                else:
                    couldown = ":clock6:`6h`"
                if valueTime == 0:
                    PlantingItemValue = sql.valueAtNumber(PlayerID, arg, "inventory")
                    if PlantingItemValue >= 1:
                        data = []
                        data.append(str(t.time()))
                        data.append(arg)
                        sql.add(PlayerID, arg2, data, "hothouse")
                        sql.add(PlayerID, arg, -1, "inventory")
                        sql.add(PlayerID, "hothouse | plant | item {}".format(arg), 1, "statgems")
                        desc = lang_P.forge_msg(lang, "hothouse", [arg, "{idmoji[gem_" + arg + "]}", couldown], False, 8)
                    else:
                        desc = lang_P.forge_msg(lang, "hothouse", [arg, "{idmoji[gem_" + arg + "]}"], False, 9)
                else:
                    desc = lang_P.forge_msg(lang, "hothouse", [valueItem, "{idmoji[gem_" + valueItem + "]}"], False, 10)
                msg.append("OK")
                msg.append(lang)
                msg.append("{}".format(nbplanting))
                msg.append("{}".format(arg2))
                msg.append(desc)
                return msg
            else:
                j = 0
                msg.append("OK")
                msg.append(lang)
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
                            sql.add(PlayerID, "hothouse | plant | item {}".format(arg), 1, "statgems")
                            desc = lang_P.forge_msg(lang, "hothouse", [arg, "{idmoji[gem_" + arg + "]}", couldown], False, 11)
                        else:
                            desc = lang_P.forge_msg(lang, "hothouse", [arg, "{idmoji[gem_" + arg + "]}"], False, 12)
                            if j == 0:
                                j = -1
                                if arg == "seed":
                                    arg = "cacao"
                                else:
                                    arg = "seed"
                    else:
                        desc = lang_P.forge_msg(lang, "hothouse", [valueItem, "{idmoji[gem_" + valueItem + "]}"], False, 13)
                    msg.append("{}".format(i))
                    msg.append(desc)
                    if j == -1:
                        j = 1
                    else:
                        i += 1
            return msg
        else:
            desc = lang_P.forge_msg(lang, "hothouse", None, False, 14)
            msg.append("NOK")
            msg.append(desc)
            return msg
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)])
        msg.append("couldown")
        msg.append(desc)
        return msg


def ferment(param):
    """**{grapes/wheat}** | Cave de fermentation. Alcool illimité !!"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    item = param["item"]
    msg = []
    desc = ""
    gain = ""
    i = 1
    max = 20

    if sql.spam(PlayerID, GF.couldown_4s, "ferment", "gems"):
        if item == "grapes":
            nbitem = 10
            gain = "wine_glass"
            couldown = GF.couldown_3h
            couldownMsg = ":clock3:`3h`"
        elif item == "wheat":
            nbitem = 8
            gain = "beer"
            couldown = GF.couldown_8h
            couldownMsg = ":clock8:`8h`"
        sql.updateComTime(PlayerID, "ferment", "gems")
        nbferment = sql.valueAtNumber(PlayerID, "barrel", "inventory") + 1
        if nbferment >= max:
            nbferment = max
        msg.append("OK")
        msg.append(lang)
        msg.append("{}".format(nbferment))
        while i <= nbferment:
            data = []
            valueFerment = sql.valueAt(PlayerID, i, "ferment")
            if valueFerment != 0:
                valueTime = float(valueFerment[0])
                valueItem = valueFerment[1]
            else:
                valueTime = 0
                valueItem = ""
            fermentItem = sql.valueAtNumber(PlayerID, item, "inventory")
            if valueItem == "" and item == "None":
                desc = lang_P.forge_msg(lang, "ferment", None, False, 0)
            elif item == "grapes" or item == "wheat":
                if valueTime == 0:
                    if fermentItem >= nbitem:
                        data = []
                        data.append(str(t.time()))
                        data.append(item)
                        sql.add(PlayerID, i, data, "ferment")
                        sql.add(PlayerID, item, -nbitem, "inventory")
                        sql.add(PlayerID, "ferment | plant | item {}".format(item), nbitem, "statgems")
                        if item == "grapes":
                            desc = lang_P.forge_msg(lang, "ferment", [item, couldownMsg], False, 1)
                        else:
                            desc = lang_P.forge_msg(lang, "ferment", [item, "{idmoji[gem_" + item + "]}", couldownMsg], False, 2)
                    else:
                        if item == "grapes":
                            desc = lang_P.forge_msg(lang, "ferment", [item, gain, nbitem], False, 3)
                        else:
                            desc = lang_P.forge_msg(lang, "ferment", [item, "{idmoji[gem_" + item + "]}", gain, nbitem], False, 4)

                else:
                    if valueItem == "grapes":
                        desc = lang_P.forge_msg(lang, "ferment", [valueItem], False, 5)
                    else:
                        desc = lang_P.forge_msg(lang, "ferment", [valueItem, "{idmoji[gem_" + valueItem + "]}"], False, 6)
            elif item == "None":
                couldown = GF.couldown_3h
                nbgain = 0
                if valueItem == "grapes":
                    gain = "wine_glass"
                    nbgain = r.randint(1, 4)
                    couldown = GF.couldown_3h
                elif valueItem == "wheat":
                    gain = "beer"
                    nbgain = r.randint(2, 6)
                    couldown = GF.couldown_8h
                CookedTime = float(valueTime)
                InstantTime = t.time()
                time = CookedTime - (InstantTime-couldown)
                if time <= 0:
                    data = []
                    data.append(0)
                    data.append("")
                    sql.add(PlayerID, gain, nbgain, "inventory")
                    sql.add(PlayerID, "ferment | harvest | item {}".format(gain), nbgain, "statgems")
                    sql.updateField(PlayerID, i, data, "ferment")
                    desc = lang_P.forge_msg(lang, "ferment", [gain, "{idmoji[gem_" + gain + "]}", nbgain], False, 7)
                    lvl.addxp(PlayerID, 1, "gems")
                    if i > 1:
                        nbbarrel = int(sql.valueAtNumber(PlayerID, "barrel", "inventory"))
                        if nbbarrel > 0:
                            if sql.valueAtNumber(PlayerID, "barrel", "durability") == 0:
                                for c in GF.objetOutil:
                                    if c.nom == "barrel":
                                        sql.add(PlayerID, "barrel", c.durabilite, "durability")
                            sql.add(PlayerID, "barrel", -1, "durability")
                            if sql.valueAtNumber(PlayerID, "barrel", "durability") <= 0:
                                for c in GF.objetOutil:
                                    if c.nom == "barrel":
                                        sql.add(PlayerID, "barrel", c.durabilite, "durability")
                                sql.add(PlayerID, "barrel", -1, "inventory")
                else:
                    timeH = int(time / 60 / 60)
                    time = time - timeH * 3600
                    timeM = int(time / 60)
                    timeS = int(time - timeM * 60)
                    if valueItem == "grapes":
                        desc = lang_P.forge_msg(lang, "ferment", [valueItem], False, 5)
                    else:
                        desc = lang_P.forge_msg(lang, "ferment", [valueItem, "{idmoji[gem_" + valueItem + "]}"], False, 6)
                    desc += lang_P.forge_msg(lang, "ferment", [timeH, timeM, timeS], False, 8)
            msg.append("{}".format(i))
            msg.append(desc)
            i += 1
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)])
        msg.append("NOK")
        msg.append(desc)
    return msg


def cooking(param):
    """**{potato/pumpkin/chocolate}** | Cuisinons compagnons !!"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    item = param["item"]
    msg = []
    desc = ""
    gain = ""
    i = 1
    jour = dt.date.today()
    max = 20

    if sql.spam(PlayerID, GF.couldown_4s, "cooking", "gems"):
        if item == "pumpkin":
            if (jour.month == 10 and jour.day >= 26) or (jour.month == 11 and jour.day <= 10):
                item = "pumpkin"
                gain = "pumpkinpie"
                nbitem = 12
                couldown = GF.couldown_2h
                couldownMsg = ":clock2:`2h`"
            else:
                msg.append("NOK")
                msg.append(lang_P.forge_msg(lang, "cooking", None, False, 8))
                return msg
        elif item == "chocolate":
            if (jour.month == 12 and jour.day >= 14) or (jour.month == 1 and jour.day <= 5):
                item = "chocolate"
                gain = "cupcake"
                nbitem = 8
                couldown = GF.couldown_2h
                couldownMsg = ":clock2:`2h`"
            else:
                msg.append("NOK")
                msg.append(lang_P.forge_msg(lang, "cooking", None, False, 9))
                return msg
        elif item == "potato":
            item = "potato"
            gain = "fries"
            nbitem = 6
            couldown = GF.couldown_3h
            couldownMsg = ":clock3:`3h`"
        elif item != "None":
            msg.append("NOK")
            msg.append(lang_P.forge_msg(lang, "cooking", None, False, 7))
            return msg

        sql.updateComTime(PlayerID, "cooking", "gems")
        nbcooking = sql.valueAtNumber(PlayerID, "furnace", "inventory") + 1
        if nbcooking >= max:
            nbcooking = max
        msg.append("OK")
        msg.append(lang)
        msg.append("{}".format(nbcooking))
        while i <= nbcooking:
            data = []
            valueCooking = sql.valueAt(PlayerID, i, "cooking")
            if valueCooking != 0:
                valueTime = float(valueCooking[0])
                valueItem = valueCooking[1]
            else:
                valueTime = 0
                valueItem = ""
            cookingItem = sql.valueAtNumber(PlayerID, item, "inventory")
            if valueItem == "" and item == "None":
                desc = lang_P.forge_msg(lang, "cooking", None, False, 0)
            elif item == "None":
                couldown = GF.couldown_3h
                nbgain = 0
                if valueItem == "pumpkin":
                    gain = "pumpkinpie"
                    nbgain = r.randint(1, 4)
                    couldown = GF.couldown_2h
                elif valueItem == "chocolate":
                    gain = "cupcake"
                    nbgain = r.randint(1, 4)
                    couldown = GF.couldown_2h
                elif valueItem == "potato":
                    gain = "fries"
                    nbgain = r.randint(1, 5)
                    couldown = GF.couldown_3h

                CookedTime = float(valueTime)
                InstantTime = t.time()
                time = CookedTime - (InstantTime-couldown)
                if time <= 0:
                    data = []
                    data.append(0)
                    data.append("")
                    sql.add(PlayerID, gain, nbgain, "inventory")
                    sql.add(PlayerID, "cooking | harvest | item {}".format(gain), nbgain, "statgems")
                    sql.updateField(PlayerID, i, data, "cooking")
                    desc = "{3} {2} <:gem_{0}:{1}>`{0}`".format(gain, "{idmoji[gem_" + gain + "]}", nbgain, lang_P.forge_msg(lang, "cooking", None, False, 1))
                    lvl.addxp(PlayerID, 1, "gems")
                    if i > 1:
                        nbfurnace = int(sql.valueAtNumber(PlayerID, "furnace", "inventory"))
                        if nbfurnace > 0:
                            if sql.valueAtNumber(PlayerID, "furnace", "durability") == 0:
                                for c in GF.objetOutil:
                                    if c.nom == "furnace":
                                        sql.add(PlayerID, "furnace", c.durabilite, "durability")
                            sql.add(PlayerID, "furnace", -1, "durability")
                            if sql.valueAtNumber(PlayerID, "furnace", "durability") <= 0:
                                for c in GF.objetOutil:
                                    if c.nom == "furnace":
                                        sql.add(PlayerID, "furnace", c.durabilite, "durability")
                                sql.add(PlayerID, "furnace", -1, "inventory")
                else:
                    timeH = int(time / 60 / 60)
                    time = time - timeH * 3600
                    timeM = int(time / 60)
                    timeS = int(time - timeM * 60)
                    desc = lang_P.forge_msg(lang, "cooking", [valueItem, "{idmoji[gem_" + valueItem + "]}"], False, 2)
                    desc += lang_P.forge_msg(lang, "cooking", [timeH, timeM, timeS], False, 3)
            else:
                if valueTime == 0:
                    if cookingItem >= nbitem:
                        data = []
                        data.append(str(t.time()))
                        data.append(item)
                        sql.add(PlayerID, i, data, "cooking")
                        sql.add(PlayerID, item, -nbitem, "inventory")
                        sql.add(PlayerID, "cooking | plant | item {}".format(item), nbitem, "statgems")
                        desc = lang_P.forge_msg(lang, "cooking", [couldownMsg], False, 4)
                    else:
                        if item == "pumpkin":
                            gain = "pumpkinpie"
                        elif item == "chocolate":
                            gain = "cupcake"
                        elif item == "potato":
                            gain = "fries"
                        desc = lang_P.forge_msg(lang, "cooking", [item, "{idmoji[gem_" + item + "]}", gain, "{idmoji[gem_" + gain + "]}", nbitem], False, 5)
                else:
                    desc = lang_P.forge_msg(lang, "cooking", [valueItem, "{idmoji[gem_" + valueItem + "]}"], False, 6)
            msg.append("{}".format(i))
            msg.append(desc)
            i += 1
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)])
        msg.append("NOK")
        msg.append(desc)
    return msg
