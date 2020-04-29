from operator import itemgetter
import time as t
from DB import SQLite as sql
from core import level as lvl
from gems import gemsFonctions as GF, gemsItems as GI
import json
from languages import lang as lang_P


def begin(param):
    """Pour créer son compte joueur et obtenir son starter Kit!"""
    msg = dict()
    name = param["name"]
    while sql.value("IDs", "Pseudo", ["Pseudo"], [name]) is not False:
        name = "User{0}".format(GF.gen_code(4))
    desc = sql.newPlayer(param["ID"], "gems", param["name_pl"], name)
    SuperID = sql.get_SuperID(param["ID"], param["name_pl"])
    GF.startKit(SuperID)
    if desc == lang_P.forge_msg(param["lang"], "newPlayer", None, False, 0):
        msg["type"] = "OK"
        # Message RGPD
        desc += lang_P.forge_msg(param["lang"], "newPlayer", None, False, 2)
    else:
        msg["type"] = "NOK"
    msg["lang"] = param["lang"]
    msg["desc"] = desc
    return msg


def connect(param):
    """Connecter un meme compte sur plusieurs plateforme (commande à effectuer sur la nouvelle plateforme)"""
    lang = param["lang"]
    msg = dict()
    msg["lang"] = lang
    SuperID = sql.get_SuperID(param["ID"], param["name_pl"])
    if SuperID != "Error 404":
        msg["type"] = "NOK"
        msg["desc"] = lang_P.forge_msg(lang, "WarningMsg", None, False, 5)
    else:
        PlayerID = param["PlayerID"]
        msg["type"] = "OK"
        msg["desc"] = lang_P.forge_msg(lang, "WarningMsg", None, False, 4)
    return msg


def infos(param):
    """**[nom]** | Affiche les informations sur un joueur"""
    lang = param["lang"]
    PlayerID = sql.get_PlayerID(sql.get_SuperID(sql.nom_ID(param["ID"]), param["name_pl"]))
    name = param["name"]
    pseudo = sql.valueAtNumber(PlayerID, "Pseudo", "IDs")
    msg = dict()
    desc = ""
    msg["lang"] = lang

    if PlayerID != "Error 404":
        msg["type"] = "OK"

        # PlayerID
        msg["playerid"] = lang_P.forge_msg(lang, "PlayerID", [PlayerID, pseudo])

        # Balance
        solde = sql.valueAtNumber(PlayerID, "gems", "gems")
        desc = "{} :gem:`gems`\n".format(solde)
        soldeSpinelles = sql.valueAtNumber(PlayerID, "spinelles", "gems")
        if soldeSpinelles > 0:
            desc += "{0} <:spinelle:{1}>`spinelles`".format(soldeSpinelles, "{idmoji[spinelle]}")
        msg["balance"] = desc

        # Level et XP
        lvlValue = sql.valueAtNumber(PlayerID, "lvl", "gems")
        xp = sql.valueAtNumber(PlayerID, "xp", "gems")
        # Niveaux part
        msg["lvl"] = lang_P.forge_msg(lang, "bal", [lvlValue], False)
        msg["xp"] = "XP: `{0}/{1}`".format(xp, lvl.lvlPalier(lvlValue))

        # Parrain/Marraine
        P = sql.valueAtNumber(PlayerID, "godparent", "gems")
        Pname = sql.valueAtNumber(P, "Pseudo", "IDs")
        F_li = sql.valueAt(PlayerID, "all", "godchilds")
        desc = ""
        msg["godparent titre"] = lang_P.forge_msg(lang, "godparent", None, False, 2)
        if P != 0 and P != None:
            desc += "\n{1}: **{0}**".format(Pname, lang_P.forge_msg(lang, "godparent", None, False, 0))
        else:
            desc += "\n{0}: `None`".format(lang_P.forge_msg(lang, "godparent", None, False, 0))

        if F_li != 0:
            if len(F_li) > 1:
                sV = "s"
            else:
                sV = ""
            desc += "\n{2}{1} `x{0}`:".format(len(F_li), sV, lang_P.forge_msg(lang, "godparent", None, False, 1))
            for one in F_li:
                Fname = sql.valueAtNumber(one[0], "Pseudo", "IDs")
                desc += "\n• _{0}_".format(Fname)
        msg["godparent"] = desc
        # Message de réussite dans la console
        print("Gems >> Informations de {} affichée".format(name))
    else:
        msg["type"] = "NOK"
        msg["desc"] = lang_P.forge_msg(lang, "WarningMsg", None, False, 6)
    return msg


def username(param):
    """**{new username}** | Change ton nom d'utilisateur!"""
    lang = param["lang"]
    PlayerID = sql.get_PlayerID(sql.get_SuperID(param["ID"], param["name_pl"]))
    msg = dict()
    msg["lang"] = lang

    if sql.spam(PlayerID, GF.couldown("10s"), "username", "gems"):
        if sql.value("IDs", "Pseudo", ["Pseudo"], [param["NU"]]) is False:
            sql.updateField(PlayerID, "Pseudo", param["NU"], "IDs")
            msg["type"] = "OK"
            msg["desc"] = lang_P.forge_msg(lang, "username", None, False, 0)
        else:
            msg["type"] = "NOK"
            msg["desc"] = lang_P.forge_msg(lang, "username", None, False, 1)
        sql.updateComTime(PlayerID, "username", "gems")
    else:
        msg["type"] = "couldown"
        msg["desc"] = lang_P.forge_msg(lang, "couldown", [str(GF.couldown("10s"))])
    return msg


def bal(param):
    """**[nom]** | Êtes vous riche ou pauvre ?"""
    lang = param["lang"]
    PlayerID = sql.get_PlayerID(sql.get_SuperID(param["ID"], param["name_pl"]))
    msg = dict()
    msg["lang"] = lang

    if sql.spam(PlayerID, GF.couldown("4s"), "bal", "gems"):
        msg["type"] = "OK"
        solde = sql.valueAtNumber(PlayerID, "gems", "gems")
        desc = "{} :gem:`gems`\n".format(solde)
        soldeSpinelles = sql.valueAtNumber(PlayerID, "spinelles", "gems")
        if soldeSpinelles > 0:
            desc += "{0} <:spinelle:{1}>`spinelles`".format(soldeSpinelles, "{idmoji[spinelle]}")
        msg["balance"] = desc
        sql.updateComTime(PlayerID, "bal", "gems")
        # Message de réussite dans la console
        print("Gems >> Balance de {} affichée".format(PlayerID))
    else:
        msg["type"] = "couldown"
        msg["desc"] = lang_P.forge_msg(lang, "couldown", [str(GF.couldown("4s"))])
    return msg


def baltop(param):
    """**_{filtre}_ [nombre]** | Classement des joueurs (10 premiers par défaut)"""
    n = param["nb"]
    filtre = param["filtre"]
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    msg = dict()
    msg["lang"] = lang
    baltop = ""
    if sql.spam(PlayerID, GF.couldown("4s"), "baltop", "gems"):
        sql.updateComTime(PlayerID, "baltop", "gems")
        if "gem" in filtre:
            UserList = []
            i = 1
            taille = sql.taille("gems")
            while i <= taille:
                IDs = sql.userID(i, "gems")
                Pseudo = IDs[0]
                IDd = IDs[1]
                IDm = IDs[2]
                if IDd is not None:
                    SuperID = sql.get_SuperID(IDd, "discord")
                elif IDm is not None:
                    SuperID = sql.get_SuperID(IDm, "messenger")
                else:
                    SuperID = 0
                PlayerID = sql.get_PlayerID(SuperID)
                if Pseudo is None or Pseudo == "":
                    user = "<@{0}>".format(IDd)
                else:
                    user = "`{0}`".format(Pseudo)
                gems = sql.valueAtNumber(PlayerID, "gems", "gems")
                spinelles = sql.valueAtNumber(PlayerID, "spinelles", "gems")
                guilde = sql.valueAtNumber(PlayerID, "guilde", "gems")
                if guilde is None or guilde == "":
                    guilde = ""
                else:
                    guilde = guilde.replace("_", " ")
                    guilde = " _{0}_".format(guilde)
                UserList.append((user, gems, spinelles, guilde))
                i = i + 1
            UserList = sorted(UserList, key=itemgetter(1), reverse=True)
            if filtre == "spinelles" or filtre == "spinelle":
                UserList = sorted(UserList, key=itemgetter(2), reverse=True)
            j = 1
            for one in UserList: # affichage des données trié
                if j <= n:
                    baltop += "{2} |{3} {0}: {1} :gem:".format(one[0], one[1], j, one[3])
                    # if one[2] != 0:
                    #     baltop += " | {0} <:spinelle:{1}>\n".format(one[2], "{idmoji[spinelle]}")
                    # else:
                    #     baltop += "\n"
                    baltop += "\n"
                j += 1
            msg["type"] = "OK"
            msg["baltop"] = baltop
        # elif "guild" in filtre:
        #     GuildList = []
        #     i = 1
        #     while i <= DB.get_endDocID("DB/guildesDB"):
        #         try:
        #             GuildList.append((DB.valueAt(i, "Nom", "DB/guildesDB"), DB.valueAt(i, "Spinelles", "DB/guildesDB")))
        #             i += 1
        #         except:
        #             i += 1
        #     GuildList = sorted(GuildList, key=itemgetter(1), reverse=True)
        #     j = 1
        #     for one in GuildList:
        #         if j <= n:
        #             baltop += "{2} | {0} {1} <:spinelle:{3}>\n".format(one[0], one[1], j, "{idmoji[spinelle]}")
        #         j += 1
        #     msg["type"] = "OK"
        #     msg["baltop"] = baltop
        #     sql.add(PlayerID, ["baltop", "baltop | guilde"], 1, "statgems")
        else:
            msg["type"] = "NOK"
            msg["desc"] = lang_P.forge_msg(lang, "baltop")
    else:
        msg["type"] = "couldown"
        msg["desc"] = lang_P.forge_msg(lang, "couldown", [str(GF.couldown("4s"))])
    return msg


def buy(param):
    """**[item] [nombre]** | Permet d'acheter les items vendus au marché"""
    nb = param["nb"]
    item = param["item"]
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    msg = dict()
    msg["lang"] = lang

    if sql.spam(PlayerID, GF.couldown("4s"), "buy", "gems"):
        if int(nb) < 0:
            sql.addGems(PlayerID, -100)
            lvl.addxp(PlayerID, -10, "gems")
            desc = lang_P.forge_msg(lang, "DiscordCop Amende")
            sql.add(PlayerID, ["divers", "DiscordCop Amende"], 1, "statgems")
            msg["type"] = "anticheat"
            msg["desc"] = desc
            return msg

        elif GF.testInvTaille(PlayerID) or item == "backpack" or item == "hyperpack" or item == "bank_upgrade":
            test = True
            nb = int(nb)
            solde = sql.valueAtNumber(PlayerID, "gems", "gems")
            soldeSpinelles = sql.valueAtNumber(PlayerID, "spinelles", "gems")
            for c in GF.objetItem :
                if item == c.nom :
                    test = False
                    check = False
                    if c.achat != 0:
                        prix = (c.achat*nb)
                        if c.type != "spinelle":
                            if solde >= prix:
                                sql.addGems(PlayerID, -prix)
                                sql.add(PlayerID, ["buy", "buy | dépense"], prix, "statgems")
                                check = True
                            argent = ":gem:`gems`"
                        else:
                            if soldeSpinelles >= prix:
                                sql.addSpinelles(PlayerID, -prix)
                                check = True
                            argent = "<:spinelle:{}>`spinelles`".format("{idmoji[spinelle]}")
                        if check:
                            sql.add(PlayerID, c.nom, nb, "inventory")
                            sql.add(PlayerID, ["buy", "buy | item | {}".format(c.nom)], nb, "statgems")
                            sql.add(PlayerID, ["buy", "buy | total"], nb, "statgems")
                            if c.type != "emoji":
                                desc = lang_P.forge_msg(lang, "buy", [nb, c.nom, "{idmoji[gem_" + c.nom + "]}", prix, argent], False, 0)
                            else:
                                desc = lang_P.forge_msg(lang, "buy", [nb, c.nom, prix, argent], False, 1)
                        else :
                            desc = lang_P.forge_msg(lang, "buy", [argent], False, 2)
                    else:
                        desc = lang_P.forge_msg(lang, "buy", None, False, 3)
                    break
            for c in GF.objetOutil :
                if item == c.nom :
                    test = False
                    check = False
                    if c.type == "bank":
                        soldeMax = sql.valueAtNumber(PlayerID, "SoldeMax", "bank")
                        if soldeMax == 0:
                            soldeMax = c.poids
                            sql.add(PlayerID, "soldeMax", c.poids, "bank")
                        soldeMult = soldeMax/c.poids
                        prix = 0
                        i = 1
                        while i <= nb:
                            prix += c.achat*soldeMult
                            soldeMult += 1
                            i += 1
                        prix = int(prix)
                    else:
                        prix = c.achat*nb
                    if c.type != "spinelle":
                        if solde >= prix:
                            sql.addGems(PlayerID, -prix)
                            sql.add(PlayerID, ["buy", "buy | dépense"], prix, "statgems")
                            check = True
                        argent = ":gem:`gems`"
                    else:
                        if soldeSpinelles >= prix:
                            sql.addSpinelles(PlayerID, -prix)
                            check = True
                        argent = "<:spinelle:{}>`spinelles`".format("{idmoji[spinelle]}")
                    if check:
                        if c.type == "bank":
                            sql.add(PlayerID, "SoldeMax", nb*c.poids, "bank")
                            desc = lang_P.forge_msg(lang, "buy", [nb, c.nom, "{idmoji[gem_" + c.nom + "]}", prix, argent], False, 0)
                            sql.add(PlayerID, ["buy", "buy | item | {}".format(c.nom)], nb, "statgems")
                            sql.add(PlayerID, ["buy", "buy | total"], nb, "statgems")
                            msg["type"] = "bank"
                            msg["desc"] = desc
                            return msg
                        else:
                            sql.add(PlayerID, c.nom, nb, "inventory")
                            desc = lang_P.forge_msg(lang, "buy", [nb, c.nom, "{idmoji[gem_" + c.nom + "]}", prix, argent], False, 0)
                            sql.add(PlayerID, ["buy", "buy | item | {}".format(c.nom)], nb, "statgems")
                            sql.add(PlayerID, ["buy", "buy | total"], nb, "statgems")
                            if c.nom != "bank_upgrade":
                                if sql.valueAtNumber(PlayerID, c.nom, "durability") == 0:
                                    sql.add(PlayerID, c.nom, c.durabilite, "durability")
                    else :
                        desc = lang_P.forge_msg(lang, "buy", [argent], False, 2)
                    break
            for c in GF.objetBox :
                if item == "lootbox_{}".format(c.nom) or item == c.nom:
                    if c.nom != "gift_heart":
                        test = False
                        prix = 0 - (c.achat*nb)
                        if c.type == "gems" and sql.addGems(PlayerID, prix) >= "0":
                            sql.add(PlayerID, ["buy", "buy | dépense"], -prix, "statgems")
                            sql.add(PlayerID, "lootbox_{}".format(c.nom), nb, "inventory")
                            desc = lang_P.forge_msg(lang, "buy", [nb, c.titre, "{idmoji[gem_lootbox]}"], False, 5)
                            sql.add(PlayerID, ["buy", "buy | item | {}".format(c.titre)], nb, "statgems")
                            sql.add(PlayerID, ["buy", "buy | total"], nb, "statgems")
                        elif c.type == "spinelle" and sql.addSpinelles(PlayerID, prix) >= "0":
                            sql.add(PlayerID, "lootbox_{}".format(c.nom), nb, "inventory")
                            desc = lang_P.forge_msg(lang, "buy", [nb, c.titre], False, 6)
                            sql.add(PlayerID, ["buy", "buy | item | {}".format(c.titre)], nb, "statgems")
                            sql.add(PlayerID, ["buy", "buy | total"], nb, "statgems")
                        else :
                            desc = lang_P.forge_msg(lang, "buy", [":gem:`gems`"], False, 2)
                        break
            if test :
                desc = lang_P.forge_msg(lang, "buy", None, False, 4)
                msg["type"] = "NOK"
            else:
                msg["type"] = "OK"
                sql.add(PlayerID, ["buy", "buy"], 1, "statgems")

            sql.updateComTime(PlayerID, "buy", "gems")
        else:
            desc = lang_P.forge_msg(lang, "WarningMsg", None, False, 2)
            msg["type"] = "NOK"
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown("4s"))])
        msg["type"] = "couldown"
    msg["desc"] = desc
    return msg


def sell(param):
    """**[item] [nombre]** | Permet de vendre vos items !"""
    nb = param["nb"]
    item = param["item"]
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    msg = dict()
    msg["lang"] = lang

    if sql.spam(PlayerID, GF.couldown("4s"), "sell", "gems"):
        nbItem = sql.valueAtNumber(PlayerID, item, "inventory")
        if int(nb) == -1:
            nb = nbItem
        nb = int(nb)
        if nbItem >= nb and nb > 0:
            test = True
            for c in GF.objetItem:
                if item == c.nom:
                    test = False
                    sql.add(PlayerID, ["sell", "sell | item | {}".format(c.nom)], nb, "statgems")
                    sql.add(PlayerID, ["sell", "sell | total"], nb, "statgems")
                    gain = c.vente*nb
                    if c.type != "spinelle":
                        sql.addGems(PlayerID, gain)
                        sql.add(PlayerID, ["sell", "sell | gain"], gain, "statgems")
                        argent = ":gem:`gems`"
                    else:
                        sql.addSpinelles(PlayerID, gain)
                        argent = "<:spinelle:{}>`spinelles`".format("{idmoji[spinelle]}")
                    if c.type != "emoji":
                        desc = lang_P.forge_msg(lang, "sell", [nb, item, gain, "{idmoji[gem_" + c.nom + "]}", argent], False, 0)
                    else:
                        desc = lang_P.forge_msg(lang, "sell", [nb, item, gain, argent], False, 1)

            for c in GF.objetOutil:
                if item == c.nom:
                    test = False
                    gain = c.vente*nb
                    if c.type != "spinelle":
                        sql.addGems(PlayerID, gain)
                        sql.add(PlayerID, ["sell", "sell | gain"], gain, "statgems")
                        argent = ":gem:`gems`"
                    else:
                        sql.addSpinelles(PlayerID, gain)
                        argent = "<:spinelle:{}>`spinelles`".format("{idmoji[spinelle]}")
                    desc = lang_P.forge_msg(lang, "sell", [nb, item, gain, "{idmoji[gem_" + c.nom + "]}", argent], False, 0)
                    sql.add(PlayerID, ["sell", "sell | item | {}".format(c.nom)], nb, "statgems")
                    sql.add(PlayerID, ["sell", "sell | total"], nb, "statgems")
                    if nbItem == 1:
                        if sql.valueAt(PlayerID, item, "durability") != 0:
                            sql.add(PlayerID, item, -1, "durability")
                    break

            sql.add(PlayerID, item, -nb, "inventory")
            if test:
                desc = lang_P.forge_msg(lang, "sell", None, False, 2)
        else:
            desc = lang_P.forge_msg(lang, "sell", [item, str(sql.valueAtNumber(PlayerID, item, "inventory"))], False, 3)
            for c in GF.objetItem:
                if c.nom == item:
                    if c.type == "emoji":
                        desc = lang_P.forge_msg(lang, "sell", [item, str(sql.valueAtNumber(PlayerID, item, "inventory"))], False, 4)
                    else:
                        desc = lang_P.forge_msg(lang, "sell", [item, str(sql.valueAtNumber(PlayerID, item, "inventory")), "{idmoji[gem_" + c.nom + "]}"], False, 5)
            for c in GF.objetOutil:
                if c.nom == item:
                    if c.type == "bank":
                        desc = lang_P.forge_msg(lang, "sell", ["{idmoji[gem_" + c.nom + "]}", item], False, 6)
                    else:
                        desc = lang_P.forge_msg(lang, "sell", [item, str(sql.valueAtNumber(PlayerID, item, "inventory")), "{idmoji[gem_" + c.nom + "]}"], False, 5)

        sql.updateComTime(PlayerID, "sell", "gems")
        sql.add(PlayerID, ["sell", "sell"], 1, "statgems")
        msg["type"] = "OK"
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown("4s"))])
        msg["type"] = "couldown"
    msg["desc"] = desc
    return msg


def inv(param):
    """**[nom de la poche]** | Permet de voir ce que vous avez dans le ventre !"""
    fct = param["fct"]
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    msg = dict()

    if sql.spam(PlayerID, GF.couldown("4s"), "inv", "gems"):
        if fct == "None" or fct == "principale" or fct == "main":
            # sql.add(PlayerID, ["inv", "inv"], 1, "statgems")
            invD = dict()
            msg_inv = ""
            tailleMax = GF.invMax
            inv = sql.valueAt(PlayerID, "all", "inventory")
            tailletot = 0
            prop_durabilite = lang_P.forge_msg(lang, "propriete", None, False, 2)
            prop_taille = lang_P.forge_msg(lang, "propriete", None, False, 4)
            for c in GF.objetOutil:
                for x in inv:
                    if c.nom == str(x[1]):
                        if int(x[0]) > 0:
                            if c.type == "consommable":
                                type = "special"
                            else:
                                type = "outils"
                            try:
                                invD[type] += "<:gem_{0}:{2}>`{0}`: `x{1}` | {5}: `{3}/{4}`\n".format(str(x[1]), str(x[0]), "{idmoji[gem_" + c.nom + "]}", sql.valueAtNumber(PlayerID, c.nom, "durability"), c.durabilite, prop_durabilite)
                            except KeyError:
                                invD[type] = "<:gem_{0}:{2}>`{0}`: `x{1}` | {5}: `{3}/{4}`\n".format(str(x[1]), str(x[0]), "{idmoji[gem_" + c.nom + "]}", sql.valueAtNumber(PlayerID, c.nom, "durability"), c.durabilite, prop_durabilite)
                            tailletot += c.poids*int(x[0])

            for c in GF.objetItem:
                for x in inv:
                    if c.nom == str(x[1]):
                        if int(x[0]) > 0:
                            if c.type == "halloween" or c.type == "christmas" or c.type == "event":
                                try:
                                    invD["event"] += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]), "{idmoji[gem_" + c.nom + "]}")
                                except KeyError:
                                    invD["event"] = "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]), "{idmoji[gem_" + c.nom + "]}")
                            elif c.type == "emoji":
                                try:
                                    invD["consommable"] += ":{0}:`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]))
                                except KeyError:
                                    invD["consommable"] = ":{0}:`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]))
                            else:
                                try:
                                    invD[c.type] += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]), "{idmoji[gem_" + c.nom + "]}")
                                except KeyError:
                                    invD[c.type] = "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]), "{idmoji[gem_" + c.nom + "]}")

                            if c.nom == "backpack" or c.nom == "hyperpack":
                                tailleMax += -1 * c.poids * int(x[0])
                            else:
                                tailletot += c.poids*int(x[0])

            invD["lootbox"] = ""
            for c in GF.objetBox:
                for x in inv:
                    name = "lootbox_{}".format(c.nom)
                    if name == str(x[1]):
                        if int(x[0]) > 0:
                            if c.nom != "gift" and c.nom != "gift_heart":
                                invD["lootbox"] += "<:gem_lootbox:{2}>`{0}`: `x{1}`\n".format(c.nom, str(x[0]), "{idmoji[gem_lootbox]}")
                            else:
                                invD["lootbox"] += ":{0}:`{0}`: `x{1}`\n".format(c.nom, str(x[0]))

            if int(tailletot) >= tailleMax:
                msg_inv += "\n{2}: `{0}/{1}` :bangbang:".format(int(tailletot), tailleMax, prop_taille)
            else:
                msg_inv += "\n{2}: `{0}/{1}`".format(int(tailletot), tailleMax, prop_taille)

            msg["type"] = "OK"
            msg["lang"] = lang
            msg["desc"] = msg_inv
            msg["inv"] = invD

            sql.updateComTime(PlayerID, "inv", "gems")

        elif "pocket" or "poche" in fct:
            desc = "• Principale >> `!inv`"
            msg["type"] = "pockets"
            msg["lang"] = lang
            msg["desc"] = desc

        else:
            desc = lang_P.forge_msg(lang, "inv", None, False, 0)
            msg["type"] = "NOK"
            msg["lang"] = lang
            msg["desc"] = desc
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown("4s"))])
        msg["type"] = "couldown"
        msg["lang"] = lang
        msg["desc"] = desc
    return msg


def market(param):
    """**[stand]** | Permet de voir tout les objets que l'on peux acheter ou vendre !"""
    fct = param["fct"]
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    msg = dict()
    msg["lang"] = lang

    if sql.spam(PlayerID, GF.couldown("4s"), "market", "gems"):
        d_market = "{0}\n\n".format(lang_P.forge_msg(lang, "market", None, False, 2))
        if sql.spam(GF.PlayerID_GetGems, GF.couldown("8h"), "bourse", "gems"):
            GF.loadItem()
        ComTime = sql.valueAtNumber(GF.PlayerID_GetGems, "bourse", "gems_com_time")
        time = float(ComTime)
        time = time - (t.time()-GF.couldown("8h"))
        timeH = int(time / 60 / 60)
        time = time - timeH * 3600
        timeM = int(time / 60)
        timeS = int(time - timeM * 60)
        d_market += lang_P.forge_msg(lang, "market", [timeH, timeM, timeS], False, 3)
        msg["type"] = "OK"
        msg["desc"] = d_market
        if fct == "mobile":
            prop_achat = "{0} ".format(lang_P.forge_msg(lang, "propriete", None, False, 0))
            prop_vente = "{0} ".format(lang_P.forge_msg(lang, "propriete", None, False, 1))
            prop_gain = "{0} ".format(lang_P.forge_msg(lang, "propriete", None, False, 5))
        else:
            prop_achat = ""
            prop_vente = ""
            prop_gain = ""
        prop_durabilite = lang_P.forge_msg(lang, "propriete", None, False, 2)
        prop_poids = lang_P.forge_msg(lang, "propriete", None, False, 3)
        prop_taille = lang_P.forge_msg(lang, "propriete", None, False, 4)
        msg["special"] = ""
        msg["special prix"] = ""
        msg["special info"] = ""
        msg["outils"] = ""
        msg["outils prix"] = ""
        msg["outils info"] = ""
        msg["items"] = ""
        msg["items prix"] = ""
        msg["items info"] = ""
        msg["event"] = ""
        msg["event prix"] = ""
        msg["event info"] = ""
        msg["lootbox"] = ""
        msg["lootbox prix"] = ""
        msg["lootbox info"] = ""

        # récupération du fichier de sauvegarde de la bourse
        with open('gems/bourse.json', 'r') as fp:
            d = json.load(fp)

        # Les outils
        for c in GF.objetOutil:
            for y in GI.PrixOutil:
                if y.nom == c.nom:
                    temp = d[c.nom]
                    if y.vente != 0:
                        try:
                            pourcentageV = ((c.vente*100)//temp["precVente"])-100
                        except:
                            pourcentageV = 0
                    else:
                        pourcentageV = 0
                    if y.achat != 0:
                        try:
                            pourcentageA = ((c.achat*100)//temp["precAchat"])-100
                        except:
                            pourcentageV = 0
                    else:
                        pourcentageA = 0
            # =======================================================================================
            if c.type == "consommable" or c.type == "bank":
                msg["special"] += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                if c.type != "bank":
                    msg["special prix"] += "\n{1}`{0}`:gem:".format(c.vente, prop_vente)
                    if pourcentageV != 0:
                        msg["special prix"] += " _{0}%_ ".format(pourcentageV)
                    msg["special prix"] += " | {1}`{0}`:gem:".format(c.achat, prop_achat)
                    if pourcentageA != 0:
                        msg["special prix"] += " _{0}%_ ".format(pourcentageA)
                    msg["special info"] += "\n`{1}: `{0}".format(c.durabilite, prop_durabilite)
                else:
                    msg["special prix"] += "\n`{0}`".format(lang_P.forge_msg(lang, "market", None, False, 0))
                    msg["special info"] += "\n`{1}:` {0}".format(c.poids, prop_taille)
            # =======================================================================================
            else:
                msg["outils"] += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                msg["outils prix"] += "\n{1}`{0}`:gem:".format(c.vente, prop_vente)
                if pourcentageV != 0:
                    msg["outils prix"] += " _{0}%_ ".format(pourcentageV)
                msg["outils prix"] += " | {1}`{0}`:gem:".format(c.achat, prop_achat)
                if pourcentageA != 0:
                    msg["outils prix"] += " _{0}%_ ".format(pourcentageA)
                msg["outils info"] += "\n`{1}:` {0}".format(c.durabilite, prop_durabilite)

        # Les items
        for c in GF.objetItem:
            for y in GI.PrixItem:
                if y.nom == c.nom:
                    temp = d[c.nom]
                    if y.vente != 0:
                        try:
                            pourcentageV = ((c.vente*100)//temp["precVente"])-100
                        except:
                            pourcentageV = 0
                    else:
                        pourcentageV = 0
                    if y.achat != 0:
                        try:
                            pourcentageA = ((c.achat*100)//temp["precAchat"])-100
                        except:
                            pourcentageA = 0
                    else:
                        pourcentageA = 0
            # =======================================================================================
            if c.type == "halloween" or c.type == "christmas" or c.type == "event":
                msg["event"] += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                msg["event prix"] += "\n{1}`{0}`:gem:".format(c.vente, prop_vente)
                if pourcentageV != 0:
                    msg["event prix"] += " _{0}%_ ".format(pourcentageV)
                if c.achat != 0:
                    msg["event prix"] += " | {1}`{0}`:gem:".format(c.achat, prop_achat)
                    if pourcentageA != 0:
                        msg["event prix"] += " _{0}%_ ".format(pourcentageA)
                msg["event info"] += "\n`{1}:` {0}".format(c.poids, prop_poids)
            # =======================================================================================
            elif c.type == "emoji" or c.type == "consommable" or c.type == "":
                msg["items"] += "\n:{nom}:`{nom}`".format(nom=c.nom)
                msg["items prix"] += "\n{1}`{0}`:gem:".format(c.vente, prop_vente)
                if pourcentageV != 0:
                    msg["items prix"] += " _{0}%_ ".format(pourcentageV)
                msg["items prix"] += " | {1}`{0}`:gem:".format(c.achat, prop_achat)
                if pourcentageA != 0:
                    msg["items prix"] += " _{0}%_ ".format(pourcentageA)
                msg["items info"] += "\n`{1}:` {0}".format(c.poids, prop_poids)
            # =======================================================================================
            else:
                # Nom de l'item
                try:
                    msg[c.type] += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                except KeyError:
                    msg[c.type] = "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                # Prix de l'item
                try:
                    msg["{0} prix".format(c.type)] += "\n{1}`{0}`:gem:".format(c.vente, prop_vente)
                except KeyError:
                    msg["{0} prix".format(c.type)] = "\n{1}`{0}`:gem:".format(c.vente, prop_vente)
                if pourcentageV != 0:
                    msg["{0} prix".format(c.type)] += " _{0}%_ ".format(pourcentageV)
                try:
                    msg["{0} prix".format(c.type)] += " | {1}`{0}`:gem:".format(c.achat, prop_achat)
                except:
                    msg["{0} prix".format(c.type)] = " | {1}`{0}`:gem:".format(c.achat, prop_achat)
                if pourcentageA != 0:
                    msg["{0} prix".format(c.type)] += " _{0}%_ ".format(pourcentageA)
                # Information sur l'item
                try:
                    msg["{0} info".format(c.type)] += "\n`{1}:` {0}".format(c.poids, prop_poids)
                except KeyError:
                    msg["{0} info".format(c.type)] = "\n`{1}:` {0}".format(c.poids, prop_poids)

        # Lootbox
        for c in GF.objetBox :
            if c.achat != 0:
                if c.nom == "gift":
                    msg["lootbox"] += "\n:{nom}:`{nom}`".format(nom=c.nom)
                    msg["lootbox prix"] += "\n`{prix}`:gem:".format(prix=c.achat)
                    msg["lootbox info"] += "\n{0}!".format(lang_P.forge_msg(lang, "lootbox", None, False, 5))
                elif c.type == "gems":
                    msg["lootbox"] += "\n<:gem_lootbox:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_lootbox]}")
                    msg["lootbox prix"] += "\n{1}`{0}`:gem:".format(c.achat, prop_achat)
                    msg["lootbox info"] += "\n{2}`{0} ▶ {1}`:gem:`gems`".format(c.min, c.max, prop_gain)
        sql.updateComTime(PlayerID, "market", "gems")
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown("4s"))])
        msg["type"] = "couldown"
        msg["desc"] = desc
    return msg


def pay(param):
    """**[Nom_recu] [gain]** | Donner de l'argent à vos amis !"""
    nom = param["nom"]
    gain = param["gain"]
    ID_recu = sql.get_PlayerID(sql.get_SuperID(sql.nom_ID(param["ID_recu"]), param["name_pl"]))
    Nom_recu = param["Nom_recu"]
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    msg = dict()
    msg["lang"] = lang

    if sql.spam(PlayerID, GF.couldown("4s"), "pay", "gems"):
        try:
            if int(gain) > 0:
                gain = int(gain)
                don = -gain
                solde = int(sql.valueAtNumber(PlayerID, "gems", "gems"))
                if solde >= gain:
                    sql.addGems(ID_recu, gain)
                    sql.addGems(PlayerID, don)
                    desc = lang_P.forge_msg(lang, "pay", [nom, gain, Nom_recu], False, 0)
                    # Message de réussite dans la console
                    print("Gems >> {} a donné {} Gems à {}".format(nom, gain, Nom_recu))
                    sql.add(PlayerID, ["pay", "pay"], 1, "statgems")
                    sql.add(PlayerID, ["pay", "pay | nb gems"], gain, "statgems")
                    donmax = sql.valueAtNumber(PlayerID, "pay | don max", "statgems")
                    recumax = sql.valueAtNumber(ID_recu, "pay | recu max", "statgems")
                    if gain > donmax:
                        if donmax == 0:
                            sql.add(PlayerID, ["pay", "pay | don max"], gain, "statgems")
                        else:
                            sql.updateField(PlayerID, "pay | don max", gain, "statgems")
                    if gain > recumax:
                        if recumax == 0:
                            sql.add(ID_recu, ["pay", "pay | recu max"], gain, "statgems")
                        else:
                            sql.updateField(ID_recu, "pay | recu max", gain, "statgems")
                else:
                    desc = lang_P.forge_msg(lang, "pay", [nom, gain, Nom_recu], False, 1)

                sql.updateComTime(PlayerID, "pay", "gems")
                msg["type"] = "OK"
            else :
                desc = lang_P.forge_msg(lang, "pay", None, False, 2)
                msg["type"] = "NOK"
        except ValueError:
            desc = lang_P.forge_msg(lang, "WarningMsg", None, False, 3)
            msg["type"] = "NOK"
            pass
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown("4s"))])
        msg["type"] = "couldown"
    msg["desc"] = desc
    return msg


def give(param):
    """**[nom] [item] [nombre]** | Donner des items à vos amis !"""
    nom = param["nom"]
    item = param["item"]
    nb = param["nb"]
    ID_recu = sql.get_PlayerID(sql.get_SuperID(sql.nom_ID(param["ID_recu"]), param["name_pl"]))
    Nom_recu = param["Nom_recu"]
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    msg = dict()
    msg["lang"] = lang

    checkLB = False
    if item == "bank_upgrade":
        msg["type"] = "NOK"
        msg["desc"] = lang_P.forge_msg(lang, "give", None, False, 0)
        return msg
        return False
    if sql.spam(PlayerID, GF.couldown("4s"), "give", "gems"):
        try:
            if nb == None:
                nb = 1
            else:
                nb = int(nb)
            if nb < 0 and nb != -1:
                sql.addGems(PlayerID, -100)
                desc = lang_P.forge_msg(lang, "DiscordCop Amende")
                sql.add(PlayerID, ["divers", "DiscordCop Amende"], 1, "statgems")
                msg["type"] = "anticheat"
                msg["desc"] = desc
                return msg
            elif nb > 0:
                for lootbox in GF.objetBox:
                    if item == lootbox.nom:
                        checkLB = True
                        itemLB = lootbox.nom
                        item = "lootbox_{}".format(lootbox.nom)
                nbItem = int(sql.valueAtNumber(PlayerID, item, "inventory"))
                if nbItem >= nb and nb > 0:
                    if GF.testInvTaille(ID_recu) or item == "hyperpack" or item == "backpack":
                        sql.add(PlayerID, item, -nb, "inventory")
                        sql.add(ID_recu, item, nb, "inventory")
                        if checkLB:
                            desc = lang_P.forge_msg(lang, "give", [nom, nb, itemLB, "{idmoji[gem_" + itemLB + "]}", Nom_recu], False, 1)
                        else:
                            for c in GF.objetItem:
                                if c.nom == item:
                                    if c.type == "emoji":
                                        desc = lang_P.forge_msg(lang, "give", [nom, nb, item, Nom_recu], False, 2)
                                    else:
                                        desc = lang_P.forge_msg(lang, "give", [nom, nb, item, "{idmoji[gem_" + item + "]}", Nom_recu], False, 3)
                            for c in GF.objetOutil:
                                if c.nom == item:
                                    if c.type == "emoji":
                                        desc = lang_P.forge_msg(lang, "give", [nom, nb, item, Nom_recu], False, 2)
                                    else:
                                        desc = lang_P.forge_msg(lang, "give", [nom, nb, item, "{idmoji[gem_" + item + "]}", Nom_recu], False, 3)
                        # Message de réussite dans la console
                        print("Gems >> {0} a donné {1} {2} à {3}".format(nom, nb, item, Nom_recu))
                        sql.add(PlayerID, ["give", "give"], 1, "statgems")
                        sql.add(PlayerID, ["give", "give | nb items"], nb, "statgems")
                        sql.add(PlayerID, ["give", "give | item | {}".format(item)], nb, "statgems")
                    else:
                        desc = lang_P.forge_msg(lang, "give", [Nom_recu], False, 4)
                else:
                    desc = lang_P.forge_msg(lang, "give", [nom, Nom_recu], False, 5)
                msg["type"] = "OK"
            elif nb == -1:
                nbItem = int(sql.valueAtNumber(PlayerID, item, "inventory"))
                if nb > 0:
                    if GF.testInvTaille(ID_recu) or item == "hyperpack" or item == "backpack":
                        sql.add(PlayerID, item, -nb, "inventory")
                        sql.add(ID_recu, item, nb, "inventory")
                        for c in GF.objetItem:
                            if c.nom == item:
                                if c.type == "emoji":
                                    desc = lang_P.forge_msg(lang, "give", [nom, nb, item, Nom_recu], False, 2)
                                else:
                                    desc = lang_P.forge_msg(lang, "give", [nom, nb, item, "{idmoji[gem_" + item + "]}", Nom_recu], False, 3)
                        for c in GF.objetOutil:
                            if c.nom == item:
                                if c.type == "emoji":
                                    desc = lang_P.forge_msg(lang, "give", [nom, nb, item, Nom_recu], False, 2)
                                else:
                                    desc = lang_P.forge_msg(lang, "give", [nom, nb, item, "{idmoji[gem_" + item + "]}", Nom_recu], False, 3)
                        # Message de réussite dans la console
                        print("Gems >> {0} a donné {1} {2} à {3}".format(nom, nb, item, Nom_recu))
                        sql.add(PlayerID, ["give", "give"], 1, "statgems")
                        sql.add(PlayerID, ["give", "give | nb items"], nb, "statgems")
                    else:
                        desc = lang_P.forge_msg(lang, "give", [Nom_recu], False, 4)
                else:
                    desc = lang_P.forge_msg(lang, "give", [nom, Nom_recu], False, 5)
                msg["type"] = "OK"
            else :
                desc = lang_P.forge_msg(lang, "give", None, False, 6)
                msg["type"] = "NOK"
            sql.updateComTime(PlayerID, "give", "gems")
        except ValueError:
            desc = lang_P.forge_msg(lang, "WarningMsg", None, False, 3)
            msg["type"] = "NOK"
            pass
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown("4s"))])
        msg["type"] = "couldown"
    msg["desc"] = desc
    return msg


def forge(param):
    """**[item] [nombre]** | Permet de concevoir des items spécifiques"""
    item = param["item"]
    nb = param["nb"]
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    msg = dict()
    msg["lang"] = lang

    if sql.spam(PlayerID, GF.couldown("4s"), "forge", "gems"):
        if GF.testInvTaille(PlayerID):
            # -------------------------------------
            # Affichage des recettes disponible
            if item == "None":
                desc = GF.recette(lang)
                msg["type"] = "OK"
                msg["desc"] = desc
                return msg
            # -------------------------------------
            else:
                for c in GF.objetRecette:
                    if item == c.nom:
                        nb = int(nb)
                        nb1 = nb*c.nb1
                        nb2 = nb*c.nb2
                        nb3 = nb*c.nb3
                        nb4 = nb*c.nb4
                        if c.item1 != "" and c.item2 != "" and c.item3 != "" and c.item4 != "":
                            if sql.valueAtNumber(PlayerID, c.item1, "inventory") >= nb1 and sql.valueAtNumber(PlayerID, c.item2, "inventory") >= nb2 and sql.valueAtNumber(PlayerID, c.item3, "inventory") >= nb3 and sql.valueAtNumber(PlayerID, c.item4, "inventory") >= nb4:
                                sql.add(PlayerID, ["forge", "forge"], 1, "statgems")
                                sql.add(PlayerID, ["forge", "forge | nb items"], 1, "statgems")
                                sql.add(PlayerID, ["forge", "forge | item | {}".format(c.nom)], 1, "statgems")
                                sql.add(PlayerID, c.nom, nb, "inventory")
                                sql.add(PlayerID, c.item1, -1*nb1, "inventory")
                                sql.add(PlayerID, c.item2, -1*nb2, "inventory")
                                sql.add(PlayerID, c.item3, -1*nb3, "inventory")
                                sql.add(PlayerID, c.item4, -1*nb4, "inventory")
                                desc = lang_P.forge_msg(lang, "forge", [nb, c.nom, "{idmoji[gem_" + c.nom + "]}"], False, 0)
                                Durability = sql.valueAtNumber(PlayerID, c.nom, "durability")
                                if Durability == 0:
                                    for x in GF.objetOutil:
                                        if x.nom == c.nom:
                                            sql.add(PlayerID, x.nom, x.durabilite, "durability")
                            else:
                                desc = ""
                                if sql.valueAtNumber(PlayerID, c.item1, "inventory") < nb1:
                                    nbmissing = (sql.valueAtNumber(PlayerID, c.item1, "inventory") - nb1)*-1
                                    desc += lang_P.forge_msg(lang, "forge", [nbmissing, c.item1, "{idmoji[gem_" + c.item1 + "]}"], False, 1)
                                if sql.valueAtNumber(PlayerID, c.item2, "inventory") < nb2:
                                    nbmissing = (sql.valueAtNumber(PlayerID, c.item2, "inventory") - nb2)*-1
                                    desc += lang_P.forge_msg(lang, "forge", [nbmissing, c.item2, "{idmoji[gem_" + c.item2 + "]}"], False, 1)
                                if sql.valueAtNumber(PlayerID, c.item3, "inventory") < nb3:
                                    nbmissing = (sql.valueAtNumber(PlayerID, c.item3, "inventory") - nb3)*-1
                                    desc += lang_P.forge_msg(lang, "forge", [nbmissing, c.item3, "{idmoji[gem_" + c.item3 + "]}"], False, 1)
                                if sql.valueAtNumber(PlayerID, c.item4, "inventory") < nb4:
                                    nbmissing = (sql.valueAtNumber(PlayerID, c.item4, "inventory") - nb4)*-1
                                    desc += lang_P.forge_msg(lang, "forge", [nbmissing, c.item4, "{idmoji[gem_" + c.item4 + "]}"], False, 1)

                        elif c.item1 != "" and c.item2 != "" and c.item3 != "":
                            if sql.valueAtNumber(PlayerID, c.item1, "inventory") >= nb1 and sql.valueAtNumber(PlayerID, c.item2, "inventory") >= nb2 and sql.valueAtNumber(PlayerID, c.item3, "inventory") >= nb3:
                                sql.add(PlayerID, ["forge", "forge"], 1, "statgems")
                                sql.add(PlayerID, ["forge", "forge | nb items"], 1, "statgems")
                                sql.add(PlayerID, ["forge", "forge | item | {}".format(c.nom)], 1, "statgems")
                                sql.add(PlayerID, c.nom, nb, "inventory")
                                sql.add(PlayerID, c.item1, -1*nb1, "inventory")
                                sql.add(PlayerID, c.item2, -1*nb2, "inventory")
                                sql.add(PlayerID, c.item3, -1*nb3, "inventory")
                                desc = lang_P.forge_msg(lang, "forge", [nb, c.nom, "{idmoji[gem_" + c.nom + "]}"], False, 0)
                                Durability = sql.valueAtNumber(PlayerID, c.nom, "durability")
                                if Durability == 0:
                                    for x in GF.objetOutil:
                                        if x.nom == c.nom:
                                            sql.add(PlayerID, x.nom, x.durabilite, "durability")
                            else:
                                desc = ""
                                if sql.valueAtNumber(PlayerID, c.item1, "inventory") < nb1:
                                    nbmissing = (sql.valueAtNumber(PlayerID, c.item1, "inventory") - nb1)*-1
                                    desc += lang_P.forge_msg(lang, "forge", [nbmissing, c.item1, "{idmoji[gem_" + c.item1 + "]}"], False, 1)
                                if sql.valueAtNumber(PlayerID, c.item2, "inventory") < nb2:
                                    nbmissing = (sql.valueAtNumber(PlayerID, c.item2, "inventory") - nb2)*-1
                                    desc += lang_P.forge_msg(lang, "forge", [nbmissing, c.item2, "{idmoji[gem_" + c.item2 + "]}"], False, 1)
                                if sql.valueAtNumber(PlayerID, c.item3, "inventory") < nb3:
                                    nbmissing = (sql.valueAtNumber(PlayerID, c.item3, "inventory") - nb3)*-1
                                    desc += lang_P.forge_msg(lang, "forge", [nbmissing, c.item3, "{idmoji[gem_" + c.item3 + "]}"], False, 1)

                        elif c.item1 != "" and c.item2 != "":
                            if sql.valueAtNumber(PlayerID, c.item1, "inventory") >= nb1 and sql.valueAtNumber(PlayerID, c.item2, "inventory") >= nb2:
                                sql.add(PlayerID, ["forge", "forge"], 1, "statgems")
                                sql.add(PlayerID, ["forge", "forge | nb items"], 1, "statgems")
                                sql.add(PlayerID, ["forge", "forge | item | {}".format(c.nom)], 1, "statgems")
                                sql.add(PlayerID, c.nom, nb, "inventory")
                                sql.add(PlayerID, c.item1, -1*nb1, "inventory")
                                sql.add(PlayerID, c.item2, -1*nb2, "inventory")
                                desc = lang_P.forge_msg(lang, "forge", [nb, c.nom, "{idmoji[gem_" + c.nom + "]}"], False, 0)
                                Durability = sql.valueAtNumber(PlayerID, c.nom, "durability")
                                if Durability == 0:
                                    for x in GF.objetOutil:
                                        if x.nom == c.nom:
                                            sql.add(PlayerID, x.nom, x.durabilite, "durability")
                            else:
                                desc = ""
                                if sql.valueAtNumber(PlayerID, c.item1, "inventory") < nb1:
                                    nbmissing = (sql.valueAtNumber(PlayerID, c.item1, "inventory") - nb1)*-1
                                    desc += lang_P.forge_msg(lang, "forge", [nbmissing, c.item1, "{idmoji[gem_" + c.item1 + "]}"], False, 1)
                                if sql.valueAtNumber(PlayerID, c.item2, "inventory") < nb2:
                                    nbmissing = (sql.valueAtNumber(PlayerID, c.item2, "inventory") - nb2)*-1
                                    desc += lang_P.forge_msg(lang, "forge", [nbmissing, c.item2, "{idmoji[gem_" + c.item2 + "]}"], False, 1)

                        elif c.item1 != "":
                            if sql.valueAtNumber(PlayerID, c.item1, "inventory") >= nb1:
                                sql.add(PlayerID, ["forge", "forge"], 1, "statgems")
                                sql.add(PlayerID, ["forge", "forge | nb items"], 1, "statgems")
                                sql.add(PlayerID, ["forge", "forge | item | {}".format(c.nom)], 1, "statgems")
                                sql.add(PlayerID, c.nom, nb, "inventory")
                                sql.add(PlayerID, c.item1, -1*nb1, "inventory")
                                desc = lang_P.forge_msg(lang, "forge", [nb, c.nom, "{idmoji[gem_" + c.nom + "]}"], False, 0)
                                Durability = sql.valueAtNumber(PlayerID, c.nom, "durability")
                                if Durability == 0:
                                    for x in GF.objetOutil:
                                        if x.nom == c.nom:
                                            sql.add(PlayerID, x.nom, x.durabilite, "durability")
                            else:
                                nbmissing = (sql.valueAtNumber(PlayerID, c.item1, "inventory") - nb1)*-1
                                desc = lang_P.forge_msg(lang, "forge", [nbmissing, c.item1, "{idmoji[gem_" + c.item1 + "]}"], False, 1)
                        msg["type"] = "OK"
                        msg["desc"] = desc
                        return msg
                    else:
                        desc = lang_P.forge_msg(lang, "forge", None, False, 2)
                msg["type"] = "NOK"
            sql.updateComTime(PlayerID, "forge", "gems")
        else:
            desc = lang_P.forge_msg(lang, "WarningMsg", None, False, 2)
            msg["type"] = "NOK"
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown("4s"))])
        msg["type"] = "couldown"
    msg["desc"] = desc
    return msg


def lang(param):
    """
    Permet de changer la langue pour un joueur.
    """
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    msg = dict()
    langlist = ["EN", "FR"]
    langue = param["langue"].upper()

    if langue == "NONE":
        msg["type"] = "OK"
        msg["desc"] = lang_P.forge_msg(lang, "lang", None, False, 2)
    else:
        if langue in langlist:
            if sql.updateField(ID, "LANG", langue, "IDs") == "200":
                msg["type"] = "OK"
                msg["desc"] = lang_P.forge_msg(langue, "lang", None, False, 0)
            else:
                msg["type"] = "NOK"
                msg["desc"] = lang_P.forge_msg(lang, "WarningMsg", None, False, 0)
        else:
            msg["type"] = "NOK"
            msg["desc"] = lang_P.forge_msg(lang, "lang", None, False, 1)
    return msg


def godparent(param):
    """Permet d'ajouter un joueur comme parrain. En le faisant vous touchez un bonus et lui aussi"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    GPID = sql.get_PlayerID(sql.get_SuperID(sql.nom_ID(param["GPID"]), param["name_pl"]))
    msg = dict()
    msg["lang"] = lang
    myGP = sql.valueAtNumber(PlayerID, "godparent", "gems")

    if (myGP == 0 or myGP == None) and PlayerID != GPID and GPID != "Error 404":
        sql.updateField(PlayerID, "godparent", GPID, "gems")
        sql.add(GPID, PlayerID, 1, "godchilds")
        lvl.addxp(PlayerID, 15, "gems")
        sql.addGems(PlayerID, 100)
        fil_L = sql.valueAt(GPID, "all", "godchilds")
        gainXP = 15 * len(fil_L)
        gainG = 100 * len(fil_L)
        lvl.addxp(GPID, gainXP, "gems")
        sql.addGems(GPID, gainG)
        msg["type"] = "OK"
        msg["desc"] = lang_P.forge_msg(lang, "godparent", [gainG], False, 3)
    elif myGP != 0 and myGP != None:
        msg["type"] = "NOK"
        msg["desc"] = lang_P.forge_msg(lang, "godparent", None, False, 4)
    else:
        msg["type"] = "NOK"
        msg["desc"] = lang_P.forge_msg(lang, "godparent", None, False, 5)
    return msg


# ==============================
# ===== Commande désactivé =====
# ==============================
# def convert(param):
#     """**[Nombre de spinelle]** | Convertisseur :gem:`gems` :left_right_arrow: `spinelles` (250 000 pour 1)"""
#     nb = param["nb"]
#     ID = sql.get_SuperID(param["ID"], param["name_pl"])
#     lang = param["langue"].upper()
#     if ID == "Error 404":
#         msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
#         return msg
#     PlayerID = sql.get_PlayerID(ID, "gems")
#     msg = dict()
#     msg["lang"] = lang
#
#     n = 250000
#     balGems = sql.valueAtNumber(PlayerID, "gems", "gems")
#     balspinelle = sql.valueAtNumber(PlayerID, "spinelles", "gems")
#     max = balGems // n
#     if nb != "None":
#         try:
#             nb = int(nb)
#         except:
#             desc = "Erreur! Nombre de <:spinelle:{idmoji}>`spinelles` incorrect".format(idmoji = "{idmoji[spinelle]}")
#             msg["type"] = "NOK"
#             msg["desc"] = desc
#             return msg
#         if nb < 0:
#             if balspinelle >= -nb:
#                 max = nb
#             else:
#                 desc = "Tu n'as pas assez de <:spinelle:{idmoji}>`spinelles`".format(idmoji="{idmoji[spinelle]}")
#                 msg["type"] = "NOK"
#                 msg["desc"] = desc
#                 return msg
#         elif nb <= max:
#             max = nb
#         else:
#             desc = "Tu n'as pas assez de :gem:`gems`"
#             msg["type"] = "NOK"
#             msg["desc"] = desc
#             return msg
#     else:
#         if max == 0:
#             desc = "Tu n'as pas assez de :gem:`gems`"
#             msg["type"] = "NOK"
#             msg["desc"] = desc
#             return msg
#     sql.addGems(PlayerID, -(max*n))
#     sql.addSpinelles(PlayerID, max)
#     if max > 0:
#         desc = "Convertion terminée! Ton compte a été crédité de {nb} <:spinelle:{idmoji}>`spinelles`".format(nb=max, idmoji="{idmoji[spinelle]}")
#     elif max < 0:
#         desc = "Convertion terminée! Ton compte a été débité de {nb} <:spinelle:{idmoji}>`spinelles`".format(nb=-max, idmoji="{idmoji[spinelle]}")
#     else:
#         desc = "Aucune convertion effectuée"
#     msg["type"] = "OK"
#     msg["desc"] = desc
#     return msg
