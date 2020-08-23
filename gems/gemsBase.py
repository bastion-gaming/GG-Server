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
