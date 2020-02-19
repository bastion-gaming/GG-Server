from operator import itemgetter
import time as t
from DB import SQLite as sql
from core import level as lvl
from gems import gemsFonctions as GF, gemsItems as GI
import json
from languages import lang as lang_P


def begin(param):
    """Pour créer son compte joueur et obtenir son starter Kit!"""
    msg = sql.newPlayer(param["ID"], "gems", param["name_pl"], param["lang"])
    SuperID = sql.get_SuperID(param["ID"], param["name_pl"])
    GF.startKit(SuperID)
    return msg


def bal(param):
    """**[nom]** | Êtes vous riche ou pauvre ?"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    fct = param["fct"]
    msg = []

    if sql.spam(PlayerID, GF.couldown_4s, "bal", "gems"):
        sql.add(PlayerID, "bal", 1, "statgems")
        msg.append("OK")
        msg.append(lang)
        if fct == "info":
            msg.append(lang_P.forge_msg(lang, "PlayerID", [PlayerID]))
        else:
            msg.append(" ")
        solde = sql.valueAtNumber(PlayerID, "gems", "gems")
        desc = "{} :gem:`gems`\n".format(solde)
        soldeSpinelles = sql.valueAtNumber(PlayerID, "spinelles", "gems")
        if soldeSpinelles > 0:
            desc += "{0} <:spinelle:{1}>`spinelles`".format(soldeSpinelles, "{idmoji[spinelle]}")
        msg.append(desc)
        lvlValue = sql.valueAtNumber(PlayerID, "lvl", "gems")
        xp = sql.valueAtNumber(PlayerID, "xp", "gems")
        # Niveaux part
        desc = "XP: `{0}/{1}`".format(xp, lvl.lvlPalier(lvlValue))
        titre = lang_P.forge_msg(lang, "bal", [lvlValue], False)
        msg.append(titre)
        msg.append(desc)
        sql.updateComTime(ID, "bal", "gems")
        # Message de réussite dans la console
        print("Gems >> Balance de {} affichée".format(PlayerID))
    else:
        msg.append("couldown")
        msg.append(lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)]))
    return msg


def baltop(param):
    """**_{filtre}_ [nombre]** | Classement des joueurs (10 premiers par défaut)"""
    n = param["nb"]
    filtre = param["filtre"]
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []
    baltop = ""
    if sql.spam(PlayerID, GF.couldown_4s, "baltop", "gems"):
        sql.updateComTime(PlayerID, "baltop", "gems")
        if filtre == "gems" or filtre == "gem":# or filtre == "spinelles" or filtre == "spinelle":
            UserList = []
            i = 1
            taille = sql.taille("gems")
            while i <= taille:
                user = sql.userID(i, "gems")
                gems = sql.valueAtNumber(i, "gems", "gems")
                spinelles = sql.valueAtNumber(i, "spinelles", "gems")
                guilde = sql.valueAtNumber(i, "guilde", "gems")
                if guilde == None:
                    guilde = ""
                UserList.append((user, gems, spinelles, guilde))
                i = i + 1
            UserList = sorted(UserList, key=itemgetter(1), reverse=True)
            if filtre == "spinelles" or filtre == "spinelle":
                UserList = sorted(UserList, key=itemgetter(2), reverse=True)
            j = 1
            for one in UserList: # affichage des données trié
                if j <= n:
                    baltop += "{2} | _{3} _<@{0}> {1}:gem:".format(one[0], one[1], j, one[3])
                    # if one[2] != 0:
                    #     baltop += " | {0}<:spinelle:{1}>\n".format(one[2], "{idmoji[spinelle]}")
                    # else:
                    #     baltop += "\n"
                    baltop += "\n"
                j += 1
            msg.append("OK")
            msg.append(lang)
            msg.append(baltop)
            sql.add(PlayerID, "baltop", 1, "statgems")
        # elif filtre == "guild" or filtre == "guilde":
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
        #     msg.append("OK")
        #     msg.append(baltop)
        #     sql.add(PlayerID, "baltop | guilde", 1, "statgems")
        else:
            msg.append("NOK")
            msg.append(lang_P.forge_msg(lang, "baltop"))
    else:
        msg.append("couldown")
        msg.append(lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)]))
    return msg


def buy(param):
    """**[item] [nombre]** | Permet d'acheter les items vendus au marché"""
    nb = param["nb"]
    item = param["item"]
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []

    if sql.spam(PlayerID, GF.couldown_4s, "buy", "gems"):
        if int(nb) < 0:
            sql.addGems(PlayerID, -100)
            lvl.addxp(PlayerID, -10, "gems")
            desc = lang_P.forge_msg(lang, "DiscordCop Amende")
            sql.add(PlayerID, "DiscordCop Amende", 1, "statgems")
            msg.append("anticheat")
            msg.append(desc)
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
                                check = True
                            argent = ":gem:`gems`"
                        else:
                            if soldeSpinelles >= prix:
                                sql.addSpinelles(PlayerID, -prix)
                                check = True
                            argent = "<:spinelle:{}>`spinelles`".format("{idmoji[spinelle]}")
                        if check:
                            sql.add(ID, c.nom, nb, "inventory")
                            sql.add(PlayerID, "buy | item | {}".format(c.nom), nb, "statgems")
                            if c.type != "emoji":
                                desc = lang_P.forge_msg(lang, "buy", [nb, c.nom, "{idmoji[gem_" + c.nom + "]}"], False, 0)
                            else:
                                desc = lang_P.forge_msg(lang, "buy", [nb, c.nom], False, 1)
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
                            desc = lang_P.forge_msg(lang, "buy", [nb, c.nom, "{idmoji[gem_" + c.nom + "]}"], False, 0)
                            sql.add(PlayerID, "buy | item | {}".format(c.nom), nb, "statgems")
                            msg.append("bank")
                            msg.append(desc)
                            return msg
                        else:
                            sql.add(PlayerID, c.nom, nb, "inventory")
                            desc = lang_P.forge_msg(lang, "buy", [nb, c.nom, "{idmoji[gem_" + c.nom + "]}"], False, 0)
                            sql.add(PlayerID, "buy | item | {}".format(c.nom), nb, "statgems")
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
                            sql.add(PlayerID, "lootbox_{}".format(c.nom), nb, "inventory")
                            desc = lang_P.forge_msg(lang, "buy", [nb, c.titre, "{idmoji[gem_lootbox]}"], False, 5)
                            sql.add(PlayerID, "buy | item | {}".format(c.titre), nb, "statgems")
                        elif c.type == "spinelle" and sql.addSpinelles(PlayerID, prix) >= "0":
                            sql.add(PlayerID, "lootbox_{}".format(c.nom), nb, "inventory")
                            desc = lang_P.forge_msg(lang, "buy", [nb, c.titre], False, 6)
                            sql.add(PlayerID, "buy | item | {}".format(c.titre), nb, "statgems")
                        else :
                            desc = lang_P.forge_msg(lang, "buy", [":gem:`gems`"], False, 2)
                        break
            if test :
                desc = lang_P.forge_msg(lang, "buy", None, False, 4)
                msg.append("NOK")
            else:
                msg.append("OK")
                sql.add(PlayerID, "buy", 1, "statgems")
            msg.append(desc)

            sql.updateComTime(PlayerID, "buy", "gems")
        else:
            desc = lang_P.forge_msg(lang, "WarningMsg", None, False, 2)
            msg.append("NOK")
            msg.append(desc)
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)])
        msg.append("couldown")
        msg.append(desc)
    return msg


def sell(param):
    """**[item] [nombre]** | Permet de vendre vos items !"""
    nb = param["nb"]
    item = param["item"]
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []

    if sql.spam(PlayerID, GF.couldown_4s, "sell", "gems"):
        nbItem = sql.valueAtNumber(PlayerID, item, "inventory")
        if int(nb) == -1:
            nb = nbItem
        nb = int(nb)
        if nbItem >= nb and nb > 0:
            test = True
            for c in GF.objetItem:
                if item == c.nom:
                    test = False
                    sql.add(PlayerID, "sell | item | {}".format(c.nom), nb, "statgems")
                    gain = c.vente*nb
                    if c.type != "spinelle":
                        sql.addGems(PlayerID, gain)
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
                        argent = ":gem:`gems`"
                    else:
                        sql.addSpinelles(PlayerID, gain)
                        argent = "<:spinelle:{}>`spinelles`".format("{idmoji[spinelle]}")
                    desc = lang_P.forge_msg(lang, "sell", [nb, item, gain, "{idmoji[gem_" + c.nom + "]}", argent], False, 0)
                    sql.add(PlayerID, "sell | item | {}".format(c.nom), nb, "statgems")
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
        sql.add(PlayerID, "sell", 1, "statgems")
        msg.append("OK")
        msg.append(desc)
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)])
        msg.append("couldown")
        msg.append(desc)
    return msg


def inv(param):
    """**[nom de la poche]** | Permet de voir ce que vous avez dans le ventre !"""
    fct = param["fct"]
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []

    if sql.spam(PlayerID, GF.couldown_4s, "inv", "gems"):
        if fct == "None" or fct == "principale" or fct == "main":
            sql.add(PlayerID, "inv", 1, "statgems")
            msg_inv = ""
            msg_invOutils = ""
            msg_invSpeciaux = ""
            msg_invItems = ""
            msg_invItemsMinerai = ""
            msg_invItemsPoisson = ""
            msg_invItemsPlante = ""
            msg_invItemsEvent = ""
            msg_invBox = ""
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
                                msg_invSpeciaux += "<:gem_{0}:{2}>`{0}`: `x{1}` | {5}: `{3}/{4}`\n".format(str(x[1]), str(x[0]), "{idmoji[gem_" + c.nom + "]}", sql.valueAtNumber(PlayerID, c.nom, "durability"), c.durabilite, prop_durabilite)
                            else:
                                msg_invOutils += "<:gem_{0}:{2}>`{0}`: `x{1}` | {5}: `{3}/{4}`\n".format(str(x[1]), str(x[0]), "{idmoji[gem_" + c.nom + "]}", sql.valueAtNumber(PlayerID, c.nom, "durability"), c.durabilite, prop_durabilite)
                            tailletot += c.poids*int(x[0])

            for c in GF.objetItem:
                for x in inv:
                    if c.nom == str(x[1]):
                        if int(x[0]) > 0:
                            if c.type == "minerai":
                                msg_invItemsMinerai += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]), "{idmoji[gem_" + c.nom + "]}")
                            elif c.type == "poisson":
                                msg_invItemsPoisson += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]), "{idmoji[gem_" + c.nom + "]}")
                            elif c.type == "plante":
                                msg_invItemsPlante += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]), "{idmoji[gem_" + c.nom + "]}")
                            elif c.type == "emoji":
                                msg_invItems += ":{0}:`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]))
                            elif c.type == "halloween" or c.type == "christmas" or c.type == "event":
                                msg_invItemsEvent += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]), "{idmoji[gem_" + c.nom + "]}")
                            elif c.type == "spinelle" or c.type == "special":
                                msg_invSpeciaux += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]), "{idmoji[gem_" + c.nom + "]}")
                            else:
                                if c.type == "emoji":
                                    msg_invItems += ":{0}:`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]))
                                else:
                                    msg_invItems += "<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x[1]), str(x[0]), "{idmoji[gem_" + c.nom + "]}")
                            if c.nom == "backpack" or c.nom == "hyperpack":
                                tailleMax += -1 * c.poids * int(x[0])
                            else:
                                tailletot += c.poids*int(x[0])

            for c in GF.objetBox :
                for x in inv:
                    name = "lootbox_{}".format(c.nom)
                    if name == str(x[1]):
                        if int(x[0]) > 0:
                            if c.nom != "gift" and c.nom != "gift_heart":
                                msg_invBox += "<:gem_lootbox:{2}>`{0}`: `x{1}`\n".format(c.nom, str(x[0]), "{idmoji[gem_lootbox]}")
                            else:
                                msg_invBox += ":{0}:`{0}`: `x{1}`\n".format(c.nom, str(x[0]))

            if int(tailletot) >= tailleMax:
                msg_inv += "\n{2}: `{0}/{1}` :bangbang:".format(int(tailletot), tailleMax, prop_taille)
            else:
                msg_inv += "\n{2}: `{0}/{1}`".format(int(tailletot), tailleMax, prop_taille)

            msg.append("OK")
            msg.append(lang)
            msg.append(msg_inv)
            if msg_invOutils == "":
                msg_invOutils = "None"
            if msg_invSpeciaux == "":
                msg_invSpeciaux = "None"
            if msg_invItems == "":
                msg_invItems = "None"
            if msg_invItemsMinerai == "":
                msg_invItemsMinerai = "None"
            if msg_invItemsPoisson == "":
                msg_invItemsPoisson = "None"
            if msg_invItemsPlante == "":
                msg_invItemsPlante = "None"
            if msg_invItemsEvent == "":
                msg_invItemsEvent = "None"
            if msg_invBox == "":
                msg_invBox = "None"
            msg.append(msg_invOutils)
            msg.append(msg_invSpeciaux)
            msg.append(msg_invItems)
            msg.append(msg_invItemsMinerai)
            msg.append(msg_invItemsPoisson)
            msg.append(msg_invItemsPlante)
            msg.append(msg_invItemsEvent)
            msg.append(msg_invBox)

            sql.updateComTime(PlayerID, "inv", "gems")

        elif fct == "pockets" or fct == "poches":
            desc = "• Principale >> `!inv`"
            msg.append("pockets")
            msg.append(lang)
            msg.append(desc)

        else:
            desc = lang_P.forge_msg(lang, "inv", None, False, 0)
            msg.append("NOK")
            msg.append(desc)
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)])
        msg.append("couldown")
        msg.append(desc)
    return msg


def market(param):
    """**[stand]** | Permet de voir tout les objets que l'on peux acheter ou vendre !"""
    fct = param["fct"]
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []

    if sql.spam(PlayerID, GF.couldown_4s, "market", "gems"):
        d_market = "{0}\n\n".format(lang_P.forge_msg(lang, "market", None, False, 2))
        if sql.spam(GF.PlayerID_GetGems, GF.couldown_8h, "bourse", "gems"):
            GF.loadItem()
        ComTime = sql.valueAtNumber(GF.PlayerID_GetGems, "bourse", "gems_com_time")
        time = float(ComTime)
        time = time - (t.time()-GF.couldown_8h)
        timeH = int(time / 60 / 60)
        time = time - timeH * 3600
        timeM = int(time / 60)
        timeS = int(time - timeM * 60)
        d_market += lang_P.forge_msg(lang, "market", [timeH, timeM, timeS], False, 3)
        msg.append("OK")
        msg.append(lang)
        msg.append(d_market)
        prop_achat = lang_P.forge_msg(lang, "propriete", None, False, 0)
        prop_vente = lang_P.forge_msg(lang, "propriete", None, False, 1)
        prop_durabilite = lang_P.forge_msg(lang, "propriete", None, False, 2)
        prop_poids = lang_P.forge_msg(lang, "propriete", None, False, 3)
        prop_taille = lang_P.forge_msg(lang, "propriete", None, False, 4)
        prop_gain = lang_P.forge_msg(lang, "propriete", None, False, 5)

        if fct == "mobile":
            sql.add(PlayerID, "market", 1, "statgems")
            d_marketOutils = ""
            d_marketOutilsS = ""
            d_marketItems = ""
            d_marketItemsMinerai = ""
            d_marketItemsPoisson = ""
            d_marketItemsPlante = ""
            d_marketItemsEvent = ""
            d_marketBox = ""
            d_marketSpinelle = ""

            # récupération du fichier de sauvegarde de la bourse
            with open('gems/bourse.json', 'r') as fp:
                dict = json.load(fp)
            for c in GF.objetOutil:
                for y in GI.PrixOutil:
                    if y.nom == c.nom:
                        temp = dict[c.nom]
                        if y.vente != 0:
                            pourcentageV = ((c.vente*100)//temp["precVente"])-100
                        else:
                            pourcentageV = 0
                        if y.achat != 0:
                            pourcentageA = ((c.achat*100)//temp["precAchat"])-100
                        else:
                            pourcentageA = 0

                if c.type == "consommable" or c.type == "bank":
                    d_marketOutilsS += "<:gem_{0}:{2}>`{0}`: {3} **{1}** ".format(c.nom, c.vente, "{idmoji[gem_" + c.nom + "]}", prop_vente)
                    if pourcentageV != 0:
                        d_marketOutilsS += "_{}%_ ".format(pourcentageV)
                    if c.nom == "bank_upgrade":
                        d_marketOutilsS += "| {0} **{1}** ".format(prop_achat, lang_P.forge_msg(lang, "market", None, False, 0))
                    else:
                        d_marketOutilsS += "| {1} **{0}** ".format(c.achat, prop_achat)
                        if pourcentageA != 0:
                            d_marketOutilsS += "_{}%_ ".format(pourcentageA)
                    if c.durabilite != None:
                        d_marketOutilsS += "| {1}: **{0}**".format(c.durabilite, prop_durabilite)
                    d_marketOutilsS += "\n"
                else:
                    d_marketOutils += "<:gem_{0}:{1}>`{0}`: ".format(c.nom, "{idmoji[gem_" + c.nom + "]}")
                    if c.vente != 0:
                        d_marketOutils += "Vente **{}** ".format(c.vente)
                        if pourcentageV != 0:
                            d_marketOutils += "_{}%_ | ".format(pourcentageV)
                        else:
                            d_marketOutils += "| "
                    d_marketOutils += "{1} **{0}** ".format(c.achat, prop_achat)
                    if pourcentageA != 0:
                        d_marketOutils += "_{}%_ ".format(pourcentageA)
                    if c.durabilite != None:
                        d_marketOutils += "| {1}: **{0}**".format(c.durabilite, prop_durabilite)
                    d_marketOutils += "\n"

            for c in GF.objetItem :
                for y in GI.PrixItem:
                    if y.nom == c.nom:
                        temp = dict[c.nom]
                        if y.vente != 0:
                            try:
                                pourcentageV = ((c.vente*100)//temp["precVente"])-100
                            except:
                                pourcentageV = 404
                        else:
                            pourcentageV = 0
                        if y.achat != 0:
                            try:
                                pourcentageA = ((c.achat*100)//temp["precAchat"])-100
                            except:
                                pourcentageA = 404
                        else:
                            pourcentageA = 0
                # =======================================================================================
                if c.type == "minerai":
                    d_marketItemsMinerai += "<:gem_{0}:{2}>`{0}`: {3} **{1}** ".format(c.nom, c.vente, "{idmoji[gem_" + c.nom + "]}", prop_vente)
                    if pourcentageV != 0:
                        d_marketItemsMinerai += "_{}%_ ".format(pourcentageV)
                    d_marketItemsMinerai += "| {1} **{0}** ".format(c.achat, prop_achat)
                    if pourcentageA != 0:
                        d_marketItemsMinerai += "_{}%_ ".format(pourcentageA)
                    d_marketItemsMinerai += "| {1} **{0}**\n".format(c.poids, prop_poids)
                # =======================================================================================
                elif c.type == "poisson":
                    d_marketItemsPoisson += "<:gem_{0}:{2}>`{0}`: {3} **{1}** ".format(c.nom, c.vente, "{idmoji[gem_" + c.nom + "]}", prop_vente)
                    if pourcentageV != 0:
                        d_marketItemsPoisson += "_{}%_ ".format(pourcentageV)
                    d_marketItemsPoisson += "| {1} **{0}** ".format(c.achat, prop_achat)
                    if pourcentageA != 0:
                        d_marketItemsPoisson += "_{}%_ ".format(pourcentageA)
                    d_marketItemsPoisson += "| {1} **{0}**\n".format(c.poids, prop_poids)
                # =======================================================================================
                elif c.type == "plante":
                    d_marketItemsPlante += "<:gem_{0}:{2}>`{0}`: {3} **{1}** ".format(c.nom, c.vente, "{idmoji[gem_" + c.nom + "]}", prop_vente)
                    if pourcentageV != 0:
                        d_marketItemsPlante += "_{}%_ ".format(pourcentageV)
                    d_marketItemsPlante += "| {1} **{0}** ".format(c.achat, prop_achat)
                    if pourcentageA != 0:
                        d_marketItemsPlante += "_{}%_ ".format(pourcentageA)
                    d_marketItemsPlante += "| {1} **{0}**\n".format(c.poids, prop_poids)
                # =======================================================================================
                elif c.type == "halloween" or c.type == "christmas" or c.type == "event":
                    d_marketItemsEvent += "<:gem_{0}:{2}>`{0}`: {3} **{1}** ".format(c.nom, c.vente, "{idmoji[gem_" + c.nom + "]}", prop_vente)
                    if pourcentageV != 0:
                        d_marketItemsEvent += "_{}%_ ".format(pourcentageV)
                    if c.achat != 0:
                        d_marketItemsEvent += "| {1} **{0}** ".format(c.achat, prop_achat)
                        if pourcentageA != 0:
                            d_marketItemsEvent += "_{}%_ ".format(pourcentageA)
                    d_marketItemsEvent += "| {1} **{0}**\n".format(c.poids, prop_poids)
                # =======================================================================================
                elif c.type == "spinelle":
                    d_marketOutilsS += "<:gem_{0}:{2}>`{0}`: {4} **{1}**<:spinelle:{3}> ".format(c.nom, c.vente, "{idmoji[gem_" + c.nom + "]}", "{idmoji[spinelle]}", prop_vente)
                    d_marketOutilsS += "| {2} **{0}**<:spinelle:{1}> ".format(c.achat, "{idmoji[spinelle]}")
                    d_marketOutilsS += "| {1} **{0}**\n".format(c.poids, prop_poids)
                # =======================================================================================
                elif c.type == "special":
                    d_marketOutilsS += "<:gem_{0}:{2}>`{0}`: {3} **{1}** ".format(c.nom, c.vente, "{idmoji[gem_" + c.nom + "]}", prop_vente)
                    if pourcentageV != 0:
                        d_marketOutilsS += "_{}%_ ".format(pourcentageV)
                    d_marketOutilsS += "| {1} **{0}** ".format(c.achat, prop_achat)
                    if pourcentageA != 0:
                        d_marketOutilsS += "_{}%_ ".format(pourcentageA)
                    d_marketOutilsS += "| {1} **{0}**\n".format(c.poids, prop_poids)
                # =======================================================================================
                else:
                    if c.type == "emoji":
                        d_marketItems += ":{0}:`{0}`: Vente **{1}** ".format(c.nom, c.vente)
                        if pourcentageV != 0:
                            d_marketItems += "_{}%_ ".format(pourcentageV)
                        d_marketItems += "| {1} **{0}** ".format(c.achat, prop_achat)
                        if pourcentageA != 0:
                            d_marketItems += "_{}%_ ".format(pourcentageA)
                        d_marketItems += "| {1} **{0}**\n".format(c.poids, prop_poids)
                    else:
                        d_marketItems += "<:gem_{0}:{2}>`{0}`: {3} **{1}** ".format(c.nom, c.vente, "{idmoji[gem_" + c.nom + "]}", prop_vente)
                        if pourcentageV != 0:
                            d_marketItems += "_{}%_ ".format(pourcentageV)
                        d_marketItems += "| {1} **{0}** ".format(c.achat, prop_achat)
                        if pourcentageA != 0:
                            d_marketItems += "_{}%_ ".format(pourcentageA)
                        d_marketItems += "| {1} **{0}**\n".format(c.poids, prop_poids)

            for c in GF.objetBox :
                if c.nom == "gift":
                    d_marketBox += ":{0}:`{0}`: {2} **{1}:gem:** | {6}: {7}!\n".format(c.nom, c.achat, prop_achat, lang_P.forge_msg(lang, "lootbox", None, False, 5))
                elif c.type == "gems":
                    d_marketBox += "<:gem_lootbox:{4}>`{0}`: {5} **{1}** | {6}: `{2} ▶ {3}`:gem:`gems` \n".format(c.nom, c.achat, c.min, c.max, "{idmoji[gem_lootbox]}", prop_achat, prop_gain)

            msg.append(d_marketOutils)
            msg.append(d_marketOutilsS)
            msg.append(d_marketItemsMinerai)
            msg.append(d_marketItemsPoisson)
            msg.append(d_marketItemsPlante)
            if d_marketItems != "":
                msg.append(d_marketItems)
            else:
                msg.append("None")
            if d_marketItemsEvent != "":
                msg.append(d_marketItemsEvent)
            else:
                msg.append("None")
            if d_marketSpinelle != "":
                msg.append(d_marketSpinelle)
            else:
                msg.append("None")

            msg.append(d_marketBox)
            sql.updateComTime(PlayerID, "market", "gems")
            return msg

        elif fct == "None" or fct == "outil" or fct == "outils" or fct == "item" or fct == "items" or fct == "minerai" or fct == "minerais" or fct == "poissons" or fct == "fish" or fct == "plantes" or fct == "plants" or fct == "event" or fct == "événements" or fct == "lootbox":
            sql.add(PlayerID, "market", 1, "statgems")
            dmMinerai = ""
            dmMineraiPrix = ""
            dmMineraiInfo = ""
            dmPoisson = ""
            dmPoissonPrix = ""
            dmPoissonInfo = ""
            dmPlante = ""
            dmPlantePrix = ""
            dmPlanteInfo = ""
            dmItem = ""
            dmItemPrix = ""
            dmItemInfo = ""
            dmEvent = ""
            dmEventPrix = ""
            dmEventInfo = ""
            dmSpeciaux = ""
            dmSpeciauxPrix = ""
            dmSpeciauxInfo = ""
            dmOutils = ""
            dmOutilsPrix = ""
            dmOutilsInfo = ""
            dmBox = ""
            dmBoxPrix = ""
            dmBoxInfo = ""

            msg.append(fct)

            # récupération du fichier de sauvegarde de la bourse
            with open('gems/bourse.json', 'r') as fp:
                dict = json.load(fp)

            if fct == "None" or fct == "outils" or fct == "outil":
                for c in GF.objetOutil:
                    for y in GI.PrixOutil:
                        if y.nom == c.nom:
                            temp = dict[c.nom]
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
                        dmSpeciaux += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                        if c.type != "bank":
                            dmSpeciauxPrix += "\n`{}`:gem:".format(c.vente)
                            if pourcentageV != 0:
                                dmSpeciauxPrix += " _{}%_ ".format(pourcentageV)
                            dmSpeciauxPrix += " | `{}`:gem:".format(c.achat)
                            if pourcentageA != 0:
                                dmSpeciauxPrix += " _{}%_ ".format(pourcentageA)
                            dmSpeciauxInfo += "\n`{1}: `{0}".format(c.durabilite, prop_durabilite)
                        else:
                            dmSpeciauxPrix += "\n`{0}`".format(lang_P.forge_msg(lang, "market", None, False, 0))
                            dmSpeciauxInfo += "\n`{1}:` {0}".format(c.poids, prop_taille)
                    # =======================================================================================
                    else:
                        dmOutils += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                        dmOutilsPrix += "\n`{}`:gem:".format(c.vente)
                        if pourcentageV != 0:
                            dmOutilsPrix += " _{}%_ ".format(pourcentageV)
                        dmOutilsPrix += " | `{}`:gem:".format(c.achat)
                        if pourcentageA != 0:
                            dmOutilsPrix += " _{}%_ ".format(pourcentageA)
                        dmOutilsInfo += "\n`{1}:` {0}".format(c.durabilite, prop_durabilite)

            if fct == "None" or fct == "item" or fct == "items" or fct == "minerai" or fct == "minerais" or fct == "poissons" or fct == "fish" or fct == "plantes" or fct == "plants" or fct == "event" or fct == "événements":
                for c in GF.objetItem:
                    for y in GI.PrixItem:
                        if y.nom == c.nom:
                            temp = dict[c.nom]
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
                    if c.type == "minerai":
                        dmMinerai += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                        dmMineraiPrix += "\n`{}`:gem:".format(c.vente)
                        if pourcentageV != 0:
                            dmMineraiPrix += " _{}%_ ".format(pourcentageV)
                        dmMineraiPrix += " | `{}`:gem:".format(c.achat)
                        if pourcentageA != 0:
                            dmMineraiPrix += " _{}%_ ".format(pourcentageA)
                        dmMineraiInfo += "\n`{1}:` {0}".format(c.poids, prop_poids)
                    # =======================================================================================
                    elif c.type == "poisson":
                        dmPoisson += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                        dmPoissonPrix += "\n`{}`:gem:".format(c.vente)
                        if pourcentageV != 0:
                            dmPoissonPrix += " _{}%_ ".format(pourcentageV)
                        dmPoissonPrix += " | `{}`:gem:".format(c.achat)
                        if pourcentageA != 0:
                            dmPoissonPrix += " _{}%_ ".format(pourcentageA)
                        dmPoissonInfo += "\n`{1}:` {0}".format(c.poids, prop_poids)
                    # =======================================================================================
                    elif c.type == "plante":
                        dmPlante += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                        dmPlantePrix += "\n`{}`:gem:".format(c.vente)
                        if pourcentageV != 0:
                            dmPlantePrix += " _{}%_ ".format(pourcentageV)
                        dmPlantePrix += " | `{}`:gem:".format(c.achat)
                        if pourcentageA != 0:
                            dmPlantePrix += " _{}%_ ".format(pourcentageA)
                        dmPlanteInfo += "\n`{1}:` {0}".format(c.poids, prop_poids)
                    # =======================================================================================
                    elif c.type == "halloween" or c.type == "christmas" or c.type == "event":
                        dmEvent += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                        dmEventPrix += "\n`{}`:gem:".format(c.vente)
                        if pourcentageV != 0:
                            dmEventPrix += " _{}%_ ".format(pourcentageV)
                        if c.achat != 0:
                            dmEventPrix += " | `{}`:gem:".format(c.achat)
                            if pourcentageA != 0:
                                dmEventPrix += " _{}%_ ".format(pourcentageA)
                        dmEventInfo += "\n`{1}:` {0}".format(c.poids, prop_poids)
                    # =======================================================================================
                    elif c.type == "spinelle":
                        dmSpeciaux += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                        dmSpeciauxPrix += "\n`{prix}`<:spinelle:{idmoji}>".format(prix=c.vente, idmoji="{idmoji[spinelle]}")
                        if pourcentageV != 0:
                            dmSpeciauxPrix += " _{}%_ ".format(pourcentageV)
                        dmSpeciauxPrix += " | `{prix}`<:spinelle:{idmoji}>".format(prix=c.achat, idmoji="{idmoji[spinelle]}")
                        if pourcentageA != 0:
                            dmSpeciauxPrix += " _{}%_ ".format(pourcentageA)
                        dmSpeciauxInfo += "\n`{1}:` {0}".format(c.poids, prop_poids)
                    # =======================================================================================
                    elif c.type == "special":
                        dmSpeciaux += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                        dmSpeciauxPrix += "\n`{}`:gem:".format(c.vente)
                        if pourcentageV != 0:
                            dmSpeciauxPrix += " _{}%_ ".format(pourcentageV)
                        dmSpeciauxPrix += " | `{}`:gem:".format(c.achat)
                        if pourcentageA != 0:
                            dmSpeciauxPrix += " _{}%_ ".format(pourcentageA)
                        dmSpeciauxInfo += "\n`{1}:` {0}".format(c.poids, prop_poids)
                    # =======================================================================================
                    elif c.type == "emoji":
                        dmItem += "\n:{nom}:`{nom}`".format(nom=c.nom)
                        dmItemPrix += "\n`{}`:gem:".format(c.vente)
                        if pourcentageV != 0:
                            dmItemPrix += " _{}%_ ".format(pourcentageV)
                        dmItemPrix += " | `{}`:gem:".format(c.achat)
                        if pourcentageA != 0:
                            dmItemPrix += " _{}%_ ".format(pourcentageA)
                        dmItemInfo += "\n`{1}:` {0}".format(c.poids, prop_poids)
                    # =======================================================================================
                    else:
                        dmItem += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                        dmItemPrix += "\n`{}`:gem:".format(c.vente)
                        if pourcentageV != 0:
                            dmItemPrix += " _{}%_ ".format(pourcentageV)
                        dmItemPrix += " | `{}`:gem:".format(c.achat)
                        if pourcentageA != 0:
                            dmItemPrix += " _{}%_ ".format(pourcentageA)
                        dmItemInfo += "\n`{1}:` {0}".format(c.poids, prop_poids)

            if fct == "None" or fct == "lootbox":
                for c in GF.objetBox :
                    if c.achat != 0:
                        if c.nom == "gift":
                            dmBox += "\n:{nom}:`{nom}`".format(nom=c.nom)
                            dmBoxPrix += "\n`{prix}`:gem:".format(prix=c.achat)
                            dmBoxInfo += "\n{0}!".format(lang_P.forge_msg(lang, "lootbox", None, False, 5))
                        elif c.type == "gems":
                            dmBox += "\n<:gem_lootbox:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_lootbox]}")
                            dmBoxPrix += "\n`{}`:gem:".format(c.achat)
                            dmBoxInfo += "\n`{} ▶ {}`:gem:`gems`".format(c.min, c.max)

            if fct == "None" or fct == "outil" or fct == "outils":
                msg.append(dmOutils)
                msg.append(dmOutilsPrix)
                msg.append(dmOutilsInfo)
            else:
                msg.append("None")
                msg.append("None")
                msg.append("None")

            if fct == "None" or fct == "outils" or fct == "outil" or fct == "item" or fct == "items" or fct == "minerai" or fct == "minerais" or fct == "poissons" or fct == "fish" or fct == "plantes" or fct == "plants" or fct == "event" or fct == "événements":
                if dmSpeciaux != "":
                    msg.append(dmSpeciaux)
                    msg.append(dmSpeciauxPrix)
                    msg.append(dmSpeciauxInfo)
                else:
                    msg.append("None")
                    msg.append("None")
                    msg.append("None")

            if fct == "None" or fct == "minerai" or fct == "minerais":
                msg.append(dmMinerai)
                msg.append(dmMineraiPrix)
                msg.append(dmMineraiInfo)
            else:
                msg.append("None")
                msg.append("None")
                msg.append("None")

            if fct == "None" or fct == "fish" or fct == "poissons":
                msg.append(dmPoisson)
                msg.append(dmPoissonPrix)
                msg.append(dmPoissonInfo)
            else:
                msg.append("None")
                msg.append("None")
                msg.append("None")

            if fct == "None" or fct == "plants" or fct == "plantes":
                msg.append(dmPlante)
                msg.append(dmPlantePrix)
                msg.append(dmPlanteInfo)
            else:
                msg.append("None")
                msg.append("None")
                msg.append("None")

            if fct == "None" or fct == "item" or fct == "items":
                msg.append(dmItem)
                msg.append(dmItemPrix)
                msg.append(dmItemInfo)
            else:
                msg.append("None")
                msg.append("None")
                msg.append("None")

            if fct == "None" or fct == "event" or fct == "événements":
                msg.append(dmEvent)
                msg.append(dmEventPrix)
                msg.append(dmEventInfo)
            else:
                msg.append("None")
                msg.append("None")
                msg.append("None")

            if fct == "None" or fct == "lootbox":
                msg.append(dmBox)
                msg.append(dmBoxPrix)
                msg.append(dmBoxInfo)
            else:
                msg.append("None")
                msg.append("None")
                msg.append("None")

            sql.updateComTime(PlayerID, "market", "gems")
        else:
            desc = lang_P.forge_msg(lang, "market", None, False, 1)
            msg.append("NOK")
            msg.append(desc)
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)])
        msg.append("couldown")
        msg.append(desc)
    return msg


def pay(param):
    """**[Nom_recu] [gain]** | Donner de l'argent à vos amis !"""
    nom = param["nom"]
    gain = param["gain"]
    ID_recu = sql.get_PlayerID(sql.get_SuperID(param["ID_recu"], param["platform"]))
    Nom_recu = param["Nom_recu"]
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []

    if sql.spam(PlayerID, GF.couldown_4s, "pay", "gems"):
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
                    sql.add(PlayerID, "pay", 1, "statgems")
                    sql.add(PlayerID, "pay | nb gems", gain, "statgems")
                else:
                    desc = lang_P.forge_msg(lang, "pay", [nom, gain, Nom_recu], False, 1)

                sql.updateComTime(PlayerID, "pay", "gems")
                msg.append("OK")
            else :
                desc = lang_P.forge_msg(lang, "pay", None, False, 2)
                msg.append("NOK")
        except ValueError:
            desc = lang_P.forge_msg(lang, "WarningMsg", None, False, 3)
            msg.append("NOK")
            pass
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)])
        msg.append("couldown")
    msg.append(desc)
    return msg


def give(param):
    """**[nom] [item] [nombre]** | Donner des items à vos amis !"""
    nom = param["nom"]
    item = param["item"]
    nb = param["nb"]
    ID_recu = sql.get_PlayerID(sql.get_SuperID(param["ID_recu"], param["platform"]))
    Nom_recu = param["Nom_recu"]
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []

    checkLB = False
    if item == "bank_upgrade":
        msg.append("NOK")
        msg.append(lang_P.forge_msg(lang, "give", None, False, 0))
        return msg
        return False
    if sql.spam(PlayerID, GF.couldown_4s, "give", "gems"):
        try:
            if nb == None:
                nb = 1
            else:
                nb = int(nb)
            if nb < 0 and nb != -1:
                sql.addGems(PlayerID, -100)
                desc = lang_P.forge_msg(lang, "DiscordCop Amende")
                sql.add(PlayerID, "DiscordCop Amende", 1, "statgems")
                msg.append("anticheat")
                msg.append(desc)
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
                        sql.add(PlayerID, "give", 1, "statgems")
                        sql.add(PlayerID, "give | nb items", nb, "statgems")
                        sql.add(PlayerID, "give | item | {}".format(item), nb, "statgems")
                    else:
                        desc = lang_P.forge_msg(lang, "give", [Nom_recu], False, 4)
                else:
                    desc = lang_P.forge_msg(lang, "give", [nom, Nom_recu], False, 5)
                msg.append("OK")
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
                        sql.add(PlayerID, "give", 1, "statgems")
                        sql.add(PlayerID, "give | nb items", nb, "statgems")
                    else:
                        desc = lang_P.forge_msg(lang, "give", [Nom_recu], False, 4)
                else:
                    desc = lang_P.forge_msg(lang, "give", [nom, Nom_recu], False, 5)
                msg.append("OK")
            else :
                desc = lang_P.forge_msg(lang, "give", None, False, 6)
                msg.append("NOK")
            sql.updateComTime(PlayerID, "give", "gems")
        except ValueError:
            desc = lang_P.forge_msg(lang, "WarningMsg", None, False, 3)
            msg.append("NOK")
            pass
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)])
        msg.append("couldown")
    msg.append(desc)
    return msg


def forge(param):
    """**[item] [nombre]** | Permet de concevoir des items spécifiques"""
    item = param["item"]
    nb = param["nb"]
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID == "Error 404":
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return msg
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []

    if sql.spam(PlayerID, GF.couldown_4s, "forge", "gems"):
        if GF.testInvTaille(PlayerID):
            # -------------------------------------
            # Affichage des recettes disponible
            if item == "None":
                desc = GF.recette(lang)
                msg.append("OK")
                msg.append(lang)
                msg.append(desc)
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
                                sql.add(PlayerID, "forge", 1, "statgems")
                                sql.add(PlayerID, "forge | nb items", nb, "statgems")
                                sql.add(PlayerID, "forge | item | {}".format(c.nom), nb, "statgems")
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
                                sql.add(PlayerID, "forge", 1, "statgems")
                                sql.add(PlayerID, "forge | nb items", nb, "statgems")
                                sql.add(PlayerID, "forge | item | {}".format(c.nom), nb, "statgems")
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
                                sql.add(PlayerID, "forge", 1, "statgems")
                                sql.add(PlayerID, "forge | nb items", nb, "statgems")
                                sql.add(PlayerID, "forge | item | {}".format(c.nom), nb, "statgems")
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
                                sql.add(PlayerID, "forge", 1, "statgems")
                                sql.add(PlayerID, "forge | nb items", nb, "statgems")
                                sql.add(PlayerID, "forge | item | {}".format(c.nom), nb, "statgems")
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
                        msg.append("OK")
                        msg.append(desc)
                        return msg
                    else:
                        desc = lang_P.forge_msg(lang, "forge", None, False, 2)
                msg.append("NOK")
            sql.updateComTime(PlayerID, "forge", "gems")
        else:
            desc = lang_P.forge_msg(lang, "WarningMsg", None, False, 2)
            msg.append("NOK")
    else:
        desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown_4s)])
        msg.append("couldown")
    msg.append(desc)
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
    PlayerID = sql.get_PlayerID(ID, "gems")
    print(PlayerID)
    msg = []
    langlist = ["EN", "FR"]
    langue = param["langue"].upper()

    if langue == "NONE":
        msg.append("OK")
        msg.append(lang_P.forge_msg(lang, "lang", None, False, 2))
    else:
        if langue in langlist:
            if sql.updateField(ID, "LANG", langue, "IDs") == "200":
                msg.append("OK")
                msg.append(lang_P.forge_msg(langue, "lang", None, False, 0))
            else:
                msg.append("NOK")
                msg.append(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        else:
            msg.append("NOK")
            msg.append(lang_P.forge_msg(lang, "lang", None, False, 1))
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
#     msg = []
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
#             msg.append("NOK")
#             msg.append(desc)
#             return msg
#         if nb < 0:
#             if balspinelle >= -nb:
#                 max = nb
#             else:
#                 desc = "Tu n'as pas assez de <:spinelle:{idmoji}>`spinelles`".format(idmoji="{idmoji[spinelle]}")
#                 msg.append("NOK")
#                 msg.append(desc)
#                 return msg
#         elif nb <= max:
#             max = nb
#         else:
#             desc = "Tu n'as pas assez de :gem:`gems`"
#             msg.append("NOK")
#             msg.append(desc)
#             return msg
#     else:
#         if max == 0:
#             desc = "Tu n'as pas assez de :gem:`gems`"
#             msg.append("NOK")
#             msg.append(desc)
#             return msg
#     sql.addGems(PlayerID, -(max*n))
#     sql.addSpinelles(PlayerID, max)
#     if max > 0:
#         desc = "Convertion terminée! Ton compte a été crédité de {nb} <:spinelle:{idmoji}>`spinelles`".format(nb=max, idmoji="{idmoji[spinelle]}")
#     elif max < 0:
#         desc = "Convertion terminée! Ton compte a été débité de {nb} <:spinelle:{idmoji}>`spinelles`".format(nb=-max, idmoji="{idmoji[spinelle]}")
#     else:
#         desc = "Aucune convertion effectuée"
#     msg.append("OK")
#     msg.append(desc)
#     return msg


# @commands.command(pass_context=True)
# async def trophy(self, ctx, nom = None):
#     """**[nom]** | Liste de vos trophées !"""
#     ID = ctx.author.id
#     if sql.spam(ID,GF.couldown_4s, "trophy", "gems"):
#         if nom != None:
#             ID = sql.nom_ID(nom)
#             nom = ctx.guild.get_member(ID)
#             nom = nom.name
#         else:
#             nom = ctx.author.name
#         d_trophy = ":trophy:Trophées de {}\n\n".format(nom)
#         #-------------------------------------
#         # Récupération de la liste des trophées de ID
#         # et attribution de nouveau trophée si les conditions sont rempli
#         trophy = sql.valueAt(ID, "all", "trophy")
#         for c in GF.objetTrophy:
#             GF.testTrophy(ID, c.nom)
#
#         #-------------------------------------
#         # Affichage des trophées possédés par ID
#         for c in GF.objetTrophy:
#             for x in trophy:
#                 if c.nom == str(x[1]):
#                     if int(x[0]) > 0:
#                         d_trophy += "•**{}**\n".format(c.nom)
#
#         sql.updateComTime(ID, "trophy", "gems")
#         msg = discord.Embed(title = "Trophées",color= 6824352, description = d_trophy)
#         # Message de réussite dans la console
#         print("Gems >> {} a affiché les trophées de {}".format(ctx.author.name,nom))
#         await ctx.channel.send(embed = msg)
#     else:
#         msg = "Il faut attendre " + str(GF.couldown_4s) + " secondes entre chaque commande !"
#         await ctx.channel.send(msg)
#
#
#
# @commands.command(pass_context=True)
# async def trophylist(self, ctx):
#     """Liste de tout les trophées disponibles !"""
#     ID = ctx.author.id
#     d_trophy = "Liste des :trophy:Trophées\n\n"
#     if sql.spam(ID,GF.couldown_6s, "trophylist", "gems"):
#         #-------------------------------------
#         # Affichage des trophées standard
#         for c in GF.objetTrophy:
#             if c.type != "unique" and c.type != "special":
#                 d_trophy += "**{}**: {}\n".format(c.nom, c.desc)
#         d_trophy += "▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
#         #-------------------------------------
#         # Affichage des trophées spéciaux
#         for c in GF.objetTrophy:
#             if c.type != "unique" and c.type == "special":
#                 d_trophy += "**{}**: {}\n".format(c.nom, c.desc)
#         d_trophy += "▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
#         #-------------------------------------
#         # Affichage des trophées uniques
#         for c in GF.objetTrophy:
#             if c.type == "unique" and c.type != "special":
#                 d_trophy += "**{}**: {}\n".format(c.nom, c.desc)
#
#         sql.updateComTime(ID, "trophylist", "gems")
#         msg = discord.Embed(title = "Trophées",color= 6824352, description = d_trophy)
#         # Message de réussite dans la console
#         print("Gems >> {} a affiché la liste des trophées".format(ctx.author.name))
#         await ctx.channel.send(embed = msg)
#     else:
#         msg = "Il faut attendre " + str(GF.couldown_6s) + " secondes entre chaque commande !"
#         await ctx.channel.send(msg)
#
