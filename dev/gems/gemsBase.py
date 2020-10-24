from operator import itemgetter
from database import SQLite as sql
from core import level as lvl, utils
from gems import gemsFonctions as GF


def begin(param):
    """Pour créer son compte joueur et obtenir son starter Kit!"""
    name = param["name"]
    lang = param["lang"]
    ID = param["ID"]
    if sql.get_PlayerID(ID, param["name_pl"])['error'] == 404:
        while sql.in_gems("Pseudo", "Pseudo", name) is not False:
            name = "User{0}".format(utils.gen_code(4))
        sql.newPlayer(ID, param["name_pl"], name)
        PlayerID = sql.get_PlayerID(ID, param["name_pl"])
        GF.startKit(PlayerID['ID'])
        return {'error': 0, 'etat': 'OK', 'lang': lang}
    else:
        return {'error': 0, 'etat': 'NOK', 'lang': lang}


def infos(param):
    """**[nom]** | Affiche les informations sur un joueur"""
    lang = param["lang"]
    if param['name'] != "None":
        ID = sql.in_gems("ID_{}".format(param["name_pl"]), "Pseudo", param["name"])
        if ID is not False:
            ID = ID[0][0]
        elif sql.nom_ID(param["name"]) != -1:
            ID = sql.nom_ID(param["name"])
        else:
            ID = param["ID"]
    else:
        ID = param["ID"]
    PlayerID = sql.get_PlayerID(sql.nom_ID(ID), param["name_pl"])

    if PlayerID['error'] != 404:
        PlayerID = PlayerID['ID']
        info = dict()
        # PlayerID
        info['PlayerID'] = PlayerID
        info['Pseudo'] = sql.value(PlayerID, 'gems', 'Pseudo')
        # Balance
        info['Gems'] = sql.value(PlayerID, "gems", "Gems")
        info['Spinelles'] = sql.value(PlayerID, "gems", "Spinelles")
        # Level et XP
        lvlValue = sql.value(PlayerID, "gems", "Level")
        xp = sql.value(PlayerID, "gems", "XP")
        # Niveaux part
        info['Level'] = lvlValue
        info['XP'] = "{0}/{1}".format(xp, lvl.lvlPalier(lvlValue))
        # Parrain/Marraine
        P = sql.value(PlayerID, "gems", "Godparent")
        info['Godparent'] = sql.value(P, "gems", "Pseudo")
        info['Godchilds'] = sql.get_Godchilds(PlayerID)

        return {'error': 0, 'etat': 'OK', 'lang': lang, 'info': info}
        # Message de réussite dans la console
        print("Gems >> Informations de {} affichée".format(sql.value(PlayerID, 'gems', 'Pseudo')))
    else:
        return {'error': 404, 'etat': 'NOK', 'lang': lang}
        # msg["desc"] = lang_P.forge_msg(lang, "WarningMsg", None, False, 6)


def username(param):
    """**{new username}** | Change ton nom d'utilisateur!"""
    lang = param["lang"]
    PlayerID = sql.get_PlayerID(param["ID"], param["name_pl"])['ID']

    if sql.spam(PlayerID, GF.couldown("10s"), "username"):
        if sql.in_gems("Pseudo", "Pseudo", param["NU"]) is False:
            sql.update(PlayerID, "gems", "Pseudo", param["NU"])
            # msg["desc"] = lang_P.forge_msg(lang, "username", None, False, 0)
            sql.updateComTime(PlayerID, "username")
            return {'error': 0, 'etat': 'OK', 'lang': lang}
        else:
            # msg["desc"] = lang_P.forge_msg(lang, "username", None, False, 1)
            return {'error': 2, 'etat': 'NOK', 'lang': lang}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'couldown': str(GF.couldown("10s"))}


def lang(param):
    """Permet de changer la langue pour un joueur."""
    lang = param["lang"]
    langlist = ["EN", "FR"]
    langue = param["langue"].upper()
    ID = sql.get_PlayerID(param["ID"], param["name_pl"])
    if ID['error'] == 404:
        return {'error': 1, 'etat': 'warning', 'lang': lang}
    PlayerID = ID['ID']

    if langue == "NONE":
        return {'error': 0, 'etat': 'OK', 'lang': lang, 'list': langlist}
    else:
        if langue in langlist:
            if sql.update(PlayerID, "gems", "Lang", langue):
                return {'error': 0, 'etat': 'OK', 'lang': langue}
            else:
                return {'error': 3, 'etat': 'NOK', 'lang': lang}
        else:
            return {'error': 2, 'etat': 'NOK', 'lang': lang}


def godparent(param):
    """Permet d'ajouter un joueur comme parrain. En le faisant vous touchez un bonus et lui aussi"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    ID = sql.in_gems("ID_{}".format(param["name_pl"]), "Pseudo", param["GPID"])
    if ID is not False:
        ID = ID[0][0]
    elif sql.nom_ID(param["GPID"]) != -1:
        ID = sql.nom_ID(param["GPID"])
    GPID = sql.get_PlayerID(ID, param["name_pl"])
    if GPID['error'] == 404:
        return {'error': 1, 'etat': 'warning', 'lang': lang}
    GPID = GPID['ID']
    myGP = sql.value(PlayerID, "gems", "Godparent")

    if (myGP == 0 or myGP == None or myGP is False) and PlayerID != GPID:
        sql.update(PlayerID, "gems", "Godparent", GPID)
        lvl.addxp(PlayerID, 15)
        sql.addGems(PlayerID, 100)
        fil_L = sql.get_Godchilds(GPID)
        gainXP = 15 * len(fil_L)
        gainG = 100 * len(fil_L)
        lvl.addxp(GPID, gainXP)
        sql.addGems(GPID, gainG)
        return {'error': 0, 'etat': 'OK', 'lang': lang, 'gain': {'gems': 100, 'XP': 15}, 'gainGP': {'gems': gainG, 'XP': gainXP}}
    elif myGP != 0 and myGP != None and myGP is not False:
        return {'error': 2, 'etat': 'NOK', 'lang': lang, 'myGP': sql.in_gems("Pseudo", "idgems", myGP)[0][0]}
    else:
        return {'error': 3, 'etat': 'NOK', 'lang': lang}


def inventory(param):
    """**[nom de la poche]** | Permet de voir ce que vous avez dans le ventre !"""
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    cat = {
        'outils': {},
        'upgrade': {},
        'items': {
            'special': {},
            'minerai': {},
            'piosson': {},
            'plante': {},
            'consommable': {},
            'emoji': {},
            'event': {}
        }
    }

    if sql.spam(PlayerID, GF.couldown("4s"), "inv"):
        sql.updateComTime(PlayerID, "inv")
        try:
            tailleMax = GF.invMax
            tailletot = 0
            invD = {'error': 0, 'etat': 'OK', 'lang': lang}
            inv = sql.valueAll(PlayerID, "inventory", "Item, Stock, Durability")
            for c in GF.objetOutil:
                for x in inv:
                    if c.nom == str(x[0]):
                        if int(x[1]) > 0:
                            tailletot += c.poids * int(x[1])
                            cat['outils'][c.nom] = {'stock': int(x[1]), 'durability': x[2], 'durabilityMax': c.durabilite}

            for c in GF.objetUpgrade:
                for x in inv:
                    if c.nom == str(x[0]):
                        if int(x[1]) > 0:
                            cat['upgrade'][c.nom] = {'stock': int(x[1])}

            for c in GF.objetItem:
                for x in inv:
                    if c.nom == str(x[0]):
                        if int(x[1]) > 0:
                            # =======================================================================================
                            if c.type == "halloween" or c.type == "christmas" or c.type == "event":
                                cat['items']['event'][c.nom] = {'stock': int(x[1])}
                            # =======================================================================================
                            else:
                                cat['items'][c.type][c.nom] = {'stock': int(x[1])}

                            if c.nom == "backpack" or c.nom == "hyperpack":
                                tailleMax += -1 * c.poids * int(x[1])
                            else:
                                tailletot += c.poids * int(x[1])

            invD['taille'] = [tailletot, tailleMax]
            invD['inventory'] = cat
            return invD
        except:
            return {'error': 2, 'etat': 'NOK', 'lang': lang}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'couldown': GF.couldown("4s")}


def forge(param):
    """**[item] [nombre]** | Permet de concevoir des items spécifiques"""
    item = param["item"]
    nb = param["nb"]
    lang = param["lang"]
    PlayerID = param["PlayerID"]

    if sql.spam(PlayerID, GF.couldown("4s"), "forge"):
        if GF.testInvTaille(PlayerID):
            sql.updateComTime(PlayerID, "forge")
            # -------------------------------------
            # Affichage des recettes disponible
            if item == "None":
                recettes = {}
                for one in GF.objetRecette:
                    recettes[one.nom] = one.items
                return {'error': 0, 'etat': 'OK', 'lang': lang, 'recettes': recettes}
            # -------------------------------------
            else:
                for c in GF.objetRecette:
                    if item == c.nom:
                        for x in c.items:
                            xStock = sql.value(PlayerID, "inventory", "Stock", "Item", x)
                            if int(xStock)*nb < (c.items[x])*nb:
                                return {'error': 4, 'etat': 'NOK', 'lang': lang, 'missing': x, 'nbmissing': (c.items[x]-int(xStock)*nb)}
                        for x in c.items:
                            GF.addInventory(PlayerID, x, (-1*(c.items[x]))*nb)
                        GF.addInventory(PlayerID, item, nb)
                        return {'error': 0, 'etat': 'OK', 'lang': lang}
                    else:
                        return {'error': 3, 'etat': 'NOK', 'lang': lang}
        else:
            return {'error': 2, 'etat': 'NOK', 'lang': lang}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'couldown': GF.couldown("4s")}


def baltop(param):
    """**_{filtre}_ [nombre]** | Classement des joueurs (10 premiers par défaut)"""
    filtre = param["filtre"]
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    if sql.spam(PlayerID, GF.couldown("4s"), "baltop"):
        sql.updateComTime(PlayerID, "baltop")
        UserList = []
        i = 1
        taille = sql.taille("gems")
        while i <= taille:
            IDs = sql.in_gems("Pseudo, Gems, Spinelles, Guilde", "idgems", i)[0]
            print(IDs)
            pseudo = IDs[0]
            gems = IDs[1]
            spinelles = IDs[2]
            guilde = IDs[3]
            if guilde is None or guilde == "":
                guilde = ""
            else:
                guilde = guilde.replace("_", " ")
                guilde = " _{0}_".format(guilde)
            UserList.append([pseudo, gems, spinelles, guilde])
            i = i + 1
        if "gem" in filtre:
            UserList = sorted(UserList, key=itemgetter(1), reverse=True)
        elif "spinelle" in filtre:
            UserList = sorted(UserList, key=itemgetter(2), reverse=True)
        else:
            return {'error': 2, 'etat': 'NOK', 'lang': lang}
        return {'error': 0, 'etat': 'OK', 'lang': lang, 'baltop': UserList}
    else:
        return {'error': 1, 'etat': 'couldown', 'lang': lang, 'couldown': GF.couldown("4s")}
