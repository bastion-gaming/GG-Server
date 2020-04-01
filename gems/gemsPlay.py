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
    lang = param["lang"]
    PlayerID = param["PlayerID"]
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
            f = 200 * (1.1**((DailyMult//30)-1))
            bonus = int(f)
        else:
            bonus = 75
        gain = 100 + int(bonus*DailyMult)
        sql.addGems(PlayerID, gain)
        desc = lang_P.forge_msg(lang, "daily", None, False, 0)
        desc += lang_P.forge_msg(lang, "daily", [DailyMult, int(bonus*DailyMult)], False, 1)
        if DailyMult < 6:
            lvl.addxp(PlayerID, 5, "gems")
        else:
            lvl.addxp(PlayerID, int(5*(DailyMult/6)), "gems")
        if DailyMult % 30 == 0:
            m = int(f*0.3)
            sql.addGems(PlayerID, m)
            desc += lang_P.forge_msg(lang, "daily", [DailyMult, m], False, 2)

    elif DailyTime == str(jour):
        desc = lang_P.forge_msg(lang, "daily", None, False, 3)
    else:
        sql.add(PlayerID, "DailyMult", 1, "daily")
        sql.add(PlayerID, "DailyTime", str(jour), "daily")
        desc = lang_P.forge_msg(lang, "daily", None, False, 0)
        lvl.addxp(PlayerID, 5, "gems")
    msg.append("OK")
    msg.append(lang)
    msg.append(desc)
    return msg


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
    msg = []

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
        msg = bank_bal(PlayerID, lang, ARG, ARG2, Taille, platform)
    elif mARG == "add":
        msg = bank_add(PlayerID, lang, ARG, ARG2, Taille)
    elif mARG == "saving":
        msg = bank_saving(PlayerID, lang, ARG, ARG2, Taille)
    else:
        msg.append("NOK")
        msg.append(lang_P.forge_msg(lang, "WarningMsg", None, False, 1))
    return msg


def bank_bal(PlayerID, lang, ARG, ARG2, Taille, platform):
    """La banque | Balance du compte"""
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
        soldeMult = soldeMax/Taille
        pourcentage = 0.049 + soldeMult*0.001
        if pourcentage > 0.6:
            pourcentage = 0.6
        desc = "{0} / {1} :gem:`gems`\n".format(solde, soldeMax)
        desc += "\n{0}\n".format(lang_P.forge_msg(lang, "bank", [pourcentage*100], False, 14))
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
        msg.append(lang)
        msg.append(desc)
    return msg


def bank_add(PlayerID, lang, ARG, ARG2, Taille):
    """La banque | Crédits"""
    msg = []
    desc = ""
    # =======================================================================
    # Ajoute ou enlève des Gems sur le compte épargne
    # un nombre positif ajoute des Gems
    # un nombre négatif enlève des Gems
    # =======================================================================
    if sql.spam(PlayerID, GF.couldown_4s, "bank_add", "gems"):
        if ARG2 != "None":
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
                    msg.append(lang)
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
    msg.append(lang)
    msg.append(desc)
    return msg


def bank_saving(PlayerID, lang, ARG, ARG2, Taille):
    """La banque | Épargne"""
    msg = []
    desc = ""
    # =======================================================================
    # Fonction d'épargne
    # L'intéret est de 20% avec un bonus de 1% pour chanque bank_upgrade possédée
    # =======================================================================
    if sql.spam(PlayerID, GF.couldown_4h, "bank_saving", "gems"):
        solde = sql.valueAtNumber(PlayerID, "Solde", "bank")
        if solde != 0:
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
            sql.add(PlayerID, ["bank", "bank saving"], 1, "statgems")
            sql.add(PlayerID, ["bank", "bank | saving | gain"], int(soldeAdd), "statgems")
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
            desc = lang_P.forge_msg(lang, "bank", [sql.valueAtNumber(PlayerID, "Solde", "bank")], False, 13)
    else:
        ComTime = sql.valueAtNumber(PlayerID, "bank_saving", "gems_com_time")
        time = float(ComTime) - (t.time()-GF.couldown_4h)
        timeH = int(time / 60 / 60)
        time = time - timeH * 3600
        timeM = int(time / 60)
        timeS = int(time - timeM * 60)
        desc = lang_P.forge_msg(lang, "bank", [timeH, timeM, timeS], False, 12)
    msg.append("saving")
    msg.append(lang)
    msg.append(desc)
    return msg


def stealing(param):
    """**[nom]** | Vole des :gem:`gems` aux autres joueurs!"""
    name = param["name"]
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    msg = []

    if sql.valueAtNumber(GF.PlayerID_GetGems, "DailyMult", "daily") == 1:
        desc = ""
    else:
        if sql.spam(PlayerID, GF.couldown_14h, "stealing", "gems") and name != "None":
            ID_Vol = sql.get_PlayerID(sql.get_SuperID(sql.nom_ID(name), param["name_pl"]))
            # Calcul du pourcentage
            if ID_Vol == GF.PlayerID_GetGems or ID_Vol == GF.PlayerID_Babot:
                R = r.randint(1, 8)
            else:
                R = "05"
            P = float("0.0{}".format(R))
            try:
                Solde = sql.valueAtNumber(ID_Vol, "gems", "gems")
                gain = int(Solde*P)
                if gain != 0:
                    if r.randint(0, 6) == 0:
                        sql.add(PlayerID, ["divers", "DiscordCop Arrestation"], 1, "statgems")
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
                        sql.add(PlayerID, ["stealing", "stealing | gain"], gain, "statgems")
                    sql.updateComTime(PlayerID, "stealing", "gems")
                    lvl.addxp(PlayerID, 1, "gems")
                    sql.add(PlayerID, ["stealing", "stealing"], 1, "statgems")
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
    msg.append(lang)
    msg.append(desc)
    return msg


def crime(param):
    """Commets un crime et gagne des :gem:`gems` Attention au DiscordCop!"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]

    msg = []
    if sql.spam(PlayerID, GF.couldown_6s, "crime", "gems"):
        # si 10 sec c'est écoulé depuis alors on peut en  faire une nouvelle
        if r.randint(0, 9) == 0:
            sql.add(PlayerID, ["divers", "DiscordCop Arrestation"], 1, "statgems")
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
                    sql.add(PlayerID, ["Halloween", "Halloween | crime | candy"], gain, "statgems")
                else:
                    desc += " :lollipop:`lollipop`"
                    sql.add(PlayerID, "lollipop", gain, "inventory")
                    sql.add(PlayerID, ["Halloween", "Halloween | crime | lollipop"], gain, "statgems")
            else:
                desc = "{1} {0} :gem:`gems`".format(gain, lang_P.forge_msg(lang, "crime array", None, True))
                sql.addGems(PlayerID, gain)
                sql.add(PlayerID, ["crime", "crime | gain"], gain, "statgems")
                try:
                    sql.addGems(GF.PlayerID_GetGems, -gain) # Vole l'équivalent du crime au bot
                except sqlite3.OperationalError:
                    pass
                desc += GF.gift(PlayerID, lang)
        sql.updateComTime(PlayerID, "crime", "gems")
        lvl.addxp(PlayerID, 1, "gems")
        sql.add(PlayerID, ["crime", "crime"], 1, "statgems")
        msg.append("OK")
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_6s)])
        msg.append("couldown")
    msg.append(lang)
    msg.append(desc)
    return msg


def gamble(param):
    """**[valeur]** | Avez vous l'ame d'un parieur ?"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    valeur = param["valeur"]
    msg = []
    valeur = int(valeur)

    gems = sql.valueAtNumber(PlayerID, "gems", "gems")
    if valeur < 0:
        desc = lang_P.forge_msg(lang, "DiscordCop Amende")
        sql.add(PlayerID, ["divers", "DiscordCop Amende"], 1, "statgems")
        if gems > 100 :
            sql.addGems(PlayerID, -100)
        else :
            sql.addGems(PlayerID, -gems)
        msg.append("anticheat")
        msg.append(lang)
        msg.append(desc)
        return msg

    elif valeur > 0 and gems >= valeur:
        if sql.spam(PlayerID, GF.couldown_8s, "gamble", "gems"):
            val = 0-valeur
            sql.addGems(PlayerID, val)
            sql.addGems(GF.PlayerID_GetGems, int(valeur))
            sql.add(PlayerID, ["gamble", "gamble | perte"], valeur, "statgems")

            if r.randint(0, 3) == 0:
                gain = valeur*3
                # l'espérence est de 0 sur la gamble
                desc = "{1} {0} :gem:`gems`".format(gain, lang_P.forge_msg(lang, "gamble array", None, True))
                sql.add(PlayerID, ["gamble", "gamble | win"], 1, "statgems")
                sql.addGems(PlayerID, gain)
                sql.add(PlayerID, ["gamble", "gamble | gain"], gain, "statgems")
                gainmax = sql.valueAtNumber(PlayerID, "gamble | max", "statgems")
                if gain > gainmax:
                    if gainmax == 0:
                        sql.add(PlayerID, ["gamble", "gamble | max"], gain, "statgems")
                    else:
                        sql.updateField(PlayerID, "gamble | max", gain, "statgems")
                # =====================================
                # Bonus
                # =====================================
                desc += GF.lootbox(PlayerID, lang)
            else:
                desc = lang_P.forge_msg(lang, "gamble", [valeur], False, 0)

            sql.updateComTime(PlayerID, "gamble", "gems")
            lvl.addxp(PlayerID, 1, "gems")
            sql.add(PlayerID, ["gamble", "gamble"], 1, "statgems")
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
    msg.append(lang)
    msg.append(desc)
    return msg


def mine(param):
    """Minez compagnons !!"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    msg = []
    nbMax = 0
    desc = ""

    if sql.spam(PlayerID, GF.couldown_6s, "mine", "gems"):
        if GF.testInvTaille(PlayerID):
            # =====================================
            # Détection du meilleur outil
            # =====================================
            if sql.valueAtNumber(PlayerID, "diamond_pickaxe", "inventory") >= 1:
                nbMax = 600
                outil = "diamond_pickaxe"
                mult = 2.5

            elif sql.valueAtNumber(PlayerID, "iron_pickaxe", "inventory") >= 1:
                nbMax = 250
                outil = "iron_pickaxe"
                mult = 1.5

            elif sql.valueAtNumber(PlayerID, "pickaxe", "inventory") >= 1:
                nbMax = 100
                outil = "pickaxe"
                mult = 1

            add_item = ""
            if nbMax != 0:
                nbrand = r.randint(1, nbMax)
                # =====================================
                # Gestion de la durabilité de l'outil
                # =====================================
                Durability = GF.durability(PlayerID, outil)
                if Durability:
                    desc = lang_P.forge_msg(lang, "mine", [outil, "{idmoji[gem_" + outil + "]}"], False, 0)
                    sql.add(PlayerID, ["mine", "mine | broken | {}".format(outil)], 1, "statgems")
                    msg.append("OK")
                    msg.append(lang)
                    msg.append(desc)
                    return msg

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
                    sql.add(PlayerID, add_item, nbrand, "inventory")
                    sql.add(PlayerID, ["mine", "mine | item | {}".format(add_item)], nbrand, "statgems")
                    desc = lang_P.forge_msg(lang, "mine", [nbrand, add_item, "{idmoji[gem_" + add_item + "]}"], False, 1)
                    # =====================================
                    # Bonus
                    # =====================================
                    desc += GF.lootbox(PlayerID, lang)
                    desc += GF.gift(PlayerID, lang)
                nbcobble = r.randint(1, 10)
                nbcobble = int(nbcobble*mult)
                sql.add(PlayerID, "cobblestone", nbcobble, "inventory")
                sql.add(PlayerID, ["mine", "mine | item | cobblestone"], nbcobble, "statgems")
                desc += lang_P.forge_msg(lang, "mine", [nbcobble, "{idmoji[gem_cobblestone]}"], False, 2)

                sql.add(PlayerID, ["mine", "mine"], 1, "statgems")

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
    msg.append(lang)
    msg.append(desc)
    return msg


def dig(param):
    """Creusons compagnons !!"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
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
                mult = 2.5

            elif sql.valueAtNumber(PlayerID, "iron_shovel", "inventory") >= 1:
                nbMax = 200
                outil = "iron_shovel"
                mult = 1.5

            elif sql.valueAtNumber(PlayerID, "shovel", "inventory") >= 1:
                nbMax = 100
                outil = "shovel"
                mult = 1

            add_item = ""
            if nbMax != 0:
                nbrand = r.randint(1, nbMax)
                # =====================================
                # Gestion de la durabilité de l'outil
                # =====================================
                Durability = GF.durability(PlayerID, outil)
                if Durability:
                    desc = lang_P.forge_msg(lang, "dig", [outil, "{idmoji[gem_" + outil + "]}"], False, 0)
                    sql.add(PlayerID, ["dig", "dig | broken | {}".format(outil)], 1, "statgems")
                    msg.append("OK")
                    msg.append(lang)
                    msg.append(desc)
                    return msg

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
                    sql.add(PlayerID, add_item, nbrand, "inventory")
                    sql.add(PlayerID, ["dig", "dig | item | {}".format(add_item)], nbrand, "statgems")
                    desc = lang_P.forge_msg(lang, "dig", [nbrand, add_item, "{idmoji[gem_" + add_item + "]}"], False, 1)
                    # =====================================
                    # Bonus
                    # =====================================
                    desc += GF.lootbox(PlayerID, lang)
                    desc += GF.gift(PlayerID, lang)
                else:
                    desc = lang_P.forge_msg(lang, "dig", None, False, 2)

                sql.add(PlayerID, ["dig", "dig"], 1, "statgems")

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
    msg.append(lang)
    msg.append(desc)
    return msg


def fish(param):
    """Péchons compagnons !!"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
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
                    sql.add(PlayerID, ["fish", "fish | fishhook utilisé"], 1, "statgems")
                else:
                    mult = 1

            add_item = ""
            if nbMax != 0:
                nbrand = r.randint(1, nbMax)
                # =====================================
                # Gestion de la durabilité de l'outil
                # =====================================
                Durability = GF.durability(PlayerID, outil)
                if Durability:
                    desc = lang_P.forge_msg(lang, "fish", [outil, "{idmoji[gem_" + outil + "]}"], False, 0)
                    sql.add(PlayerID, ["fish", "fish | broken | {}".format(outil)], 1, "statgems")
                    msg.append("OK")
                    msg.append(lang)
                    msg.append(desc)
                    return msg

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
                        sql.add(PlayerID, add_item, nbrand, "inventory")
                        sql.add(PlayerID, ["fish", "fish | item | {}".format(add_item)], nbrand, "statgems")
                        desc = lang_P.forge_msg(lang, "fish", [nbrand, add_item, "{idmoji[gem_" + add_item + "]}"], False, 1)
                    nb = r.randint(1, 8)
                    nb = int(nb*mult)
                    sql.add(PlayerID, "fish", nb, "inventory")
                    sql.add(PlayerID, ["fish", "fish | item | fish"], nb, "statgems")
                    desc += lang_P.forge_msg(lang, "fish", [nb, "{idmoji[gem_fish]}"], False, 2)
                    # =====================================
                    # Bonus
                    # =====================================
                    desc += GF.lootbox(PlayerID, lang)
                    desc += GF.gift(PlayerID, lang)
                else:
                    desc = lang_P.forge_msg(lang, "fish", None, False, 3)
                    if mult >= 2:
                        sql.add(PlayerID, "fishhook", 1, "inventory")
                        sql.add(PlayerID, ["fish", "fish | fishhook utilisé"], -1, "statgems")

                sql.add(PlayerID, ["fish", "fish"], 1, "statgems")

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
    msg.append(lang)
    msg.append(desc)
    return msg


def slots(param):
    """**[mise]** | La machine à sous, la mise minimum est de 10 :gem:`gems`"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    imise = param["imise"]
    msg = []

    gems = sql.valueAtNumber(PlayerID, "gems", "gems")
    niveau = sql.valueAtNumber(PlayerID, "level", "gems")
    if niveau <= 5:
        misemax = 50
    elif niveau <= 10:
        misemax = 150
    elif niveau <= 15:
        misemax = 360
    else:
        misemax = 500
    if imise != "None":
        if int(imise) < 0:
            desc = lang_P.forge_msg(lang, "DiscordCop Amende")
            lvl.addxp(PlayerID, -10, "gems")
            sql.add(PlayerID, ["divers", "DiscordCop Amende"], 1, "statgems")
            if gems > 100 :
                sql.addGems(PlayerID, -100)
            else :
                sql.addGems(PlayerID, -gems)
            msg.append("anticheat")
            msg.append(lang)
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
        result = []
        desc = lang_P.forge_msg(lang, "slots", [mise], False, 0)
        val = 0-mise
        slotsItem = [
            "zero",
            "zero",
            "one",
            "one",
            "two",
            "two",
            "three",
            "three",
            "four",
            "four",
            "five",
            "five",
            "six",
            "six",
            "seven",
            "seven",
            "eight",
            "eight",
            "nine",
            "nine",
            "gem",
            "ticket",
            "ticket",
            "ticket",
            "boom",
            "boom",
            "apple",
            "green_apple",
            "cherries",
            "tangerine",
            "banana",
            "grapes",
            "cookie",
            "beer",
            "backpack",
            "ruby"
        ]

        # Creation de la machine à sous
        LSI = len(slotsItem)
        for i in range(0, 9):
            if i == 3:
                desc += "\n"
            elif i == 6:
                desc += " :arrow_backward:\n"
            nbrand = r.randint(0, LSI-1)
            result.append(slotsItem[nbrand])
            if nbrand < LSI-2:
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
            sql.add(PlayerID, ["slots", "slots | Ruby"], 1, "statgems")
            gain = 16
            desc += lang_P.forge_msg(lang, "slots", ["{idmoji[gem_ruby]}"], False, 1)
            GF.lootbox(PlayerID, lang)
        # ===================================================================
        # Super gain, 3 chiffres identique
        elif result[3] == "seven" and result[4] == "seven" and result[5] == "seven":
            gain = 1000
            sql.add(PlayerID, ["slots", "slots | Super Jackpot :seven::seven::seven:"], 1, "statgems")
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
            sql.add(PlayerID, ["slots", "slots | Beer"], 1, "statgems")
            gain = 5
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
            gain = 8
        elif (result[3] == "ticket" and result[4] == "ticket") or (result[4] == "ticket" and result[5] == "ticket") or (result[3] == "ticket" and result[5] == "ticket"):
            gain = 4
        elif result[3] == "ticket" or result[4] == "ticket" or result[5] == "ticket":
            gain = 1
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
                sql.add(PlayerID, ["slots", "slots | Cookie"], nbCookie, "statgems")
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
                sql.add(PlayerID, ["slots", "slots | Grapes"], nbGrapes, "statgems")
            else:
                desc += lang_P.forge_msg(lang, "slots", None, False, 5)
        # ===================================================================
        # Backpack (hyper rare)
        if result[3] == "backpack" or result[4] == "backpack" or result[5] == "backpack":
            sql.add(PlayerID, "backpack", 1, "inventory")
            sql.add(PlayerID, ["slots", "slots | Backpack"], 1, "statgems")
            p = 0
            for c in GF.objetItem:
                if c.nom == "backpack":
                    p = c.poids * (-1)
            desc += lang_P.forge_msg(lang, "slots", ["{idmoji[gem_backpack]}", p], False, 7)

        # Calcul du prix
        prix = gain * mise
        sql.addGems(PlayerID, val)
        sql.add(PlayerID, ["slots", "slots | perte"], mise, "statgems")
        if gain != 0 and gain != 1:
            if prix > 400:
                desc += lang_P.forge_msg(lang, "slots", [prix], False, 8)
                sql.add(PlayerID, ["slots", "slots | gain"], prix, "statgems")
                sql.add(PlayerID, ["slots", "slots | win"], 1, "statgems")
            elif prix > 0:
                desc += lang_P.forge_msg(lang, "slots", [prix], False, 9)
                sql.add(PlayerID, ["slots", "slots | gain"], prix, "statgems")
                sql.add(PlayerID, ["slots", "slots | win"], 1, "statgems")
            else:
                desc += lang_P.forge_msg(lang, "slots", [-1*prix], False, 10)
                sql.add(PlayerID, ["slots", "slots | perte"], -prix, "statgems")
                sql.add(PlayerID, ["slots", "slots | lose"], 1, "statgems")
            sql.addGems(PlayerID, prix)
            sql.addGems(GF.PlayerID_GetGems, -prix)
        elif gain == 1:
            desc += lang_P.forge_msg(lang, "slots", None, False, 11)
            sql.add(PlayerID, ["slots", "slots | gain"], prix, "statgems")
            sql.add(PlayerID, ["slots", "slots | win"], 1, "statgems")
            sql.addGems(PlayerID, prix)
        else:
            desc += lang_P.forge_msg(lang, "slots", None, False, 12)
            sql.add(PlayerID, ["slots", "slots | lose"], 1, "statgems")
        sql.updateComTime(PlayerID, "slots", "gems")
        sql.add(PlayerID, ["slots", "slots"], 1, "statgems")
        if gain >= 0:
            lvl.addxp(PlayerID, gain + 1, "gems")
        msg.append("OK")
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_8s)])
        msg.append("couldown")
    msg.append(lang)
    msg.append(desc)
    return msg


def boxes(param):
    """**open [nom]** | Ouverture de Loot Box"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
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
                        sql.add(PlayerID, ["boxes", "boxes | open | {}".format(lootbox.titre)], 1, "statgems")
                        sql.add(PlayerID, ["boxes", "boxes | gain"], gain, "statgems")
                        sql.add(PlayerID, ["boxes", "boxes"], 1, "statgems")
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
    data = []
    desc = ""
    valueOutil = sql.valueAt(PlayerID, i, commande)
    if valueOutil != 0:
        valueTime = float(valueOutil[0])
        valueItem = valueOutil[1]
    else:
        valueTime = 0
        valueItem = ""

    OutilItem = sql.valueAtNumber(PlayerID, item, "inventory")

    if valueItem == "" and item == "None":
        desc = lang_P.forge_msg(lang, commande, None, False, 0)

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
                data = []
                data.append(str(t.time()))
                data.append(item)
                sql.add(PlayerID, i, data, commande)
                sql.add(PlayerID, item, -nbitem, "inventory")
                sql.add(PlayerID, [commande, "{1} | plant | item | {0}".format(item, commande)], nbitem, "statgems")
                if item == "grapes":
                    desc = lang_P.forge_msg(lang, commande, [item, couldownMsg], False, 1)
                else:
                    desc = lang_P.forge_msg(lang, commande, [item, "{idmoji[gem_" + item + "]}", couldownMsg], False, 2)
            else:
                if item == "grapes":
                    desc = lang_P.forge_msg(lang, commande, [item, gain, nbitem], False, 3)
                else:
                    desc = lang_P.forge_msg(lang, commande, [item, "{idmoji[gem_" + item + "]}", gain, nbitem], False, 4)

        else:
            if valueItem == "grapes":
                desc = lang_P.forge_msg(lang, commande, [valueItem], False, 5)
            else:
                desc = lang_P.forge_msg(lang, commande, [valueItem, "{idmoji[gem_" + valueItem + "]}"], False, 6)

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
            data = []
            data.append(0)
            data.append("")
            sql.add(PlayerID, gain, nbgain, "inventory")
            sql.add(PlayerID, [commande, "{1} | harvest | item | {0}".format(gain, commande)], nbgain, "statgems")
            sql.updateField(PlayerID, i, data, commande)
            if gain == "grapes" or gain == "beer" or gain == "wine_glass":
                desc = lang_P.forge_msg(lang, commande, [gain, "{idmoji[gem_" + gain + "]}", nbgain], False, 7)
            else:
                desc = lang_P.forge_msg(lang, commande, [gain, "{idmoji[gem_" + gain + "]}", nbgain], False, 8)
            lvl.addxp(PlayerID, 1, "gems")
            if i > 1:
                GF.durability(PlayerID, outil)
        else:
            restime = GF.time_aff(time)
            if valueItem == "grapes":
                desc = lang_P.forge_msg(lang, commande, [valueItem], False, 5)
            else:
                desc = lang_P.forge_msg(lang, commande, [valueItem, "{idmoji[gem_" + valueItem + "]}"], False, 6)
            desc += lang_P.forge_msg(lang, commande, [restime["timeH"], restime["timeM"], restime["timeS"], restime["cl"]], False, 9)
    else:
        desc = lang_P.forge_msg(lang, commande, None, False, 10)
    return desc


def hothouse(param):
    """**{seed/pumpkin}** | Plantons compagnons !!"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    item = param["item"]
    msg = []
    i = 1
    max = 50

    if sql.spam(PlayerID, GF.couldown_4s, "hothouse", "gems"):
        sql.updateComTime(PlayerID, "hothouse", "gems")
        nboutil = sql.valueAtNumber(PlayerID, "planting_plan", "inventory") + 1
        if nboutil >= max:
            nboutil = max
        msg.append("OK")
        msg.append(lang)
        msg.append("{}".format(nboutil))
        while i <= nboutil:
            msg.append("{}".format(i))
            msg.append(prod_HFC(PlayerID, lang, item, "hothouse", i))
            i += 1
    else:
        msg.append("NOK")
        msg.append(lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)]))
    return msg


def ferment(param):
    """**{grapes/wheat}** | Cave de fermentation. Alcool illimité !!"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    item = param["item"]
    msg = []
    i = 1
    max = 20

    if sql.spam(PlayerID, GF.couldown_4s, "ferment", "gems"):
        sql.updateComTime(PlayerID, "ferment", "gems")
        nboutil = sql.valueAtNumber(PlayerID, "barrel", "inventory") + 1
        if nboutil >= max:
            nboutil = max
        msg.append("OK")
        msg.append(lang)
        msg.append("{}".format(nboutil))
        while i <= nboutil:
            msg.append("{}".format(i))
            msg.append(prod_HFC(PlayerID, lang, item, "ferment", i))
            i += 1
    else:
        msg.append("NOK")
        msg.append(lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)]))
    return msg


def cooking(param):
    """**{potato/pumpkin/chocolate}** | Cuisinons compagnons !!"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    item = param["item"]
    msg = []
    i = 1
    jour = dt.date.today()
    max = 20
    if item == "pumpkin":
        if not ((jour.month == 10 and jour.day >= 26) or (jour.month == 11 and jour.day <= 10)):
            msg.append("NOK")
            msg.append(lang_P.forge_msg(lang, "cooking", None, False, 11))
            return msg
    elif item == "chocolate":
        if not ((jour.month == 12 and jour.day >= 21) or (jour.month == 1 and jour.day <= 14)):
            msg.append("NOK")
            msg.append(lang_P.forge_msg(lang, "cooking", None, False, 12))
            return msg

    if sql.spam(PlayerID, GF.couldown_4s, "cooking", "gems"):
        sql.updateComTime(PlayerID, "cooking", "gems")
        nboutil = sql.valueAtNumber(PlayerID, "furnace", "inventory") + 1
        if nboutil >= max:
            nboutil = max
        msg.append("OK")
        msg.append(lang)
        msg.append("{}".format(nboutil))
        while i <= nboutil:
            msg.append("{}".format(i))
            msg.append(prod_HFC(PlayerID, lang, item, "cooking", i))
            i += 1
    else:
        msg.append("NOK")
        msg.append(lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)]))
    return msg
