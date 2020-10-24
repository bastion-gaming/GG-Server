import random as r
import datetime as dt
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from database import SQLite as sql
from gems import gemsItems as GI, gemsStats as GS
import json
# from gems import gemsItems as GI, gemsStats as GS

idGetGems = 620558080551157770
if sql.get_PlayerID(idGetGems, "discord")['error'] == 0:
    PlayerID_GetGems = sql.get_PlayerID(idGetGems, "discord")['ID']
else:
    PlayerID_GetGems = 1

# Taille max de l'Inventaire
invMax = 5000


# Définition des classes
class Item:

    def __init__(self, nom, vente, achat, poids, type):
        self.nom = nom
        self.vente = vente
        self.achat = achat
        self.poids = poids
        self.type = type


class Outil:

    def __init__(self, nom, vente, achat, poids, durabilite, type):
        self.nom = nom
        self.vente = vente
        self.achat = achat
        self.poids = poids
        self.durabilite = durabilite
        self.type = type


class Upgrade:

    def __init__(self, nom, vente, achat, type):
        self.nom = nom
        self.vente = vente
        self.achat = achat
        self.type = type


class Recette:

    def __init__(self, nom, type, items):
        self.nom = nom
        self.type = type
        self.items = items


def itemBourse(item, type):
    """Version 3.0 | Attribue les prix de la bourse """
    # récupération du fichier de sauvegarde de la bourse
    with open('gems/bourse.json', 'r') as fp:
        dict = json.load(fp)
    temp = dict[item]
    # Récuperation de la valeur courante
    if type == "vente":
        pnow = temp["vente"]
    elif type == "achat":
        pnow = temp["achat"]
    PrixMini = 2

    # Verification pour l'actualisation de la bourse
    if sql.spam(PlayerID_GetGems, couldown("8h"), "bourse"):
        # Gestion des exceptions
        if item in GI.exception:
            return pnow
        if item in ObjetEventEnd:
            return pnow

        # Récuperation prix d'origine | prix mini | prix maxi
        taux = 0.9
        for c in GI.PrixItem:
            if c.nom == item:
                if type == "vente":
                    pdef = c.vente
                    pmini = c.vente - (c.vente*taux)
                    pmaxi = c.vente + (c.vente*taux)
                elif type == "achat":
                    pdef = c.achat
                    pmini = c.achat - (c.achat*taux)
                    pmaxi = c.achat + (c.achat*taux)
        for c in GI.PrixOutil:
            if c.nom == item:
                if type == "vente":
                    pdef = c.vente
                    pmini = c.vente - (c.vente*taux)
                    pmaxi = c.vente + (c.vente*taux)
                elif type == "achat":
                    pdef = c.achat
                    pmini = c.achat - (c.achat*taux)
                    pmaxi = c.achat + (c.achat*taux)

        pdef = int(pdef)
        if pmini <= PrixMini:
            pmini = PrixMini
        else:
            pmini = int(pmini)
        pmaxi = int(pmaxi)
        # print("============================================\n=== {0} >>> {1}".format(type, item))
        # print("Prix défaut: {0}\nPrix mini: {1}\nPrix maxi: {2}".format(pdef, pmini, pmaxi))

        # Fonctionnement de la bourse
        DcrackB = r.randint(1, 1000)
        # crack boursier négatif
        if DcrackB <= 5:
            taux = 0.85
            Prix = int(pnow - (pnow*taux))
        # crack boursier positif
        elif DcrackB >= 985 or (pnow < 4 and DcrackB >= 900):
            if pnow <= 50:
                taux = 10
            elif pnow <= 7:
                taux = 50
            else:
                taux = 5
            Prix = int(pnow + (pnow*taux))
        # évolution de la bourse normale (entre -10% et +10% de la valeur courante)
        else:
            if pnow > pmaxi:
                pourcentage = r.randint(-20, -5)
            elif pnow <= pmini:
                pourcentage = r.randint(15, 30)
            elif (pnow > (pmaxi - pdef*0.3)) or (pnow < (pmini + pdef*0.3)):
                pourcentage = r.randint(-20, 20)
            else:
                if pnow > 10:
                    pourcentage = r.randint(-10, 10)
                else:
                    pourcentage = r.randint(-5, 20)
            Prix = int(pnow + ((pnow*pourcentage)//100))
        if Prix < PrixMini:
            Prix = PrixMini
        # print("\nAncien prix: {1}\nNouveau prix: {0}\n".format(Prix, pnow))

        # La valeur de vente ne peux etre supérieur à la valeur d'achat
        if type == "vente":
            if Prix > temp["achat"]:
                Prix = temp["achat"]
            temp["vente"] = Prix
            temp["precVente"] = pnow
        # La valeur d'achat ne peux être inférieur à la valeur de vente
        elif type == "achat":
            if Prix < temp["vente"]:
                Prix = temp["vente"]
            temp["achat"] = Prix
            temp["precAchat"] = pnow
        # actualisation du fichier de sauvegarde de la bourse
        dict[item] = temp
        with open('gems/bourse.json', 'w') as fp:
            json.dump(dict, fp, indent=4)
        return Prix
    else:
        return pnow
# <<< def itemBourse(item, type):


def ActuBourse():
    # Start the scheduler
    sched = BackgroundScheduler()
    dd = datetime.now() + timedelta(minutes=30)
    job = sched.add_job(loadItem, 'date', run_date=dd)
    sched.start()


# Fonction d'actualisation/initialisation des items
def loadItem(F=False):
    jour = dt.date.today()

    # Récupere le multiplicateur
    m = 1
    # if jour.day == 5 or jour.day == 13 or jour.day == 20:
    #     path = "core/saisons.json"
    #     with open(path, encoding='utf-8') as json_file:
    #         data = json.load(json_file)
    #     m = data["mult"]
    #     if m <= 0:
    #         m = 1

    if F:
        GI.initBourse()
    global ObjetEventEnd
    ObjetEventEnd = []
    # ========== Items ==========

    global objetItem
    objetItem = [
        Item("backpack", m*itemBourse("backpack", "vente"), m*itemBourse("backpack", "achat"), -200, "special"),
        Item("hyperpack", m*itemBourse("hyperpack", "vente"), m*itemBourse("hyperpack", "achat"), -2000, "special"),
        Item("fishhook", m*itemBourse("fishhook", "vente"), m*itemBourse("fishhook", "achat"), 1, "special"),

        Item("cobblestone", m*itemBourse("cobblestone", "vente"), m*itemBourse("cobblestone", "achat"), 4, "minerai"),
        Item("iron", m*itemBourse("iron", "vente"), m*itemBourse("iron", "achat"), 10, "minerai"),
        Item("gold", m*itemBourse("gold", "vente"), m*itemBourse("gold", "achat"), 20, "minerai"),
        Item("diamond", m*itemBourse("diamond", "vente"), m*itemBourse("diamond", "achat"), 40, "minerai"),
        Item("emerald", m*itemBourse("emerald", "vente"), m*itemBourse("emerald", "achat"), 50, "minerai"),
        Item("ruby", m*itemBourse("ruby", "vente"), m*itemBourse("ruby", "achat"), 70, "minerai"),

        Item("fish", m*itemBourse("fish", "vente"), m*itemBourse("fish", "achat"), 2, "poisson"),
        Item("tropicalfish", m*itemBourse("tropicalfish", "vente"), m*itemBourse("tropicalfish", "achat"), 8, "poisson"),
        Item("blowfish", m*itemBourse("blowfish", "vente"), m*itemBourse("blowfish", "achat"), 8, "poisson"),
        Item("octopus", m*itemBourse("octopus", "vente"), m*itemBourse("octopus", "achat"), 16, "poisson"),

        Item("seed", m*itemBourse("seed", "vente"), m*itemBourse("seed", "achat"), 0.5, "plante"),
        Item("cacao", m*itemBourse("cacao", "vente"), m*itemBourse("cacao", "achat"), 1, "plante"),
        Item("potato", m*itemBourse("potato", "vente"), m*itemBourse("potato", "achat"), 1, "plante"),

        Item("oak", m*itemBourse("oak", "vente"), m*itemBourse("oak", "achat"), 50, "plante"),
        Item("spruce", m*itemBourse("spruce", "vente"), m*itemBourse("spruce", "achat"), 70, "plante"),
        Item("palm", m*itemBourse("palm", "vente"), m*itemBourse("palm", "achat"), 60, "plante"),
        Item("wheat", m*itemBourse("wheat", "vente"), m*itemBourse("wheat", "achat"), 3, "plante"),
        Item("grapes", m*itemBourse("grapes", "vente"), m*itemBourse("grapes", "achat"), 1, "plante"),

        Item("wine_glass", m*itemBourse("wine_glass", "vente"), m*itemBourse("wine_glass", "achat"), 2, "consommable"),
        Item("beer", m*itemBourse("beer", "vente"), m*itemBourse("beer", "achat"), 2, "consommable"),

        Item("chocolate", m*itemBourse("chocolate", "vente"), m*itemBourse("chocolate", "achat"), 3, "consommable"),
        Item("fries", m*itemBourse("fries", "vente"), m*itemBourse("fries", "achat"), 30, "consommable"),
        Item("cookie", m*itemBourse("cookie", "vente"), m*itemBourse("cookie", "achat"), 1, "consommable"),
        Item("candy", m*itemBourse("candy", "vente"), m*itemBourse("candy", "achat"), 1, "consommable"),
        Item("lollipop", m*itemBourse("lollipop", "vente"), m*itemBourse("lollipop", "achat"), 2, "consommable")
    ]

    if not (jour.month == 10 and jour.day >= 22) or (jour.month == 11 and jour.day <= 10):
        for one in GI.ObjetHalloween:
            ObjetEventEnd.append(one)
    if not (jour.month == 12 and jour.day >= 20) or (jour.month == 1 and jour.day <= 14):
        for one in GI.ObjetChristmas:
            ObjetEventEnd.append(one)

    objetItem += [
        Item("pumpkin", m*itemBourse("pumpkin", "vente"), m*itemBourse("pumpkin", "achat"), 5, "halloween"),
        Item("pumpkinpie", m*itemBourse("pumpkinpie", "vente"), m*itemBourse("pumpkinpie", "achat"), 30, "halloween")
    ]

    objetItem += [
        Item("cupcake", m*itemBourse("cupcake", "vente"), m*itemBourse("cupcake", "achat"), 10, "christmas")
    ]

    # ========== Outils ==========

    global objetOutil
    objetOutil = [
        Outil("fishingrod", itemBourse("fishingrod", "vente"), itemBourse("fishingrod", "achat"), 25, 100, ""),

        Outil("pickaxe", itemBourse("pickaxe", "vente"), itemBourse("pickaxe", "achat"), 15, 75, ""),
        Outil("iron_pickaxe", itemBourse("iron_pickaxe", "vente"), itemBourse("iron_pickaxe", "achat"), 70, 200, "forge"),
        Outil("diamond_pickaxe", itemBourse("diamond_pickaxe", "vente"), itemBourse("diamond_pickaxe", "achat"), 150, 450, "forge"),

        Outil("shovel", itemBourse("shovel", "vente"), itemBourse("shovel", "achat"), 10, 35, ""),
        Outil("iron_shovel", itemBourse("iron_shovel", "vente"), itemBourse("iron_shovel", "achat"), 60, 100, "forge"),
        Outil("diamond_shovel", itemBourse("diamond_shovel", "vente"), itemBourse("diamond_shovel", "achat"), 120, 240, "forge"),

        Outil("planting_plan", itemBourse("planting_plan", "vente"), itemBourse("planting_plan", "achat"), 4, 4, "consommable"),
        Outil("barrel", itemBourse("barrel", "vente"), itemBourse("barrel", "achat"), 3, 3, "consommable"),
        Outil("furnace", itemBourse("furnace", "vente"), itemBourse("furnace", "achat"), 2, 2, "consommable")
    ]

    if sql.spam(PlayerID_GetGems, couldown("8h"), "bourse"):
        sql.updateComTime(PlayerID_GetGems, "bourse")
        for x in objetItem:
            GS.csv_add(x.nom)
        for x in objetOutil:
            GS.csv_add(x.nom)
    ActuBourse()
# <<< def loadItem(F = None):


##############################################
# ========== Recettes ==========

objetRecette = [
    Recette("iron_pickaxe", "forge", {'iron': 20, 'pickaxe': 1}),
    Recette("diamond_pickaxe", "forge", {'diamond': 45, 'iron_pickaxe': 1}),

    Recette("iron_shovel", "forge", {'iron': 16, 'shovel': 1}),
    Recette("diamond_shovel", "forge", {'diamond': 30, 'iron_shovel': 1})
]

# ========== Upgrade ==========

global objetUpgrade
objetUpgrade = [
    Upgrade("bank", 0, 10000, "bank")
]


def couldown(couldown):
    d = dict()
    d["couldown"] = couldown.lower()
    # ======= Jours =======
    if "j" in d["couldown"]:
        couldown_split(d, "j")
        d["j"] = d["j"]*3600*24
    else:
        d["j"] = 0
    # ======= Heures =======
    if "h" in d["couldown"]:
        couldown_split(d, "h")
        d["h"] = d["h"]*3600
    else:
        d["h"] = 0
    # ======= Minutes =======
    if "m" in d["couldown"]:
        couldown_split(d, "m")
        d["m"] = d["m"]*60
    else:
        d["m"] = 0
    # ======= Secondes =======
    if "s" in d["couldown"]:
        couldown_split(d, "s")
    else:
        d["s"] = 0
    # ======= Résultat =======
    # print("{0}:{1}:{2}:{3}".format(d["j"], d["h"], d["m"], d["s"]))
    n = d["j"] + d["h"] + d["m"] + d["s"]
    return n


def couldown_split(dict, s):
    temp = dict["couldown"].split(s)
    dict[s] = int(temp[0])
    dict["couldown"] = temp[1]
    return dict


def get_price(nameElem, type = None):
    """Permet de connaitre le prix de l'item"""
    if type == None or type == "vente":
        for c in objetItem:
            if c.nom == nameElem:
                return c.vente

        for c in objetOutil:
            if c.nom == nameElem:
                return c.vente
    elif type == "achat":
        for c in objetItem:
            if c.nom == nameElem:
                return c.achat

        for c in objetOutil:
            if c.nom == nameElem:
                return c.achat
    return 0


def testInvTaille(ID):
    """Verifie si l'inventaire est plein """
    inv = sql.valueAll(ID, "inventory", ["Item", "Stock"])
    tailletot = 0
    if inv != [] or inv is not False:
        for c in objetOutil:
            for x in inv:
                if c.nom == str(x[0]):
                    if int(x[1]) > 0:
                        tailletot += c.poids*int(int(x[1]))

        for c in objetItem:
            for x in inv:
                if c.nom == str(x[0]):
                    if int(x[1]) > 0:
                        tailletot += c.poids*int(int(x[1]))

    if tailletot <= invMax:
        return True
    else:
        return False


def taxe(solde, pourcentage):
    """Affiche la somme de la taxe en fonction du pourcentage """
    taxe = dict()
    taxe["taxe"] = solde * pourcentage
    taxe["new solde"] = solde - taxe["taxe"]
    return taxe


def startKit(ID):
    gems = sql.value(ID, "gems", "Gems")
    if gems == 0:
        sql.addGems(ID, 100)
        addInventory(ID, "pickaxe", 1)
        addInventory(ID, "fishingrod", 1)
        addInventory(ID, "shovel", 1)
        sql.update(ID, "inventory", "Durability", 20, "Item", "pickaxe")
        sql.update(ID, "inventory", "Durability", 20, "Item", "fishingrod")
        sql.update(ID, "inventory", "Durability", 20, "Item", "shovel")


def ChiffreRomain(nb):
    # Transforme un chiffre arabe (nb) en chiffre romain (CR)
    # minimum = 1
    # maximum = 1000
    CR = ""
    CR_I = 'I'  # 1
    CR_X = 'X'  # 10
    CR_C = 'C'  # 100
    CR_M = 'M'  # 1000

    if nb == 1000:
        return CR_M
    elif nb > 1000:
        return nb
    nbc = nb // 100
    nbd = (nb % 100) // 10
    nbu = nb % 10

    if nbc < 4:
        CR += "{0}".format(CR_C*nbc)
    elif nbc == 4:
        CR += "CD"
    elif nbc < 9:
        CR += "D{0}".format(CR_C*(nbc-5))
    elif nbc == 9:
        CR += "CM"

    if nbd < 4:
        CR += "{0}".format(CR_X*nbd)
    elif nbd == 4:
        CR += "XL"
    elif nbd < 9:
        CR += "L{0}".format(CR_X*(nbd-5))
    elif nbd == 9:
        CR += "XC"

    if nbu < 4:
        CR += "{0}".format(CR_I*nbu)
    elif nbu == 4:
        CR += "IV"
    elif nbu < 9:
        CR += "V{0}".format(CR_I*(nbu-5))
    elif nbu == 9:
        CR += "IX"
    return CR


def param_prod(item):
    res = dict()
    # Items utilisé dans la production de la serre (hothouse)
    if item == "seed":
        res["nbitem"] = 1
        De = r.randint(1, 16)
        if De <= 5:
            res["nbgain"] = r.randint(1, 2)
            res["gain"] = "oak"
        elif De > 5 and De <= 9:
            res["nbgain"] = r.randint(1, 2)
            res["gain"] = "spruce"
        elif De > 9 and De <= 12:
            res["nbgain"] = r.randint(1, 2)
            res["gain"] = "palm"
        elif De > 12 and De <= 14:
            res["nbgain"] = r.randint(4, 10)
            res["gain"] = "wheat"
        elif De > 14:
            res["nbgain"] = r.randint(6, 12)
            res["gain"] = "grapes"

        res["couldown"] = couldown("6h")
        res["couldownMsg"] = ":clock6:`6h`"
    elif item == "pumpkinH":
        res["nbitem"] = 1
        res["gain"] = "pumpkin"
        res["nbgain"] = r.randint(2, 5)
        res["couldown"] = couldown("4h")
        res["couldownMsg"] = ":clock4:`4h`"

    # Items utilisé dans la production de la cave (ferment)
    elif item == "grapes":
        res["nbitem"] = 10
        res["gain"] = "wine_glass"
        res["nbgain"] = r.randint(1, 4)
        res["couldown"] = couldown("3h")
        res["couldownMsg"] = ":clock3:`3h`"
    elif item == "wheat":
        res["nbitem"] = 8
        res["gain"] = "beer"
        res["nbgain"] = r.randint(2, 6)
        res["couldown"] = couldown("8h")
        res["couldownMsg"] = ":clock8:`8h`"

    # Items utilisé dans la production de la cuisine (cooking)
    elif item == "potato":
        res["nbitem"] = 6
        res["gain"] = "fries"
        res["nbgain"] = r.randint(1, 5)
        res["couldown"] = couldown("3h")
        res["couldownMsg"] = ":clock3:`3h`"
    elif item == "cacao":
        res["nbitem"] = 4
        res["gain"] = "chocolate"
        res["nbgain"] = r.randint(1, 5)
        res["couldown"] = couldown("2h")
        res["couldownMsg"] = ":clock2:`2h`"
    elif item == "chocolate":
        res["nbitem"] = 8
        res["gain"] = "cupcake"
        res["nbgain"] = r.randint(1, 4)
        res["couldown"] = couldown("4h")
        res["couldownMsg"] = ":clock4:`4h`"
    elif item == "pumpkin":
        res["nbitem"] = 12
        res["gain"] = "pumpkinpie"
        res["nbgain"] = r.randint(1, 4)
        res["couldown"] = couldown("2h")
        res["couldownMsg"] = ":clock2:`2h`"

    # Autre
    else:
        res["nbitem"] = 0
        res["gain"] = ""
        res["nbgain"] = 0
        res["couldown"] = 0
        res["couldownMsg"] = ""
    return res


def time_aff(time):
    # Traduit une valeur time (en secondes) en valeur HH:mm:ss
    # (avec un emoji correspondant devant)
    dtime = dict()
    dtime["timeH"] = int(time / 60 / 60)
    dtime["time"] = time - dtime["timeH"] * 3600
    dtime["timeM"] = int(dtime["time"] / 60)
    dtime["timeS"] = int(dtime["time"] - dtime["timeM"] * 60)
    if dtime["timeM"] <= 30:
        if dtime["timeH"] % 12 == 0:
            dtime["cl"] = "12"
        else:
            dtime["cl"] = dtime["timeH"] % 12
        dtime["cl"] = "clock{0}30".format(dtime["cl"])
    else:
        if dtime["timeH"] % 12 == 0:
            dtime["cl"] = "12"
        else:
            dtime["cl"] = (dtime["timeH"] % 12)+1
        dtime["cl"] = "clock{0}".format(dtime["cl"])
    return dtime


def addInventory(PlayerID, fieldName, fieldValue):
    """
    int             PlayerID: id du joueur dans la base de données
    string          nameDB: Nom de la table
    string          fieldName: Item a modifier
    string          fieldValue: valeur associé au fieldName
    """
    nameDB = 'inventory'
    try:
        old_value = sql.value(PlayerID, nameDB, "Stock", "Item", fieldName)
        if old_value is not False:
            new_value = int(old_value) + int(fieldValue)
            if new_value < 0:
                new_value = 0
            if sql.update(PlayerID, nameDB, "Stock", new_value, "Item", fieldName):
                return True
            else:
                return False
        else:
            if sql.create(PlayerID, nameDB, ["Item", "Stock"], [fieldName, fieldValue]):
                return True
            else:
                return False
    except:
        return False


def addStats(PlayerID, fieldName, fieldValue):
    """
    int             PlayerID: id du joueur dans la base de données
    string          nameDB: Nom de la table
    tab             fieldName: Item a modifier
    string          fieldValue: valeur associé au fieldName
    """
    nameDB = 'statgems'
    try:
        old_value = sql.value(PlayerID, nameDB, "Stock", ["Nom", "Type"], [fieldName[1], fieldName[0]])
        if old_value is not False:
            new_value = int(old_value) + int(fieldValue)
            if new_value < 0:
                new_value = 0
            if sql.update(PlayerID, nameDB, "Stock", new_value, ["Nom", "Type"], [fieldName[1], fieldName[0]]):
                return True
            else:
                return False
        else:
            if sql.create(PlayerID, nameDB, ["Nom", "Type", "Stock"], [fieldName[1], fieldName[0], fieldValue]):
                return True
            else:
                return False
    except:
        return False


def addSuccess(PlayerID, fieldName, fieldValue):
    """
    int             PlayerID: id du joueur dans la base de données
    string          nameDB: Nom de la table
    tab             fieldName: Item a modifier
    string          fieldValue: valeur associé au fieldName
    """
    nameDB = 'success'
    try:
        old_value = sql.value(PlayerID, nameDB, "Stock", "idsuccess", fieldName)
        if old_value is not False:
            new_value = int(old_value) + int(fieldValue)
            if new_value < 0:
                new_value = 0
            if sql.update(PlayerID, nameDB, "Stock", new_value, "idsuccess", fieldName):
                return True
            else:
                return False
        else:
            if sql.create(PlayerID, nameDB, ["idsuccess", "Stock"], [fieldName, fieldValue]):
                return True
            else:
                return False
    except:
        return False


def durability(PlayerID, outil):
    # gestion de la durabilité d'un outil
    stock = sql.value(PlayerID, "inventory", "Stock", "Item", outil)
    if stock is not False:
        nb = int(stock)
        if nb > 0:
            sql.update(PlayerID, "inventory", "Durability", -1, "Item", outil)
            if sql.value(PlayerID, "inventory", "Durability", "Item", outil) <= 0:
                for c in objetOutil:
                    if c.nom == outil:
                        sql.update(PlayerID, "inventory", "Durability", c.durabilite, "Item", outil)
                addInventory(PlayerID, outil, -1)
                return True
    return False
