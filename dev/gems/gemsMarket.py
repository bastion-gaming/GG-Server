import time as t
from database import SQLite as sql
from core import level as lvl
from gems import gemsFonctions as GF, gemsItems as GI
import json


def buy(param):
    """**[item] [nombre]** | Permet d'acheter les items vendus au marché"""
    nb = param["nb"]
    item = param["item"]
    lang = param["lang"]
    PlayerID = param["PlayerID"]

    if sql.spam(PlayerID, GF.couldown("4s"), "buy"):
        if int(nb) < 0:
            sql.addGems(PlayerID, -100)
            lvl.addxp(PlayerID, -10)
            GF.addStats(PlayerID, ["divers", "DiscordCop Amende"], 1)
            return {'error': 3, 'etat': 'anticheat', 'lang': lang, 'gain': False, 'perte': False}

        elif GF.testInvTaille(PlayerID) or item == "backpack" or item == "hyperpack" or item == "bank_upgrade":
            nb = int(nb)
            solde = sql.value(PlayerID, "gems", "Gems")
            soldeSpinelles = sql.value(PlayerID, "gems", "Spinelles")
            for c in GF.objetItem :
                if item == c.nom :
                    check = False
                    prix = (c.achat*nb)
                    if c.type != "spinelle":
                        argent = "gems"
                        if solde >= prix:
                            sql.addGems(PlayerID, -prix)
                            GF.addStats(PlayerID, ["buy", "buy | dépense"], prix)
                            check = True
                    else:
                        argent = c.type
                        if soldeSpinelles >= prix:
                            sql.addSpinelles(PlayerID, -prix)
                            check = True
                    if check:
                        GF.addInventory(PlayerID, c.nom, nb)
                        GF.addStats(PlayerID, ["buy", "buy | item | {}".format(c.nom)], nb)
                        GF.addStats(PlayerID, ["buy", "buy | total"], nb)
                        GF.addStats(PlayerID, ["buy", "buy"], 1)
                        sql.updateComTime(PlayerID, "buy")
                        return {'error': 0, 'etat': 'OK', 'lang': lang, 'gain': {c.nom: nb}, 'perte': {argent: prix}}
                    else :
                        sql.updateComTime(PlayerID, "buy")
                        return {'error': 4, 'etat': 'NOK', 'lang': lang, 'gain': False, 'perte': False, 'device': argent}
                    break
            for c in GF.objetOutil :
                if item == c.nom :
                    check = False
                    prix = c.achat*nb
                    if c.type != "spinelle":
                        argent = "gems"
                        if solde >= prix:
                            sql.addGems(PlayerID, -prix)
                            GF.addStats(PlayerID, ["buy", "buy | dépense"], prix)
                            check = True
                    else:
                        argent = c.type
                        if soldeSpinelles >= prix:
                            sql.addSpinelles(PlayerID, -prix)
                            check = True
                    if check:
                        GF.addInventory(PlayerID, c.nom, nb)
                        GF.addStats(PlayerID, ["buy", "buy"], 1)
                        GF.addStats(PlayerID, ["buy", "buy | item | {}".format(c.nom)], nb)
                        GF.addStats(PlayerID, ["buy", "buy | total"], nb)
                        sql.updateComTime(PlayerID, "buy")
                        return {'error': 0, 'etat': 'OK', 'lang': lang, 'gain': {c.nom: nb}, 'perte': {argent: prix}}
                    else :
                        return {'error': 4, 'etat': 'NOK', 'lang': lang, 'gain': False, 'perte': False, 'device': argent}
                    break
            for c in GF.objetUpgrade:
                if item == c.nom :
                    check = False
                    if c.type == "bank":
                        soldeMax = sql.value(PlayerID, "gems", "BankSMax")
                        if soldeMax == 0:
                            soldeMax = c.achat
                            sql.update(PlayerID, "gems", "BankSMax", soldeMax)
                        soldeMult = soldeMax/c.achat
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
                        argent = "gems"
                        if solde >= prix:
                            sql.addGems(PlayerID, -prix)
                            GF.addStats(PlayerID, ["buy", "buy | dépense"], prix)
                            check = True
                    else:
                        argent = c.type
                        if soldeSpinelles >= prix:
                            sql.addSpinelles(PlayerID, -prix)
                            check = True
                    if check:
                        if c.type == "bank":
                            sql.update(PlayerID, "gems", "BankSMax", soldeMax + nb*c.achat)
                        else:
                            GF.addInventory(PlayerID, c.nom, nb)
                        GF.addStats(PlayerID, ["buy", "buy | upgrade | {}".format(c.nom)], nb)
                        GF.addStats(PlayerID, ["buy", "buy | total"], nb)
                        GF.addStats(PlayerID, ["buy", "buy"], 1)
                        sql.updateComTime(PlayerID, "buy")
                        return {'error': 0, 'etat': 'OK', 'lang': lang, 'gain': {c.nom: nb}, 'perte': {argent: prix}}
                    else :
                        sql.updateComTime(PlayerID, "buy")
                        return {'error': 4, 'etat': 'NOK', 'lang': lang, 'gain': False, 'perte': False, 'device': argent}
                    break
            return {'error': 5, 'etat': 'NOK', 'lang': lang, 'gain': False, 'perte': False}
        else:
            return {'error': 2, 'etat': 'Warning', 'lang': lang, 'gain': False, 'perte': False}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'gain': False, 'perte': False, 'couldown': str(GF.couldown("4s"))}


def sell(param):
    """**[item] [nombre]** | Permet de vendre vos items !"""
    nb = param["nb"]
    item = param["item"]
    lang = param["lang"]
    PlayerID = param["PlayerID"]

    if sql.spam(PlayerID, GF.couldown("4s"), "sell"):
        nbItem = sql.value(PlayerID, "inventory", "Stock", "Item", item)
        if nbItem is False:
            nbItem = 0
        if int(nb) == -1:
            nb = nbItem
        nb = int(nb)
        check = False
        for c in GF.objetItem:
            if item == c.nom:
                check = True
        for c in GF.objetOutil:
            if item == c.nom:
                check = True
        if nbItem >= nb and nb > 0:
            for c in GF.objetItem:
                if item == c.nom:
                    GF.addStats(PlayerID, ["sell", "sell | item | {}".format(c.nom)], nb)
                    GF.addStats(PlayerID, ["sell", "sell | total"], nb)
                    gain = c.vente*nb
                    if c.type != "spinelle":
                        argent = "gems"
                        sql.addGems(PlayerID, gain)
                        GF.addStats(PlayerID, ["sell", "sell | gain"], gain)
                    else:
                        argent = c.type
                        sql.addSpinelles(PlayerID, gain)
                    GF.addStats(PlayerID, ["sell", "sell"], 1)
                    sql.updateComTime(PlayerID, "sell")
                    GF.addInventory(PlayerID, item, -nb)
                    return {'error': 0, 'etat': 'OK', 'lang': lang, 'gain': {argent: gain}, 'perte': {c.nom: nb}}

            for c in GF.objetOutil:
                if item == c.nom:
                    gain = c.vente*nb
                    if c.type9 != "spinelle":
                        argent = "gems"
                        sql.addGems(PlayerID, gain)
                        GF.addStats(PlayerID, ["sell", "sell | gain"], gain)
                    else:
                        argent = c.type
                        sql.addSpinelles(PlayerID, gain)
                    GF.addStats(PlayerID, ["sell", "sell | item | {}".format(c.nom)], nb)
                    GF.addStats(PlayerID, ["sell", "sell | total"], nb)
                    if nbItem == 1:
                        itemDurability = sql.value(PlayerID, "inventory", "Stock", "Item", item)
                        if itemDurability is not False or itemDurability != []:
                            sql.update(PlayerID, "inventory", "Durability", -1, "Item", item)
                    GF.addStats(PlayerID, ["sell", "sell"], 1)
                    sql.updateComTime(PlayerID, "sell")
                    GF.addInventory(PlayerID, item, -nb)
                    return {'error': 0, 'etat': 'OK', 'lang': lang, 'gain': {argent: gain}, 'perte': {c.nom: nb}}
        else:
            if check:
                return {'error': 2, 'etat': 'Warning', 'lang': lang, 'gain': False, 'perte': False, 'nbItem': nbItem}
            else:
                return {'error': 5, 'etat': 'NOK', 'lang': lang, 'gain': False, 'perte': False}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'gain': False, 'perte': False, 'couldown': str(GF.couldown("4s"))}


def market(param):
    """**[stand]** | Permet de voir tout les objets que l'on peux acheter ou vendre !"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    cat = {
        'special': {},
        'outils': {},
        'upgrade': {},
        'items': {
            'special': {},
            'minerai': {},
            'poisson': {},
            'plante': {},
            'consommable': {},
            'event': {}
        }
    }
    if sql.spam(PlayerID, GF.couldown("4s"), "market"):
        if sql.spam(GF.PlayerID_GetGems, GF.couldown("8h"), "bourse"):
            GF.loadItem()
        ComTime = sql.value(GF.PlayerID_GetGems, "gems_com_time", "Com_Time", "Commande", "bourse")
        time = float(ComTime)
        time = time - (t.time()-GF.couldown("8h"))
        timeH = int(time / 60 / 60)
        time = time - timeH * 3600
        timeM = int(time / 60)
        timeS = int(time - timeM * 60)
        TimeBourse = [timeH, timeM, timeS]
        Market = {'error': 0, 'etat': 'OK', 'lang': lang, 'market': cat, 'time': TimeBourse}
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
                            if pourcentageV != 0:
                                pourcentageV = "{0}%".format(pourcentageV)
                            else:
                                pourcentageV = ""
                        except:
                            pourcentageV = ""
                    else:
                        pourcentageV = ""
                    if y.achat != 0:
                        try:
                            pourcentageA = ((c.achat*100)//temp["precAchat"])-100
                            if pourcentageA != 0:
                                pourcentageA = "{0}%".format(pourcentageA)
                            else:
                                pourcentageA = ""
                        except:
                            pourcentageA = ""
                    else:
                        pourcentageA = ""
            # =======================================================================================
            if c.type == "consommable":
                Market['market']['special'][c.nom] = {'achat': c.achat, 'PA': pourcentageA, 'vente': c.vente, 'PV': pourcentageV, 'durability': c.durabilite, 'poids': c.poids}
            # =======================================================================================
            else:
                Market['market']['outils'][c.nom] = {'achat': c.achat, 'PA': pourcentageA, 'vente': c.vente, 'PV': pourcentageV, 'durability': c.durabilite, 'poids': c.poids}

        # Les upgrades
        for c in GF.objetUpgrade:
            Market['market']['upgrade'][c.nom] = {'achat': c.achat, 'vente': c.vente, 'info': 0}

        # Les items
        for c in GF.objetItem:
            for y in GI.PrixItem:
                if y.nom == c.nom:
                    temp = d[c.nom]
                    if y.vente != 0:
                        try:
                            pourcentageV = ((c.vente*100)//temp["precVente"])-100
                            if pourcentageV != 0:
                                pourcentageV = "{0}%".format(pourcentageV)
                            else:
                                pourcentageV = ""
                        except:
                            pourcentageV = ""
                    else:
                        pourcentageV = ""
                    if y.achat != 0:
                        try:
                            pourcentageA = ((c.achat*100)//temp["precAchat"])-100
                            if pourcentageA != 0:
                                pourcentageA = "{0}%".format(pourcentageA)
                            else:
                                pourcentageA = ""
                        except:
                            pourcentageA = ""
                    else:
                        pourcentageA = ""
            # =======================================================================================
            if c.type == "halloween" or c.type == "christmas" or c.type == "event":
                Market['market']['items']['event'][c.nom] = {'achat': c.achat, 'PA': pourcentageA, 'vente': c.vente, 'PV': pourcentageV, 'poids': c.poids}
            # =======================================================================================
            else:
                Market['market']['items'][c.type][c.nom] = {'achat': c.achat, 'PA': pourcentageA, 'vente': c.vente, 'PV': pourcentageV, 'poids': c.poids}

        sql.updateComTime(PlayerID, "market")
        return Market
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'gain': False, 'perte': False, 'couldown': str(GF.couldown("4s"))}


def pay(param):
    """**[Nom_recu] [gain]** | Donner de l'argent à vos amis !"""
    nom = param["nom"]
    gain = param["gain"]
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    ID_recu = sql.get_PlayerID(sql.nom_ID(param["ID_recu"]), param["name_pl"])
    if ID_recu['error'] == 404:
        return {'error': 405, 'etat': 'PlayerID', 'lang': lang, 'gain': False, 'perte': False, 'success': False}
    ID_recu = ID_recu['ID']
    Nom_recu = sql.value(ID_recu, "gems", "Pseudo")

    if sql.spam(PlayerID, GF.couldown("4s"), "pay"):
        try:
            if int(gain) > 0:
                gain = int(gain)
                don = -gain
                solde = int(sql.value(PlayerID, "gems", "Gems"))
                print(solde)
                if solde >= gain:
                    sql.addGems(ID_recu, gain)
                    sql.addGems(PlayerID, don)
                    # desc = lang_P.forge_msg(lang, "pay", [nom, gain, Nom_recu], False, 0)
                    # Message de réussite dans la console
                    print("Gems >> {} a donné {} Gems à {}".format(nom, gain, Nom_recu))
                    GF.addStats(PlayerID, ["pay", "pay"], 1)
                    GF.addStats(PlayerID, ["pay", "pay | nb gems"], gain)
                    donmax = sql.value(PlayerID, "statgems", "Stock", ["Nom", "Type"], ["pay | don max", "pay"])
                    recumax = sql.value(PlayerID, "statgems", "Stock", ["Nom", "Type"], ["pay | recu max", "pay"])
                    if gain > donmax:
                        GF.addStats(PlayerID, ["pay", "pay | don max"], gain)
                    if gain > recumax:
                        GF.addStats(ID_recu, ["pay", "pay | recu max"], gain)
                    sql.updateComTime(PlayerID, "pay")
                    return {'error': 0, 'etat': 'OK', 'lang': lang, 'gain': gain, 'don': don}
                else:
                    # desc = lang_P.forge_msg(lang, "pay", [nom, gain, Nom_recu], False, 1)
                    return {'error': 4, 'etat': 'NOK', 'lang': lang, 'gain': False, 'don': -don}
            else :
                # desc = lang_P.forge_msg(lang, "pay", None, False, 2)
                return {'error': 3, 'etat': 'NOK', 'lang': lang, 'gain': False, 'don': False}
        except ValueError:
            # desc = lang_P.forge_msg(lang, "WarningMsg", None, False, 3)
            return {'error': 2, 'etat': 'Warning', 'lang': lang, 'gain': False, 'don': False}
            pass
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'gain': False, 'don': False, 'couldown': str(GF.couldown("4s"))}


# def give(param):
#     """**[nom] [item] [nombre]** | Donner des items à vos amis !"""
#     nom = param["nom"]
#     item = param["item"]
#     nb = param["nb"]
#     ID_recu = sql.get_PlayerID(sql.get_SuperID(sql.nom_ID(param["ID_recu"]), param["name_pl"]))
#     Nom_recu = param["Nom_recu"]
#     lang = param["lang"]
#     PlayerID = param["PlayerID"]
#     msg = dict()
#     msg["lang"] = lang
#
#     checkLB = False
#     if item == "bank_upgrade":
#         msg["type"] = "NOK"
#         msg["desc"] = lang_P.forge_msg(lang, "give", None, False, 0)
#         return msg
#         return False
#     if sql.spam(PlayerID, GF.couldown("4s"), "give", "gems"):
#         try:
#             if nb == None:
#                 nb = 1
#             else:
#                 nb = int(nb)
#             if nb < 0 and nb != -1:
#                 sql.addGems(PlayerID, -100)
#                 desc = lang_P.forge_msg(lang, "DiscordCop Amende")
#                 sql.add(PlayerID, ["divers", "DiscordCop Amende"], 1, "statgems")
#                 msg["type"] = "anticheat"
#                 msg["desc"] = desc
#                 return msg
#             elif nb > 0:
#                 for lootbox in GF.objetBox:
#                     if item == lootbox.nom:
#                         checkLB = True
#                         itemLB = lootbox.nom
#                         item = "lootbox_{}".format(lootbox.nom)
#                 nbItem = int(sql.valueAtNumber(PlayerID, item, "inventory"))
#                 if nbItem >= nb and nb > 0:
#                     if GF.testInvTaille(ID_recu) or item == "hyperpack" or item == "backpack":
#                         sql.add(PlayerID, item, -nb, "inventory")
#                         sql.add(ID_recu, item, nb, "inventory")
#                         if checkLB:
#                             desc = lang_P.forge_msg(lang, "give", [nom, nb, itemLB, "{idmoji[gem_" + itemLB + "]}", Nom_recu], False, 1)
#                         else:
#                             for c in GF.objetItem:
#                                 if c.nom == item:
#                                     if c.type == "emoji":
#                                         desc = lang_P.forge_msg(lang, "give", [nom, nb, item, Nom_recu], False, 2)
#                                     else:
#                                         desc = lang_P.forge_msg(lang, "give", [nom, nb, item, "{idmoji[gem_" + item + "]}", Nom_recu], False, 3)
#                             for c in GF.objetOutil:
#                                 if c.nom == item:
#                                     if c.type == "emoji":
#                                         desc = lang_P.forge_msg(lang, "give", [nom, nb, item, Nom_recu], False, 2)
#                                     else:
#                                         desc = lang_P.forge_msg(lang, "give", [nom, nb, item, "{idmoji[gem_" + item + "]}", Nom_recu], False, 3)
#                         # Message de réussite dans la console
#                         print("Gems >> {0} a donné {1} {2} à {3}".format(nom, nb, item, Nom_recu))
#                         sql.add(PlayerID, ["give", "give"], 1, "statgems")
#                         sql.add(PlayerID, ["give", "give | nb items"], nb, "statgems")
#                         sql.add(PlayerID, ["give", "give | item | {}".format(item)], nb, "statgems")
#                     else:
#                         desc = lang_P.forge_msg(lang, "give", [Nom_recu], False, 4)
#                 else:
#                     desc = lang_P.forge_msg(lang, "give", [nom, Nom_recu], False, 5)
#                 msg["type"] = "OK"
#             elif nb == -1:
#                 nbItem = int(sql.valueAtNumber(PlayerID, item, "inventory"))
#                 if nb > 0:
#                     if GF.testInvTaille(ID_recu) or item == "hyperpack" or item == "backpack":
#                         sql.add(PlayerID, item, -nb, "inventory")
#                         sql.add(ID_recu, item, nb, "inventory")
#                         for c in GF.objetItem:
#                             if c.nom == item:
#                                 if c.type == "emoji":
#                                     desc = lang_P.forge_msg(lang, "give", [nom, nb, item, Nom_recu], False, 2)
#                                 else:
#                                     desc = lang_P.forge_msg(lang, "give", [nom, nb, item, "{idmoji[gem_" + item + "]}", Nom_recu], False, 3)
#                         for c in GF.objetOutil:
#                             if c.nom == item:
#                                 if c.type == "emoji":
#                                     desc = lang_P.forge_msg(lang, "give", [nom, nb, item, Nom_recu], False, 2)
#                                 else:
#                                     desc = lang_P.forge_msg(lang, "give", [nom, nb, item, "{idmoji[gem_" + item + "]}", Nom_recu], False, 3)
#                         # Message de réussite dans la console
#                         print("Gems >> {0} a donné {1} {2} à {3}".format(nom, nb, item, Nom_recu))
#                         sql.add(PlayerID, ["give", "give"], 1, "statgems")
#                         sql.add(PlayerID, ["give", "give | nb items"], nb, "statgems")
#                     else:
#                         desc = lang_P.forge_msg(lang, "give", [Nom_recu], False, 4)
#                 else:
#                     desc = lang_P.forge_msg(lang, "give", [nom, Nom_recu], False, 5)
#                 msg["type"] = "OK"
#             else :
#                 desc = lang_P.forge_msg(lang, "give", None, False, 6)
#                 msg["type"] = "NOK"
#             sql.updateComTime(PlayerID, "give", "gems")
#         except ValueError:
#             desc = lang_P.forge_msg(lang, "WarningMsg", None, False, 3)
#             msg["type"] = "NOK"
#             pass
#     else:
#         desc = lang_P.forge_msg(lang, "couldown", [str(GF.couldown("4s"))])
#         msg["type"] = "couldown"
#     msg["desc"] = desc
#     return msg
