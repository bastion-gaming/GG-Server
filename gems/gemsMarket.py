from operator import itemgetter
import time as t
from DB import SQLite as sql
from core import level as lvl
from gems import gemsFonctions as GF, gemsItems as GI
import json
from languages import lang as lang_P


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
