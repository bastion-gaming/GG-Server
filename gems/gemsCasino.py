import random as r
from DB import SQLite as sql
from gems import gemsFonctions as GF
from core import level as lvl
from languages import lang as lang_P


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


def roulette(param):
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    myV = int(param["valeur"])
    if param["mise"] == "None":
        mise = 20
    else:
        mise = int(param["mise"])
    msg = []
    VM = []
    desc = ""

    if sql.spam(PlayerID, GF.couldown_8s, "roulette", "gems"):
        # Prix du ticket
        sql.addGems(PlayerID, -mise)
        # Vérification que la valeur renseigner par le joueur est présente sur le plateau
        if myV >= 0 and myV < 100:
            # Choix des 4 valeurs maudites
            i = 0
            while i < 4:
                check = True
                V = r.randint(0, 100)
                for one in VM:
                    M = one - 9
                    P = one + 9
                    if V >= M and V <= P:
                        check = False
                if check:
                    VM.append(V)
                    i += 1
            print(myV)
            print("------\n{0}".format(VM))
            # Choix de la valeur bénite
            i = 0
            while i < 1:
                check = True
                VB = r.randint(0, 100)
                for one in VM:
                    M = one - 10
                    P = one + 10
                    if VB >= M and VB <= P:
                        check = False
                if check:
                    i = 1
            print("------\n{0}".format(VB))
            V = myV - VB
            if V >= -5 and V <= 5:
                desc = "Victoire"
                if V < 0:
                    V = -V
                if myV == VB:
                    gain = 2*mise
                else:
                    gain = int(mise + ((10-V)/10)*mise)
            else:
                desc = "Rien"
                gain = 0
                for one in VM:
                    V = myV - one
                    if V >= -5 and V <= 5:
                        desc = "Défaite"
                        if V > 0:
                            V = -V
                        if myV == one:
                            gain = -mise
                        else:
                            gain = int(-((10+V)/10)*mise)
            desc += "\n{0}".format(gain)
            sql.addGems(PlayerID, gain)
            msg.append("OK")
            msg.append(lang)
            msg.append(desc)
            msg.append(VM)
            msg.append(VB)
            return msg
        else:
            msg.append("NOK")
            desc = "Valeur incorrecte!"
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_8s)])
        msg.append("couldown")
    msg.append(lang)
    msg.append(desc)
    return msg


def marketbet(param):
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    msg = []
    desc = ""

    if sql.spam(PlayerID, GF.couldown_8s, "marketbet", "gems"):
        msg.append("OK")
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_8s)])
        msg.append("couldown")
    msg.append(lang)
    msg.append(desc)
    return msg


def weatherbet(param):
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    msg = []
    desc = ""

    if sql.spam(PlayerID, GF.couldown_8s, "weatherbet", "gems"):
        msg.append("OK")
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_8s)])
        msg.append("couldown")
    msg.append(lang)
    msg.append(desc)
    return msg
