import random as r
from database import SQLite as sql
from gems import gemsFonctions as GF
from core import level as lvl


def gamble(param):
    """**[valeur]** | Avez vous l'ame d'un parieur ?"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    valeur = int(param["valeur"])
    gems = sql.value(PlayerID, "gems", "Gems")

    if valeur < 0:
        # desc = lang_P.forge_msg(lang, "DiscordCop Amende")
        GF.addStats(PlayerID, ["divers", "DiscordCop Amende"], 1)
        if gems > 100 :
            sql.addGems(PlayerID, -100)
            amende = 100
        else :
            sql.addGems(PlayerID, -gems)
            amende = gems
        return {'error': 1, 'etat': "anticheat", 'lang': lang, 'amende': amende}
    elif valeur > 0 and gems >= valeur:
        if sql.spam(PlayerID, GF.couldown("8s"), "gamble"):
            val = 0-valeur
            sql.addGems(PlayerID, val)
            sql.addGems(GF.PlayerID_GetGems, int(valeur))
            GF.addStats(PlayerID, ["gamble", "gamble | perte"], valeur)

            if r.randint(0, 3) == 0:
                gain = valeur*3
                Taxe = GF.taxe(gain, 0.2)
                try:
                    sql.addGems(GF.PlayerID_GetGems, int(Taxe["taxe"]))
                except:
                    print("Le bot ne fait pas parti de la DB")
                # l'espérence est de 0 sur la gamble
                GF.addStats(PlayerID, ["gamble", "gamble | win"], 1)
                sql.addGems(PlayerID, gain)
                GF.addStats(PlayerID, ["gamble", "gamble | gain"], gain)
                gainmax = sql.value(PlayerID, "statgems", "Stock", "Nom", "gamble | max")
                if gain > gainmax:
                    GF.addStats(PlayerID, ["gamble", "gamble | max"], gain)
            else:
                gain = 0

            sql.updateComTime(PlayerID, "gamble")
            if valeur >= 10000:
                gainXP = 1+(int(valeur//10000))
            else:
                gainXP = 1
            lvl.addxp(PlayerID, gainXP)
            GF.addStats(PlayerID, ["gamble", "gamble"], 1)
            return {'error': 0, 'etat': "OK", 'lang': lang, 'gain': gain, 'XP': gainXP}
        else:
            return {'error': 3, 'etat': "couldown", 'lang': lang, 'couldown': GF.couldown("8s")}
    else:
        return {'error': 2, 'etat': "NOK", 'lang': lang}


def roulette(param):
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    try:
        myV = int(param["valeur"])
    except:
        myV = -1
    try:
        mise = int(param["mise"])
    except:
        mise = 0
    VM = []
    d = dict()
    gems = sql.value(PlayerID, "gems", "Gems")
    niveau = sql.value(PlayerID, "gems", "Level")
    if niveau <= 5:
        d["misemax"] = 50
    else:
        d["misemax"] = int(100*(2**(niveau-5)))
    if int(mise) > d["misemax"]:
        mise = d["misemax"]

    if mise < 0:
        lvl.addxp(PlayerID, -10)
        GF.addStats(PlayerID, ["divers", "DiscordCop Amende"], 1)
        if gems > 100 :
            sql.addGems(PlayerID, -100)
            amende = 100
        else :
            sql.addGems(PlayerID, -gems)
            amende = gems
        return {'error': 2, 'etat': 'anticheat', 'lang': lang, 'amende': amende}

    elif gems < mise:
        return {'error': 3, 'etat': 'NOK', 'lang': lang}

    elif sql.spam(PlayerID, GF.couldown("8s"), "roulette"):
        sql.updateComTime(PlayerID, "roulette")
        # Prix du ticket
        sql.addGems(PlayerID, -mise)
        GF.addStats(PlayerID, ["roulette", "roulette | perte"], mise)
        # Vérification que la valeur renseigner par le joueur est présente sur le plateau
        if myV >= 0 and myV < 100:
            # Choix des 4 valeurs maudites
            i = 0
            while i < 4:
                check = True
                V = r.randint(0, 99)
                for one in VM:
                    M = one - 9
                    P = one + 9
                    if V >= M and V <= P:
                        check = False
                if check:
                    VM.append(V)
                    i += 1
            # print(myV)
            # print("------\n{0}".format(VM))
            # Choix de la valeur bénite
            i = 0
            while i < 1:
                check = True
                VB = r.randint(0, 99)
                for one in VM:
                    M = one - 10
                    P = one + 10
                    if VB >= M and VB <= P:
                        check = False
                if check:
                    i = 1
            # print("------\n{0}".format(VB))
            V = myV - VB
            d['valeurs'] = {'VB': VB, 'myV': myV, 'VM': VM}
            if V >= -5 and V <= 5:
                if V < 0:
                    V = -V
                pourcentage = (10-V)/10
                # desc["desc"] = lang_P.forge_msg(lang, "roulette", [int(pourcentage*100)], False, 1)
                d['etat'] = "Victoire"
                if myV == VB:
                    gain = 2*mise
                else:
                    gain = int(mise + pourcentage*mise)
                d['pourcentage'] = pourcentage*100
                d['gain'] = gain
                d['perte'] = 0
                GF.addStats(PlayerID, ["roulette", "roulette | gain"], gain)
            else:
                # desc["desc"] = lang_P.forge_msg(lang, "roulette", None, False, 0)
                d['etat'] = "Echec"
                gain = 0
                pourcentage = 0
                for one in VM:
                    V = myV - one
                    if V >= -5 and V <= 5:
                        if V < 0:
                            V = -V
                        pourcentage = (10-V)/10
                        # desc["desc"] = lang_P.forge_msg(lang, "roulette", [int(pourcentage*100)], False, 2)
                        d['etat'] = "Defaite"
                        if myV == one:
                            gain = -mise
                        else:
                            gain = int(-(pourcentage*mise))
                d['pourcentage'] = pourcentage*100
                d['gain'] = 0
                d['perte'] = -gain
                GF.addStats(PlayerID, ["roulette", "roulette | perte"], gain)
            sql.addGems(PlayerID, gain)
            if gain > 0:
                gainXP = 1+int(gain//d["misemax"])
            else:
                gainXP = 1
            lvl.addxp(PlayerID, gainXP)
            GF.addStats(PlayerID, ["roulette", "roulette"], 1)
            return {'error': 0, 'etat': 'OK', 'lang': lang, 'roulette': d}
        else:
            return {'error': 4, 'etat': 'NOK', 'lang': lang}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'couldown': GF.couldown("8s")}


def slots(param):
    """**[mise]** | La machine à sous, la mise minimum est de 10 :gem:`gems`"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    imise = param["imise"]
    d = dict()
    gems = sql.value(PlayerID, "gems", "Gems")
    niveau = sql.value(PlayerID, "gems", "Level")
    if niveau <= 5:
        d["misemax"] = 50
    else:
        d["misemax"] = int(100*(2**(niveau-5)))
    if imise != "None":
        if int(imise) < 0:
            lvl.addxp(PlayerID, -10)
            GF.addStats(PlayerID, ["divers", "DiscordCop Amende"], 1)
            if gems > 100 :
                sql.addGems(PlayerID, -100)
                amende = 100
            else :
                sql.addGems(PlayerID, -gems)
                amende = gems
            return {'error': 2, 'etat': 'anticheat', 'lang': lang, 'amende': amende}
        elif int(imise) < 10:
            mise = 10
        elif int(imise) > d["misemax"]:
            mise = d["misemax"]
        else:
            mise = int(imise)
    else:
        mise = 10

    if gems < mise:
        return {'error': 3, 'etat': 'NOK', 'lang': lang}
    elif sql.spam(PlayerID, GF.couldown("8s"), "slots"):
        result = []
        d["mise"] = mise
        val = 0-mise
        slotsItem = [
            "zero", "zero",
            "one", "one",
            "two", "two",
            "three", "three",
            "four", "four",
            "five", "five",
            "six", "six",
            "seven", "seven",
            "eight", "eight",
            "nine", "nine",
            "gem",
            "ticket", "ticket", "ticket",
            "boom", "boom",
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
            nbrand = r.randint(0, LSI-1)
            result.append(slotsItem[nbrand])
        d['result'] = result
        d['ruby'] = False
        d['beer'] = False

        # ===================================================================
        # Attribution des prix
        # ===================================================================
        # Ruby (hyper rare)
        if result[3] == "ruby" or result[4] == "ruby" or result[5] == "ruby":
            GF.addInventory(PlayerID, "ruby", 1)
            GF.addStats(PlayerID, ["slots", "slots | ruby"], 1)
            gain = 16
            d['ruby'] = True
        # ===================================================================
        # Super gain, 3 chiffres identique
        elif result[3] == "seven" and result[4] == "seven" and result[5] == "seven":
            gain = 1000
            GF.addStats(PlayerID, ["slots", "slots | Super Jackpot :seven::seven::seven:"], 1)
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
            GF.addStats(PlayerID, ["slots", "slots | Beer"], 1)
            gain = 5
            d['beer'] = True
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
                GF.addInventory(PlayerID, "cookie", nbCookie)
                GF.addStats(PlayerID, ["slots", "slots | Cookie"], nbCookie)
                d['cookies'] = nbCookie
            else:
                d['cookies'] = 0
        else:
            d['cookies'] = False
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
                GF.addInventory(PlayerID, "grapes", nbGrapes)
                GF.addStats(PlayerID, ["slots", "slots | Grapes"], nbGrapes)
                d['grapes'] = nbGrapes
            else:
                d['grapes'] = 0
        else:
            d['grapes'] = False
        # ===================================================================
        # Backpack (hyper rare)
        if result[3] == "backpack" or result[4] == "backpack" or result[5] == "backpack":
            GF.addInventory(PlayerID, "backpack", 1)
            GF.addStats(PlayerID, ["slots", "slots | Backpack"], 1)
            for c in GF.objetItem:
                if c.nom == "backpack":
                    p = c.poids
            d['backpack'] = p
        else:
            d['backpack'] = False

        # Calcul du prix
        d['gain'] = gain
        d['prix'] = gain * mise
        sql.addGems(PlayerID, val)
        GF.addStats(PlayerID, ["slots", "slots | perte"], mise)
        if gain != 0 and gain != 1:
            if d['prix'] > 0:
                GF.addStats(PlayerID, ["slots", "slots | gain"], d['prix'])
                GF.addStats(PlayerID, ["slots", "slots | win"], 1)
            else:
                GF.addStats(PlayerID, ["slots", "slots | perte"], -d['prix'])
                GF.addStats(PlayerID, ["slots", "slots | lose"], 1)
            sql.addGems(PlayerID, d['prix'])
            sql.addGems(GF.PlayerID_GetGems, -d['prix'])
        elif gain == 1:
            GF.addStats(PlayerID, ["slots", "slots | gain"], d['prix'])
            GF.addStats(PlayerID, ["slots", "slots | win"], 1)
            sql.addGems(PlayerID, d['prix'])
        else:
            GF.addStats(PlayerID, ["slots", "slots | lose"], 1)
        sql.updateComTime(PlayerID, "slots")
        GF.addStats(PlayerID, ["slots", "slots"], 1)
        if gain >= 0:
            d['gainXP'] = 1+int(gain//d["misemax"])
        else:
            d['gainXP'] = 1
        lvl.addxp(PlayerID, d['gainXP'])
        return {'error': 0, 'etat': 'OK', 'lang': lang, 'slots': d}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'couldown': GF.couldown("8s")}
