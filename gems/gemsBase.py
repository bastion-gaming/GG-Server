import os
from operator import itemgetter
import random as r
import time as t
import datetime as dt
from DB import SQLite as sql, TinyDB as DB
from core import level as lvl
from gems import gemsFonctions as GF, gemsItems as GI, gemsStats as GS
import json


def begin(param):
    """Pour créer son compte joueur et obtenir son starter Kit!"""
    msg = sql.newPlayer(param["ID"], "gems", param["name_pl"])
    SuperID = sql.get_SuperID(param["ID"], param["name_pl"])
    GF.startKit(SuperID)
    return msg


def bal(param):
    """**[nom]** | Êtes vous riche ou pauvre ?"""
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []

    if sql.spam(PlayerID, GF.couldown_4s, "bal", "gems"):
        msg.append("OK")
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
        titre = "**_Niveau_: {0}**".format(lvlValue)
        msg.append(titre)
        msg.append(desc)
        sql.updateComTime(ID, "bal", "gems")
        # Message de réussite dans la console
        print("Gems >> Balance de {} affichée".format(PlayerID))
    else:
        msg.append("couldown")
        msg.append("Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !")
    return msg


def baltop(param):
    """**_{filtre}_ [nombre]** | Classement des joueurs (10 premiers par défaut)"""
    n = param["nb"]
    filtre = param["filtre"]
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []
    baltop = ""
    if sql.spam(PlayerID, GF.couldown_4s, "baltop", "gems"):
        sql.updateComTime(PlayerID, "baltop", "gems")
        if filtre == "gems" or filtre == "gem" or filtre == "spinelles" or filtre == "spinelle":
            UserList = []
            i = 1
            taille = sql.taille("gems")
            while i <= taille:
                user = sql.userID(i, "gems")
                gems = sql.valueAtNumber(i, "gems", "gems")
                spinelles = sql.valueAtNumber(i, "spinelles", "gems")
                guilde = sql.valueAtNumber(i, "guilde", "gems")
                UserList.append((user, gems, spinelles, guilde))
                i = i + 1
            UserList = sorted(UserList, key=itemgetter(1), reverse=True)
            if filtre == "spinelles" or filtre == "spinelle":
                UserList = sorted(UserList, key=itemgetter(2), reverse=True)
            j = 1
            for one in UserList: # affichage des données trié
                if j <= n:
                    baltop += "{2} | _{3} _<@{0}> {1}:gem:".format(one[0], one[1], j, one[3])
                    if one[2] != 0:
                        baltop += " | {0}<:spinelle:{1}>\n".format(one[2], "{idmoji[spinelle]}")
                    else:
                        baltop += "\n"
                j += 1
            msg.append("OK")
            msg.append(baltop)
        elif filtre == "guild" or filtre == "guilde":
            GuildList = []
            i = 1
            while i <= DB.get_endDocID("DB/guildesDB"):
                try:
                    GuildList.append((DB.valueAt(i, "Nom", "DB/guildesDB"), DB.valueAt(i, "Spinelles", "DB/guildesDB")))
                    i += 1
                except:
                    i += 1
            GuildList = sorted(GuildList, key=itemgetter(1), reverse=True)
            j = 1
            for one in GuildList:
                if j <= n:
                    baltop += "{2} | {0} {1} <:spinelle:{3}>\n".format(one[0], one[1], j, "{idmoji[spinelle]}")
                j += 1
            msg.append("OK")
            msg.append(baltop)
        else:
            msg.append("NOK")
            msg.append("Erreur! Commande incorrect")
    else:
        msg.append("couldown")
        msg.append("Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !")
    return msg


def buy(param):
    """**[item] [nombre]** | Permet d'acheter les items vendus au marché"""
    nb = param["nb"]
    item = param["item"]
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []

    if sql.spam(PlayerID, GF.couldown_4s, "buy", "gems"):
        if int(nb) < 0:
            sql.addGems(PlayerID, -100)
            lvl.addxp(PlayerID, -10, "gems")
            desc = ":no_entry: Anti-cheat! Je vous met un amende de 100 :gem:`gems` pour avoir essayé de tricher !"
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
                            if c.type != "emoji":
                                desc = "Tu viens d'acquérir {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, "{idmoji[gem_" + c.nom + "]}")
                            else:
                                desc = "Tu viens d'acquérir {0} :{1}:`{1}` !".format(nb, c.nom)
                        else :
                            desc = "Désolé, nous ne pouvons pas executer cet achat, tu n'as pas assez de {} en banque".format(argent)
                    else:
                        desc = "Désolé, nous ne pouvons pas executer cet achat, cette item n'est pas vendu au marché"
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
                            desc = "Tu viens d'acquérir {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, "{idmoji[gem_" + c.nom + "]}")
                            msg.append("bank")
                            msg.append(desc)
                            return msg
                        else:
                            sql.add(PlayerID, c.nom, nb, "inventory")
                            desc = "Tu viens d'acquérir {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, "{idmoji[gem_" + c.nom + "]}")
                            if c.nom != "bank_upgrade":
                                if sql.valueAtNumber(PlayerID, c.nom, "durability") == 0:
                                    sql.add(PlayerID, c.nom, c.durabilite, "durability")
                    else :
                        desc = "Désolé, nous ne pouvons pas executer cet achat, tu n'as pas assez de {} en banque".format(argent)
                    break
            for c in GF.objetBox :
                if item == "lootbox_{}".format(c.nom) or item == c.nom:
                    if c.nom != "gift_heart":
                        test = False
                        prix = 0 - (c.achat*nb)
                        if c.type == "gems" and sql.addGems(PlayerID, prix) >= "0":
                            sql.add(PlayerID, "lootbox_{}".format(c.nom), nb, "inventory")
                            desc = "Tu viens d'acquérir {0} <:gem_lootbox:630698430313922580>`{1}` !".format(nb, c.titre)
                        elif c.type == "spinelle" and sql.addSpinelles(PlayerID, prix) >= "0":
                            sql.add(PlayerID, "lootbox_{}".format(c.nom), nb, "inventory")
                            desc = "Tu viens d'acquérir {nb} :{nom}:`{nom}` !".format(nb=nb, nom=c.titre)
                        else :
                            desc = "Désolé, nous ne pouvons pas executer cet achat, tu n'as pas assez de :gem:`gems` en banque"
                        break
            if test :
                desc = "Cet item n'est pas vendu au marché !"
                msg.append("NOK")
            else:
                msg.append("OK")
            msg.append(desc)

            sql.updateComTime(PlayerID, "buy", "gems")
        else:
            desc = "Ton inventaire est plein"
            msg.append("NOK")
            msg.append(desc)
    else:
        desc = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
        msg.append("couldown")
        msg.append(desc)
    return msg


def sell(param):
    """**[item] [nombre]** | Permet de vendre vos items !"""
    nb = param["nb"]
    item = param["item"]
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    if ID == "Error 404":
        return GF.WarningMsg[1]
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
                    gain = c.vente*nb
                    if c.type != "spinelle":
                        sql.addGems(PlayerID, gain)
                        argent = ":gem:`gems`"
                    else:
                        sql.addSpinelles(PlayerID, gain)
                        argent = "<:spinelle:{}>`spinelles`".format("{idmoji[spinelle]}")
                    if c.type != "emoji":
                        desc = "Tu as vendu {0} <:gem_{1}:{3}>`{1}` pour {2} {4} !".format(nb, item, gain, "{idmoji[gem_" + c.nom + "]}", argent)
                    else:
                        desc = "Tu as vendu {0} :{1}:`{1}` pour {2} {3} !".format(nb, item, gain, argent)

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
                    desc = "Tu as vendu {0} <:gem_{1}:{3}>`{1}` pour {2} {4} !".format(nb, item, gain, "{idmoji[gem_" + c.nom + "]}", argent)
                    if nbItem == 1:
                        if sql.valueAt(PlayerID, item, "durability") != 0:
                            sql.add(PlayerID, item, -1, "durability")
                    break

            sql.add(PlayerID, item, -nb, "inventory")
            if test:
                desc = "Cette objet n'existe pas"
        else:
            desc = "Tu n'as pas assez de `{i}`. Il t'en reste : {nb}".format(i=item, nb=str(sql.valueAtNumber(PlayerID, item, "inventory")))
            for c in GF.objetItem:
                if c.nom == item:
                    if c.type == "emoji":
                        desc = "Tu n'as pas assez de :{i}:`{i}`. Il t'en reste : {nb}".format(i=item, nb=str(sql.valueAtNumber(PlayerID, item, "inventory")))
                    else:
                        desc = "Tu n'as pas assez de <:gem_{i}:{idmoji}>`{i}`. Il t'en reste : {nb}".format(i=item, nb=str(sql.valueAtNumber(PlayerID, item, "inventory")), idmoji="{idmoji[gem_" + c.nom + "]}")
            for c in GF.objetOutil:
                if c.nom == item:
                    if c.type == "bank":
                        desc = "Tu ne peux pas vendre tes <:gem_{i}:{idmoji}>`{i}`".format(idmoji="{idmoji[gem_" + c.nom + "]}", i=item)
                    else:
                        desc = "Tu n'as pas assez de <:gem_{i}:{idmoji}>`{i}`. Il t'en reste : {nb}".format(i=item, nb=str(sql.valueAtNumber(PlayerID, item, "inventory")), idmoji="{idmoji[gem_" + c.nom + "]}")

        sql.updateComTime(PlayerID, "sell", "gems")
        msg.append("OK")
        msg.append(desc)
    else:
        desc = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
        msg.append("couldown")
        msg.append(desc)
    return msg


def inv(param):
    """**[nom de la poche]** | Permet de voir ce que vous avez dans le ventre !"""
    fct = param["fct"]
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []

    if sql.spam(PlayerID, GF.couldown_4s, "inv", "gems"):
        if fct == "None" or fct == "principale" or fct == "main":
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
            for c in GF.objetOutil:
                for x in inv:
                    if c.nom == str(x[1]):
                        if int(x[0]) > 0:
                            if c.type == "consommable":
                                msg_invSpeciaux += "<:gem_{0}:{2}>`{0}`: `x{1}` | Durabilité: `{3}/{4}`\n".format(str(x[1]), str(x[0]), "{idmoji[gem_" + c.nom + "]}", sql.valueAtNumber(PlayerID, c.nom, "durability"), c.durabilite)
                            else:
                                msg_invOutils += "<:gem_{0}:{2}>`{0}`: `x{1}` | Durabilité: `{3}/{4}`\n".format(str(x[1]), str(x[0]), "{idmoji[gem_" + c.nom + "]}", sql.valueAtNumber(PlayerID, c.nom, "durability"), c.durabilite)
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
                msg_inv += "\nTaille: `{}/{}` :bangbang:".format(int(tailletot), tailleMax)
            else:
                msg_inv += "\nTaille: `{}/{}`".format(int(tailletot), tailleMax)

            msg.append("OK")
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
            msg.append(desc)

        else:
            desc = "Cette poche n'existe pas"
            msg.append("NOK")
            msg.append(desc)
    else:
        desc = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
        msg.append("couldown")
        msg.append(desc)
    return msg


def market(param):
    """**[stand]** | Permet de voir tout les objets que l'on peux acheter ou vendre !"""
    fct = param["fct"]
    ID = sql.get_SuperID(param["ID"], param["name_pl"])
    if ID == "Error 404":
        return GF.WarningMsg[1]
    PlayerID = sql.get_PlayerID(ID, "gems")
    msg = []
    PlayerID_Babot = sql.get_PlayerID(sql.get_SuperID(GF.idBaBot, "discord"))

    if sql.spam(PlayerID, GF.couldown_4s, "market", "gems"):
        d_market = "Permet de voir tout les objets que l'on peux acheter ou vendre !\n\n"
        if sql.spam(PlayerID_Babot, GF.couldown_10s, "bourse", "gems"):
            GF.loadItem()
        ComTime = sql.valueAtNumber(PlayerID_Babot, "bourse", "gems_com_time")
        time = float(ComTime)
        time = time - (t.time()-GF.couldown_12h)
        timeH = int(time / 60 / 60)
        time = time - timeH * 3600
        timeM = int(time / 60)
        timeS = int(time - timeM * 60)
        d_market += "Actualisation de la bourse dans :clock2:`{}h {}m {}s`\n".format(timeH, timeM, timeS)
        msg.append("OK")
        msg.append(d_market)

        if fct == "mobile":
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
                    d_marketOutilsS += "<:gem_{0}:{2}>`{0}`: Vente **{1}** ".format(c.nom, c.vente, "{idmoji[gem_" + c.nom + "]}")
                    if pourcentageV != 0:
                        d_marketOutilsS += "_{}%_ ".format(pourcentageV)
                    if c.nom == "bank_upgrade":
                        d_marketOutilsS += "| Achat **Le plafond du compte épargne** "
                    else:
                        d_marketOutilsS += "| Achat **{}** ".format(c.achat)
                        if pourcentageA != 0:
                            d_marketOutilsS += "_{}%_ ".format(pourcentageA)
                    if c.durabilite != None:
                        d_marketOutilsS += "| Durabilité: **{}**".format(c.durabilite)
                    d_marketOutilsS += "\n"
                else:
                    d_marketOutils += "<:gem_{0}:{1}>`{0}`: ".format(c.nom, "{idmoji[gem_" + c.nom + "]}")
                    if c.vente != 0:
                        d_marketOutils += "Vente **{}** ".format(c.vente)
                        if pourcentageV != 0:
                            d_marketOutils += "_{}%_ | ".format(pourcentageV)
                        else:
                            d_marketOutils += "| "
                    d_marketOutils += "Achat **{}** ".format(c.achat)
                    if pourcentageA != 0:
                        d_marketOutils += "_{}%_ ".format(pourcentageA)
                    if c.durabilite != None:
                        d_marketOutils += "| Durabilité: **{}**".format(c.durabilite)
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
                    d_marketItemsMinerai += "<:gem_{0}:{2}>`{0}`: Vente **{1}** ".format(c.nom, c.vente, "{idmoji[gem_" + c.nom + "]}")
                    if pourcentageV != 0:
                        d_marketItemsMinerai += "_{}%_ ".format(pourcentageV)
                    d_marketItemsMinerai += "| Achat **{}** ".format(c.achat)
                    if pourcentageA != 0:
                        d_marketItemsMinerai += "_{}%_ ".format(pourcentageA)
                    d_marketItemsMinerai += "| Poids **{}**\n".format(c.poids)
                # =======================================================================================
                elif c.type == "poisson":
                    d_marketItemsPoisson += "<:gem_{0}:{2}>`{0}`: Vente **{1}** ".format(c.nom, c.vente, "{idmoji[gem_" + c.nom + "]}")
                    if pourcentageV != 0:
                        d_marketItemsPoisson += "_{}%_ ".format(pourcentageV)
                    d_marketItemsPoisson += "| Achat **{}** ".format(c.achat)
                    if pourcentageA != 0:
                        d_marketItemsPoisson += "_{}%_ ".format(pourcentageA)
                    d_marketItemsPoisson += "| Poids **{}**\n".format(c.poids)
                # =======================================================================================
                elif c.type == "plante":
                    d_marketItemsPlante += "<:gem_{0}:{2}>`{0}`: Vente **{1}** ".format(c.nom, c.vente, "{idmoji[gem_" + c.nom + "]}")
                    if pourcentageV != 0:
                        d_marketItemsPlante += "_{}%_ ".format(pourcentageV)
                    d_marketItemsPlante += "| Achat **{}** ".format(c.achat)
                    if pourcentageA != 0:
                        d_marketItemsPlante += "_{}%_ ".format(pourcentageA)
                    d_marketItemsPlante += "| Poids **{}**\n".format(c.poids)
                # =======================================================================================
                elif c.type == "halloween" or c.type == "christmas" or c.type == "event":
                    d_marketItemsEvent += "<:gem_{0}:{2}>`{0}`: Vente **{1}** ".format(c.nom, c.vente, "{idmoji[gem_" + c.nom + "]}")
                    if pourcentageV != 0:
                        d_marketItemsEvent += "_{}%_ ".format(pourcentageV)
                    if c.achat != 0:
                        d_marketItemsEvent += "| Achat **{}** ".format(c.achat)
                        if pourcentageA != 0:
                            d_marketItemsEvent += "_{}%_ ".format(pourcentageA)
                    d_marketItemsEvent += "| Poids **{}**\n".format(c.poids)
                # =======================================================================================
                elif c.type == "spinelle":
                    d_marketOutilsS += "<:gem_{0}:{2}>`{0}`: Vente **{1}**<:spinelle:{3}> ".format(c.nom, c.vente, "{idmoji[gem_" + c.nom + "]}", "{idmoji[spinelle]}")
                    d_marketOutilsS += "| Achat **{}**<:spinelle:{}> ".format(c.achat, "{idmoji[spinelle]}")
                    d_marketOutilsS += "| Poids **{}**\n".format(c.poids)
                # =======================================================================================
                elif c.type == "special":
                    d_marketOutilsS += "<:gem_{0}:{2}>`{0}`: Vente **{1}** ".format(c.nom, c.vente, "{idmoji[gem_" + c.nom + "]}")
                    if pourcentageV != 0:
                        d_marketOutilsS += "_{}%_ ".format(pourcentageV)
                    d_marketOutilsS += "| Achat **{}** ".format(c.achat)
                    if pourcentageA != 0:
                        d_marketOutilsS += "_{}%_ ".format(pourcentageA)
                    d_marketOutilsS += "| Poids **{}**\n".format(c.poids)
                # =======================================================================================
                else:
                    if c.type == "emoji":
                        d_marketItems += ":{0}:`{0}`: Vente **{1}** ".format(c.nom, c.vente)
                        if pourcentageV != 0:
                            d_marketItems += "_{}%_ ".format(pourcentageV)
                        d_marketItems += "| Achat **{}** ".format(c.achat)
                        if pourcentageA != 0:
                            d_marketItems += "_{}%_ ".format(pourcentageA)
                        d_marketItems += "| Poids **{}**\n".format(c.poids)
                    else:
                        d_marketItems += "<:gem_{0}:{2}>`{0}`: Vente **{1}** ".format(c.nom, c.vente, "{idmoji[gem_" + c.nom + "]}")
                        if pourcentageV != 0:
                            d_marketItems += "_{}%_ ".format(pourcentageV)
                        d_marketItems += "| Achat **{}** ".format(c.achat)
                        if pourcentageA != 0:
                            d_marketItems += "_{}%_ ".format(pourcentageA)
                        d_marketItems += "| Poids **{}**\n".format(c.poids)

            for c in GF.objetBox :
                if c.type == "gems":
                    d_marketBox += "<:gem_lootbox:{4}>`{0}`: Achat **{1}** | Gain: `{2} ▶ {3}`:gem:`gems` \n".format(c.nom, c.achat, c.min, c.max, "{idmoji[gem_lootbox]}")
                elif c.type == "spinelle":
                    d_marketBox += ":{nom}:`{nom}`: Achat **{prix}<:gem_spinelle:{idmoji}>** | Gain: Items en folie!\n".format(nom=c.nom, prix=c.achat, idmoji="{idmoji[spinelle]}")

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
                            dmSpeciauxInfo += "\n`Durabilité: `{}".format(c.durabilite)
                        else:
                            dmSpeciauxPrix += "\n`Le plafond du compte épargne`"
                            dmSpeciauxInfo += "\n`Taille:` {}".format(c.poids)
                    # =======================================================================================
                    else:
                        dmOutils += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                        dmOutilsPrix += "\n`{}`:gem:".format(c.vente)
                        if pourcentageV != 0:
                            dmOutilsPrix += " _{}%_ ".format(pourcentageV)
                        dmOutilsPrix += " | `{}`:gem:".format(c.achat)
                        if pourcentageA != 0:
                            dmOutilsPrix += " _{}%_ ".format(pourcentageA)
                        dmOutilsInfo += "\n`Durabilité:` {}".format(c.durabilite)

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
                        dmMineraiInfo += "\n`Poids:` {}".format(c.poids)
                    # =======================================================================================
                    elif c.type == "poisson":
                        dmPoisson += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                        dmPoissonPrix += "\n`{}`:gem:".format(c.vente)
                        if pourcentageV != 0:
                            dmPoissonPrix += " _{}%_ ".format(pourcentageV)
                        dmPoissonPrix += " | `{}`:gem:".format(c.achat)
                        if pourcentageA != 0:
                            dmPoissonPrix += " _{}%_ ".format(pourcentageA)
                        dmPoissonInfo += "\n`Poids:` {}".format(c.poids)
                    # =======================================================================================
                    elif c.type == "plante":
                        dmPlante += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                        dmPlantePrix += "\n`{}`:gem:".format(c.vente)
                        if pourcentageV != 0:
                            dmPlantePrix += " _{}%_ ".format(pourcentageV)
                        dmPlantePrix += " | `{}`:gem:".format(c.achat)
                        if pourcentageA != 0:
                            dmPlantePrix += " _{}%_ ".format(pourcentageA)
                        dmPlanteInfo += "\n`Poids:` {}".format(c.poids)
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
                        dmEventInfo += "\n`Poids:` {}".format(c.poids)
                    # =======================================================================================
                    elif c.type == "spinelle":
                        dmSpeciaux += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                        dmSpeciauxPrix += "\n`{prix}`<:spinelle:{idmoji}>".format(prix=c.vente, idmoji="{idmoji[spinelle]}")
                        if pourcentageV != 0:
                            dmSpeciauxPrix += " _{}%_ ".format(pourcentageV)
                        dmSpeciauxPrix += " | `{prix}`<:spinelle:{idmoji}>".format(prix=c.achat, idmoji="{idmoji[spinelle]}")
                        if pourcentageA != 0:
                            dmSpeciauxPrix += " _{}%_ ".format(pourcentageA)
                        dmSpeciauxInfo += "\n`Poids:` {}".format(c.poids)
                    # =======================================================================================
                    elif c.type == "special":
                        dmSpeciaux += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                        dmSpeciauxPrix += "\n`{}`:gem:".format(c.vente)
                        if pourcentageV != 0:
                            dmSpeciauxPrix += " _{}%_ ".format(pourcentageV)
                        dmSpeciauxPrix += " | `{}`:gem:".format(c.achat)
                        if pourcentageA != 0:
                            dmSpeciauxPrix += " _{}%_ ".format(pourcentageA)
                        dmSpeciauxInfo += "\n`Poids:` {}".format(c.poids)
                    # =======================================================================================
                    elif c.type == "emoji":
                        dmItem += "\n:{nom}:`{nom}`".format(nom=c.nom)
                        dmItemPrix += "\n`{}`:gem:".format(c.vente)
                        if pourcentageV != 0:
                            dmItemPrix += " _{}%_ ".format(pourcentageV)
                        dmItemPrix += " | `{}`:gem:".format(c.achat)
                        if pourcentageA != 0:
                            dmItemPrix += " _{}%_ ".format(pourcentageA)
                        dmItemInfo += "\n`Poids:` {}".format(c.poids)
                    # =======================================================================================
                    else:
                        dmItem += "\n<:gem_{nom}:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_" + c.nom + "]}")
                        dmItemPrix += "\n`{}`:gem:".format(c.vente)
                        if pourcentageV != 0:
                            dmItemPrix += " _{}%_ ".format(pourcentageV)
                        dmItemPrix += " | `{}`:gem:".format(c.achat)
                        if pourcentageA != 0:
                            dmItemPrix += " _{}%_ ".format(pourcentageA)
                        dmItemInfo += "\n`Poids:` {}".format(c.poids)

            if fct == "None" or fct == "lootbox":
                for c in GF.objetBox :
                    if c.achat != 0:
                        if c.type == "gems":
                            dmBox += "\n<:gem_lootbox:{idmoji}>`{nom}`".format(nom=c.nom, idmoji="{idmoji[gem_lootbox]}")
                            dmBoxPrix += "\n`{}`:gem:".format(c.achat)
                            dmBoxInfo += "\n`{} ▶ {}`:gem:`gems`".format(c.min, c.max)
                        elif c.type == "spinelle":
                            dmBox += "\n:{nom}:`{nom}`".format(nom=c.nom)
                            dmBoxPrix += "\n`{prix}`<:gem_spinelle:{idmoji}>".format(prix=c.achat, idmoji="{idmoji[spinelle]}")
                            dmBoxInfo += "\nItems en folie!"

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
                msg.append(dmPoissonPrix)
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
            desc = "Ce marché n'existe pas"
            msg.append("NOK")
            msg.append(desc)
    else:
        desc = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
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
    if ID == "Error 404":
        return GF.WarningMsg[1]
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
                    desc = "{0} donne {1} :gem:`gems` à {2} !".format(nom, gain, Nom_recu)
                    # Message de réussite dans la console
                    print("Gems >> {} a donné {} Gems à {}".format(nom, gain, Nom_recu))
                else:
                    desc = "{0} n'a pas assez pour donner {1} :gem:`gems` à {2} !".format(nom, gain, Nom_recu)

                sql.updateComTime(PlayerID, "pay", "gems")
                msg.append("OK")
            else :
                desc = "Tu ne peux pas donner une somme négative ! N'importe quoi enfin !"
                msg.append("NOK")
        except ValueError:
            desc = "La commande est mal formulée"
            msg.append("NOK")
            pass
    else:
        desc = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
        msg.append("couldown")
    msg.append(desc)
    return msg

# @commands.command(pass_context=True)
# async def give(self, ctx, nom, item, nb = None):
#     """**[nom] [item] [nombre]** | Donner des items à vos amis !"""
#     ID = ctx.author.id
#     name = ctx.author.name
#     checkLB = False
#     if item == "bank_upgrade":
#         await ctx.channel.send("Tu ne peux pas donner cette item!")
#         return False
#     if sql.spam(ID,GF.couldown_4s, "give", "gems"):
#         try:
#             if nb == None:
#                 nb = 1
#             else:
#                 nb = int(nb)
#             if nb < 0 and nb != -1:
#                 sql.addGems(ID, -100)
#                 msg = ":no_entry: Anti-cheat! Je vous met un amende de 100 :gem:`gems` pour avoir essayé de tricher !"
#                 slq.add(ID, "DiscordCop Amende", 1, "statgems")
#                 await ctx.channel.send(msg)
#                 return "anticheat"
#             elif nb > 0:
#                 ID_recu = sql.nom_ID(nom)
#                 Nom_recu = ctx.guild.get_member(ID_recu).name
#                 for lootbox in GF.objetBox:
#                     if item == lootbox.nom:
#                         checkLB = True
#                         itemLB = lootbox.nom
#                         item = "lootbox_{}".format(lootbox.nom)
#                 nbItem = int(sql.valueAtNumber(ID, item, "inventory"))
#                 if nbItem >= nb and nb > 0:
#                     if GF.testInvTaille(ID_recu):
#                         sql.add(ID, item, -nb, "inventory")
#                         sql.add(ID_recu, item, nb, "inventory")
#                         if checkLB:
#                             msg = "{0} donne {1} <:gem_lootbox:{3}>`{2}` à {4} !".format(name,nb,itemLB,"{idmoji[gem_" + itemLB + "]}",Nom_recu)
#                         else:
#                             for c in GF.objetItem:
#                                 if c.nom == item:
#                                     if c.type == "emoji":
#                                         msg = "{0} donne {1} :{2}:`{2}` à {3} !".format(name, nb, item, Nom_recu)
#                                     else:
#                                         msg = "{0} donne {1} <:gem_{2}:{3}>`{2}` à {4} !".format(name,nb,item,"{idmoji[gem_" + item + "]}",Nom_recu)
#                             for c in GF.objetOutil:
#                                 if c.nom == item:
#                                     if c.type == "emoji":
#                                         msg = "{0} donne {1} :{2}:`{2}` à {3} !".format(name, nb, item, Nom_recu)
#                                     else:
#                                         msg = "{0} donne {1} <:gem_{2}:{3}>`{2}` à {4} !".format(name,nb,item,"{idmoji[gem_" + item + "]}",Nom_recu)
#                         # Message de réussite dans la console
#                         print("Gems >> {0} a donné {1} {2} à {3}".format(name, nb, item, Nom_recu))
#                     else:
#                         msg = "L'inventaire de {} est plein".format(Nom_recu)
#                 else:
#                     msg = "{0} n'a pas assez pour donner à {1} !".format(name, Nom_recu)
#
#             elif nb == -1:
#                 ID_recu = sql.nom_ID(nom)
#                 Nom_recu = ctx.guild.get_member(ID_recu).name
#                 nbItem = int(sql.valueAtNumber(ID, item, "inventory"))
#                 if nb > 0:
#                     if GF.testInvTaille(ID_recu):
#                         sql.add(ID, item, -nb, "inventory")
#                         sql.add(ID_recu, item, nb, "inventory")
#                         for c in GF.objetItem:
#                             if c.nom == item:
#                                 if c.type == "emoji":
#                                     msg = "{0} donne {1} :{2}:`{2}` à {3} !".format(name, nb, item, Nom_recu)
#                                 else:
#                                     msg = "{0} donne {1} <:gem_{2}:{3}>`{2}` à {4} !".format(name,nb,item,"{idmoji[gem_" + item + "]}",Nom_recu)
#                         for c in GF.objetOutil:
#                             if c.nom == item:
#                                 if c.type == "emoji":
#                                     msg = "{0} donne {1} :{2}:`{2}` à {3} !".format(name, nb, item, Nom_recu)
#                                 else:
#                                     msg = "{0} donne {1} <:gem_{2}:{3}>`{2}` à {4} !".format(name,nb,item,"{idmoji[gem_" + item + "]}",Nom_recu)
#                         # Message de réussite dans la console
#                         print("Gems >> {0} a donné {1} {2} à {3}".format(name, nb, item, Nom_recu))
#                     else:
#                         msg = "L'inventaire de {} est plein".format(Nom_recu)
#                 else:
#                     msg = "{0} n'a pas assez pour donner à {1} !".format(name, Nom_recu)
#
#             else :
#                 msg = "Tu ne peux pas donner une somme négative ! N'importe quoi enfin !"
#             sql.updateComTime(ID, "give", "gems")
#         except ValueError:
#             msg = "La commande est mal formulée"
#             pass
#     else:
#         msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
#     await ctx.channel.send(msg)
#
#
#
# @commands.command(pass_context=True)
# async def forge(self, ctx, item = None, nb = 1):
#     """**[item] [nombre]** | Permet de concevoir des items spécifiques"""
#     ID = ctx.author.id
#     if sql.spam(ID,GF.couldown_4s, "forge", "gems"):
#         if GF.testInvTaille(ID):
#             #-------------------------------------
#             # Affichage des recettes disponible
#             if item == None:
#                 msg = GF.recette(ctx)
#                 await ctx.channel.send(embed = msg)
#                 # Message de réussite dans la console
#                 print("Gems >> {} a afficher les recettes".format(ctx.author.name))
#                 return
#             #-------------------------------------
#             else:
#                 for c in GF.objetRecette:
#                     if item == c.nom:
#                         nb = int(nb)
#                         nb1 = nb*c.nb1
#                         nb2 = nb*c.nb2
#                         nb3 = nb*c.nb3
#                         nb4 = nb*c.nb4
#                         if c.item1 != "" and c.item2 != "" and c.item3 != "" and c.item4 != "":
#                             if sql.valueAtNumber(ID, c.item1, "inventory") >= nb1 and sql.valueAtNumber(ID, c.item2, "inventory") >= nb2 and sql.valueAtNumber(ID, c.item3, "inventory") >= nb3 and sql.valueAtNumber(ID, c.item4, "inventory") >= nb4:
#                                 sql.add(ID, c.nom, nb, "inventory")
#                                 sql.add(ID, c.item1, -1*nb1, "inventory")
#                                 sql.add(ID, c.item2, -1*nb2, "inventory")
#                                 sql.add(ID, c.item3, -1*nb3, "inventory")
#                                 sql.add(ID, c.item4, -1*nb4, "inventory")
#                                 msg = "Bravo, tu as réussi à forger {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, "{idmoji[gem_" + c.nom + "]}")
#                                 print("Gems >> {0} a forgé {1} {2}".format(ctx.author.name, nb, c.nom))
#                                 Durability = sql.valueAtNumber(ID, c.nom, "durability")
#                                 if Durability == 0:
#                                     for x in GF.objetOutil:
#                                         if x.nom == c.nom:
#                                             sql.add(ID, x.nom, x.durabilite, "durability")
#                             else:
#                                 msg = ""
#                                 if sql.valueAtNumber(ID, c.item1, "inventory") < nb1:
#                                     nbmissing = (sql.valueAtNumber(ID, c.item1, "inventory") - nb1)*-1
#                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item1, "{idmoji[gem_" + c.item1 + "]}")
#                                 if sql.valueAtNumber(ID, c.item2, "inventory") < nb2:
#                                     nbmissing = (sql.valueAtNumber(ID, c.item2, "inventory") - nb2)*-1
#                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item2, "{idmoji[gem_" + c.item2 + "]}")
#                                 if sql.valueAtNumber(ID, c.item3, "inventory") < nb3:
#                                     nbmissing = (sql.valueAtNumber(ID, c.item3, "inventory") - nb3)*-1
#                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item3, "{idmoji[gem_" + c.item3 + "]}")
#                                 if sql.valueAtNumber(ID, c.item4, "inventory") < nb4:
#                                     nbmissing = (sql.valueAtNumber(ID, c.item4, "inventory") - nb4)*-1
#                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item4, "{idmoji[gem_" + c.item4 + "]}")
#
#                         elif c.item1 != "" and c.item2 != "" and c.item3 != "":
#                             if sql.valueAtNumber(ID, c.item1, "inventory") >= nb1 and sql.valueAtNumber(ID, c.item2, "inventory") >= nb2 and sql.valueAtNumber(ID, c.item3, "inventory") >= nb3:
#                                 sql.add(ID, c.nom, nb, "inventory")
#                                 sql.add(ID, c.item1, -1*nb1, "inventory")
#                                 sql.add(ID, c.item2, -1*nb2, "inventory")
#                                 sql.add(ID, c.item3, -1*nb3, "inventory")
#                                 msg = "Bravo, tu as réussi à forger {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, "{idmoji[gem_" + c.nom + "]}")
#                                 print("Gems >> {0} a forgé {1} {2}".format(ctx.author.name, nb, c.nom))
#                                 Durability = sql.valueAtNumber(ID, c.nom, "durability")
#                                 if Durability == 0:
#                                     for x in GF.objetOutil:
#                                         if x.nom == c.nom:
#                                             sql.add(ID, x.nom, x.durabilite, "durability")
#                             else:
#                                 msg = ""
#                                 if sql.valueAtNumber(ID, c.item1, "inventory") < nb1:
#                                     nbmissing = (sql.valueAtNumber(ID, c.item1, "inventory") - nb1)*-1
#                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item1, "{idmoji[gem_" + c.item1 + "]}")
#                                 if sql.valueAtNumber(ID, c.item2, "inventory") < nb2:
#                                     nbmissing = (sql.valueAtNumber(ID, c.item2, "inventory") - nb2)*-1
#                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item2, "{idmoji[gem_" + c.item2 + "]}")
#                                 if sql.valueAtNumber(ID, c.item3, "inventory") < nb3:
#                                     nbmissing = (sql.valueAtNumber(ID, c.item3, "inventory") - nb3)*-1
#                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item3, "{idmoji[gem_" + c.item3 + "]}")
#
#                         elif c.item1 != "" and c.item2 != "":
#                             if sql.valueAtNumber(ID, c.item1, "inventory") >= nb1 and sql.valueAtNumber(ID, c.item2, "inventory") >= nb2:
#                                 sql.add(ID, c.nom, nb, "inventory")
#                                 sql.add(ID, c.item1, -1*nb1, "inventory")
#                                 sql.add(ID, c.item2, -1*nb2, "inventory")
#                                 msg = "Bravo, tu as réussi à forger {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, "{idmoji[gem_" + c.nom + "]}")
#                                 print("Gems >> {0} a forgé {1} {2}".format(ctx.author.name, nb, c.nom))
#                                 Durability = sql.valueAtNumber(ID, c.nom, "durability")
#                                 if Durability == 0:
#                                     for x in GF.objetOutil:
#                                         if x.nom == c.nom:
#                                             sql.add(ID, x.nom, x.durabilite, "durability")
#                             else:
#                                 msg = ""
#                                 if sql.valueAtNumber(ID, c.item1, "inventory") < nb1:
#                                     nbmissing = (sql.valueAtNumber(ID, c.item1, "inventory") - nb1)*-1
#                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item1, "{idmoji[gem_" + c.item1 + "]}")
#                                 if sql.valueAtNumber(ID, c.item2, "inventory") < nb2:
#                                     nbmissing = (sql.valueAtNumber(ID, c.item2, "inventory") - nb2)*-1
#                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item2, "{idmoji[gem_" + c.item2 + "]}")
#
#                         elif c.item1 != "":
#                             if sql.valueAtNumber(ID, c.item1, "inventory") >= nb1:
#                                 sql.add(ID, c.nom, nb, "inventory")
#                                 sql.add(ID, c.item1, -1*nb1, "inventory")
#                                 msg = "Bravo, tu as réussi à forger {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, "{idmoji[gem_" + c.nom + "]}")
#                                 print("Gems >> {0} a forgé {1} {2}".format(ctx.author.name, nb, c.nom))
#                                 Durability = sql.valueAtNumber(ID, c.nom, "durability")
#                                 if Durability == 0:
#                                     for x in GF.objetOutil:
#                                         if x.nom == c.nom:
#                                             sql.add(ID, x.nom, x.durabilite, "durability")
#                             else:
#                                 nbmissing = (sql.valueAtNumber(ID, c.item1, "inventory") - nb1)*-1
#                                 msg = "Il te manque {0} <:gem_{1}:{2}>`{1}`".format(nbmissing, c.item1, "{idmoji[gem_" + c.item1 + "]}")
#                         await ctx.channel.send(msg)
#                         return True
#                     else:
#                         msg = "Aucun recette disponible pour forger cette item !"
#             sql.updateComTime(ID, "forge", "gems")
#         else:
#             msg = "Ton inventaire est plein"
#     else:
#         msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
#     await ctx.channel.send(msg)
#
#
#
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
#         msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
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
#         msg = "Il faut attendre "+str(GF.couldown_6s)+" secondes entre chaque commande !"
#         await ctx.channel.send(msg)
#
#
#
# @commands.command(pass_context=True)
# async def graphbourse(self, ctx, item, mois = None, annee = None, type = None):
#     """**[item] [mois] [année]** | Historique de la bourse par item"""
#     ID = ctx.author.id
#     now = dt.datetime.now()
#
#     if item.lower() == "all":
#         if type == None:
#             type = str(now.month)
#         if annee == None:
#             annee = str(now.year)
#         temp = type
#         type = mois.lower()
#         mois = temp
#         if type == "item" or type == "items":
#             for c in GF.objetItem:
#                 check = False
#                 for x in GI.exception:
#                     if x == c.nom:
#                         check = True
#                 for x in GF.ObjetEventEnd:
#                     if x == c.nom:
#                         check = True
#                 if not check:
#                     graph = GS.create_graph(c.nom, annee, mois)
#                     if graph == "404":
#                         await ctx.send("Aucune données n'a été trouvée!")
#                     else:
#                         await ctx.send(file=discord.File("cache/{}".format(graph)))
#                         os.remove("cache/{}".format(graph))
#         elif type == "outil" or type == "outils":
#             for c in GF.objetOutil:
#                 check = False
#                 for x in GI.exception:
#                     if x == c.nom:
#                         check = True
#                 if c.type != "bank" and check == False:
#                     graph = GS.create_graph(c.nom, annee, mois)
#                     if graph == "404":
#                         await ctx.send("Aucune données n'a été trouvée!")
#                     else:
#                         await ctx.send(file=discord.File("cache/{}".format(graph)))
#                         os.remove("cache/{}".format(graph))
#         else:
#             await ctx.send("Commande mal formulée")
#     else:
#         if mois == None:
#             mois = str(now.month)
#         if annee == None:
#             annee = str(now.year)
#         graph = GS.create_graph(item, annee, mois)
#         if graph == "404":
#             await ctx.send("Aucune données n'a été trouvée!")
#         else:
#             await ctx.send(file=discord.File("cache/{}".format(graph)))
#             os.remove("cache/{}".format(graph))
