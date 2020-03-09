import json
import datetime as dt

jour = dt.date.today()
exception = ["bank_upgrade", "backpack", "hyperpack", "candy", "lollipop", "fishhook", "pickaxe", "shovel", "fishingrod"]
objetEmoji = ["grapes", "wine_glass", "beer", "cookie"]

# ========== Items ==========
class Item:

    def __init__(self, nom, vente, achat):
        self.nom = nom
        self.vente = vente
        self.achat = achat


PrixItem = [
    Item("cobblestone", 15, 20),
    Item("iron", 30, 100),
    Item("gold", 50, 120),
    Item("diamond", 150, 180),
    Item("emerald", 190, 220),
    Item("ruby", 770, 800),

    Item("fish", 10, 40),
    Item("tropicalfish", 30, 120),
    Item("blowfish", 40, 130),
    Item("octopus", 60, 200),

    Item("seed", 20, 220),
    Item("cacao", 22, 230),
    Item("potato", 25, 240),

    Item("oak", 60, 70),
    Item("spruce", 70, 82),
    Item("palm", 85, 90),
    Item("wheat", 60, 80),
    Item("grapes", 12, 20),

    Item("wine_glass", 150, 170),
    Item("beer", 404, 1664),

    Item("chocolate", 201, 250),
    Item("fries", 160, 185),
    Item("cookie", 30, 40),
    Item("candy", 1, 2),
    Item("lollipop", 5, 12),

    Item("backpack", 3000, 3000),
    Item("hyperpack", 29000, 29000),
    Item("fishhook", 46, 64)
    ]

ObjetHalloween = ["pumpkin", "pumpkinpie"]
PrixItem += [
    Item("pumpkin", 65, 75),
    Item("pumpkinpie", 790, 850)
    ]

ObjetChristmas = ["cupcake"]
PrixItem += [
    Item("cupcake", 1700, 2000)
    ]


# ========== Outils ==========
class Outil:

    def __init__(self, nom, vente, achat):
        self.nom = nom
        self.vente = vente
        self.achat = achat


PrixOutil = [
    Outil("pickaxe", 40, 80),
    Outil("shovel", 30, 60),
    Outil("fishingrod", 35, 100),

    Outil("iron_pickaxe", 120, 2200),
    Outil("diamond_pickaxe", 300, 11000),

    Outil("iron_shovel", 100, 1800),
    Outil("diamond_shovel", 500, 8000),

    Outil("planting_plan", 150, 150),
    Outil("barrel", 600, 600),
    Outil("furnace", 100, 100),

    Outil("bank_upgrade", 0, 10000)
    ]


def initBourse():
    try:
        # essaie de lire le fichier bourse.json
        with open('gems/bourse.json', 'r') as fp:
            value = json.load(fp)
        for x in PrixItem:
            checkItemBourse(value, x.nom)
        for x in PrixOutil:
            checkItemBourse(value, x.nom)
    except:
        # Création du fichier bourse.json avec les valeurs par défaut
        dict = {}
        for x in PrixItem:
            dict[x.nom] = {"vente": x.vente, "achat": x.achat, "precVente": x.vente, "precAchat": x.achat}
        for x in PrixOutil:
            dict[x.nom] = {"vente": x.vente, "achat": x.achat, "precVente": x.vente, "precAchat": x.achat}
        with open('gems/bourse.json', 'w') as fp:
            json.dump(dict, fp, indent=4)


def checkItemBourse(value, item):
    check = False
    key = value.keys()
    # print("## {} ##".format(item))
    for x in PrixItem:
        if x.nom == item:
            for one in key:
                if item == one:
                    # print(">> {}".format(x.nom))
                    check = True
        # else:
        #     print(x.nom)
    for x in PrixOutil:
        if x.nom == item:
            for one in key:
                if item == one:
                    # print(">> {}".format(x.nom))
                    check = True
    #     else:
    #         print(x.nom)
    # print("===============")
    if not check:
        for x in PrixItem:
            if x.nom == item:
                dict[x.nom] = {"vente": x.vente, "achat": x.achat, "precVente": x.vente, "precAchat": x.achat}
        for x in PrixOutil:
            if x.nom == item:
                dict[x.nom] = {"vente": x.vente, "achat": x.achat, "precVente": x.vente, "precAchat": x.achat}
        with open('gems/bourse.json', 'w') as fp:
            json.dump(dict, fp, indent=4)
    return True
