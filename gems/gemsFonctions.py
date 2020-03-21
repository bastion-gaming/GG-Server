import random as r
import datetime as dt
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from DB import TinyDB as DB, SQLite as sql
import json
from gems import gemsItems as GI, gemsStats as GS
from languages import lang as lang_P

idBaBot = 604776153458278415
idGetGems = 620558080551157770
try:
    PlayerID_GetGems = sql.get_PlayerID(sql.get_SuperID(idGetGems, "discord"))
    PlayerID_Babot = sql.get_PlayerID(sql.get_SuperID(idBaBot, "discord"))
except:
    PlayerID_GetGems = 1
    PlayerID_Babot = 2


# def checkDB_Guilde():
#     if DB.dbExist("DB/guildesDB"):
#         print("Guildes >> La DB existe, poursuite sans soucis.")
#     else:
#         print("Guildes >> La DB n'existait pas. Elle a été (re)créée.")
#     flag = DB.checkField("DB/guildesDB", "DB/Templates/guildesTemplate")
#     if flag == 0:
#         print("DB >> Aucun champ n'a été ajouté, supprimé ou modifié.")
#     elif "add" in flag:
#         print("DB >> Un ou plusieurs champs ont été ajoutés à la DB.")
#     elif "type" in flag:
#         print("DB >> Un ou plusieurs type ont été modifié sur la DB.")
#     elif "sup" in flag:
#         print("DB >> Un ou plusieurs champs ont été supprimés de la DB.")


# Taille max de l'Inventaire
invMax = 5000


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
    if sql.spam(PlayerID_GetGems, couldown_8h, "bourse", "gems"):
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
    if jour.day == 5 or jour.day == 13 or jour.day == 20:
        path = "core/saisons.json"
        with open(path, encoding='utf-8') as json_file:
            data = json.load(json_file)
        m = data["mult"]
        if m <= 0:
            m = 1

    if F:
        GI.initBourse()
    global ObjetEventEnd
    ObjetEventEnd = []
    # ========== Items ==========
    class Item:

        def __init__(self, nom, vente, achat, poids, type):
            self.nom = nom
            self.vente = vente
            self.achat = achat
            self.poids = poids
            self.type = type

    global objetItem
    objetItem = [
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
        Item("grapes", m*itemBourse("grapes", "vente"), m*itemBourse("grapes", "achat"), 1, "emoji"),

        Item("wine_glass", m*itemBourse("wine_glass", "vente"), m*itemBourse("wine_glass", "achat"), 2, "emoji"),
        Item("beer", m*itemBourse("beer", "vente"), m*itemBourse("beer", "achat"), 2, "emoji"),

        Item("chocolate", m*itemBourse("chocolate", "vente"), m*itemBourse("chocolate", "achat"), 3, "consommable"),
        Item("fries", m*itemBourse("fries", "vente"), m*itemBourse("fries", "achat"), 30, "consommable"),
        Item("cookie", m*itemBourse("cookie", "vente"), m*itemBourse("cookie", "achat"), 1, "emoji"),
        Item("candy", m*itemBourse("candy", "vente"), m*itemBourse("candy", "achat"), 1, "emoji"),
        Item("lollipop", m*itemBourse("lollipop", "vente"), m*itemBourse("lollipop", "achat"), 2, "emoji"),

        Item("backpack", m*itemBourse("backpack", "vente"), m*itemBourse("backpack", "achat"), -200, "special"),
        Item("hyperpack", m*itemBourse("hyperpack", "vente"), m*itemBourse("hyperpack", "achat"), -2000, "special"),
        Item("fishhook", m*itemBourse("fishhook", "vente"), m*itemBourse("fishhook", "achat"), 1, "special")
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
    class Outil:

        def __init__(self, nom, vente, achat, poids, durabilite, type):
            self.nom = nom
            self.vente = vente
            self.achat = achat
            self.poids = poids
            self.durabilite = durabilite
            self.type = type

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
        Outil("furnace", itemBourse("furnace", "vente"), itemBourse("furnace", "achat"), 2, 2, "consommable"),

        Outil("bank_upgrade", itemBourse("bank_upgrade", "vente"), itemBourse("bank_upgrade", "achat"), 10000, None, "bank")
    ]

    # ========== Loot Box ==========
    class Box:

        def __init__(self, nom, titre, achat, min, max, type, xp):
            self.nom = nom
            self.titre = titre
            self.achat = achat
            self.min = min
            self.max = max
            self.type = type
            self.xp = xp

    global objetBox
    objetBox = [
        Box("commongems", "Gems Common", 30, 10, 50, "gems", 1),
        Box("raregems", "Gems Rare", 300, 100, 500, "gems", 2),
        Box("legendarygems", "Gems Legendary", 3000, 1000, 5000, "gems", 4),

        Box("gift", "Items en folie", 50000, 100, 100000, "gems", 3),
        Box("gift_heart", "Cadeau de la Saint Valentin", 0, 10000, 50000, "", 2)
    ]

    if sql.spam(PlayerID_GetGems, couldown_8h, "bourse", "gems"):
        sql.updateComTime(PlayerID_GetGems, "bourse", "gems")
        for x in objetItem:
            GS.csv_add(x.nom)
        for x in objetOutil:
            GS.csv_add(x.nom)
    ActuBourse()
# <<< def loadItem(F = None):


##############################################
# ========== Recettes ==========
class Recette:

    def __init__(self, nom, type, nb1, item1, nb2, item2, nb3, item3, nb4, item4):
        self.nom = nom
        self.type = type
        self.nb1 = nb1
        self.item1 = item1
        self.nb2 = nb2
        self.item2 = item2
        self.nb3 = nb3
        self.item3 = item3
        self.nb4 = nb4
        self.item4 = item4


objetRecette = [
    Recette("iron_pickaxe", "forge", 20, "iron", 1, "pickaxe", 0, "", 0, ""),
    Recette("diamond_pickaxe", "forge", 45, "diamond", 1, "iron_pickaxe", 0, "", 0, ""),

    Recette("iron_shovel", "forge", 16, "iron", 1, "shovel", 0, "", 0, ""),
    Recette("diamond_shovel", "forge", 30, "diamond", 1, "iron_shovel", 0, "", 0, "")
]


# ========== Couldown pour la fonction antispam ==========
couldown_72h = 86400*3
couldown_48h = 86400*2
couldown_36h = 86400 + 86400/2
couldown_24h = 86400
couldown_23h = 3600*23
couldown_22h = 3600*22
couldown_21h = 3600*21
couldown_20h = 3600*20
couldown_19h = 3600*19
couldown_18h = 3600*18
couldown_17h = 3600*17
couldown_16h = 3600*16
couldown_15h = 3600*15
couldown_14h = 3600*14
couldown_13h = 3600*13
couldown_12h = 3600*12
couldown_11h = 3600*11
couldown_10h = 3600*10
couldown_9h = 3600*9
couldown_8h = 3600*8
couldown_7h = 3600*7
couldown_6h = 3600*6
couldown_5h = 3600*5
couldown_4h = 3600*4
couldown_3h = 3600*3
couldown_2h = 3600*2
couldown_1h = 3600
couldown_30m = 3600/2
couldown_20m = 3600/3
couldown_15m = 3600/4
couldown_10m = 3600/6
couldown_5m = 3600/12
couldown_30s = 30
couldown_15s = 15
couldown_10s = 10
couldown_8s = 8
couldown_6s = 6
couldown_4s = 4


def recette(lang):
    """Liste de toutes les recettes disponibles !"""
    d_recette = lang_P.forge_msg(lang, "recette")
    d_recette += "▬▬▬▬▬▬▬▬▬▬▬▬▬\n**Forge**\n"
    for c in objetOutil:
        for R in objetRecette:
            if c.type == "forge":
                if c.nom == R.nom:
                    d_recette += "<:gem_{0}:{1}>`{0}`: ".format(c.nom, "{idmoji[gem_" + c.nom + "]}")
                    if R.nb1 > 0:
                        d_recette += "{0} <:gem_{1}:{2}>`{1}` ".format(R.nb1, R.item1, "{idmoji[gem_" + R.item1 + "]}")
                    if R.nb2 > 0:
                        d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(R.nb2, R.item2, "{idmoji[gem_" + R.item2 + "]}")
                    if R.nb3 > 0:
                        d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(R.nb3, R.item3, "{idmoji[gem_" + R.item3 + "]}")
                    if R.nb4 > 0:
                        d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(R.nb4, R.item4, "{idmoji[gem_" + R.item4 + "]}")
                    d_recette += "\n"

    return d_recette


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
    inv = sql.valueAt(ID, "all", "inventory")
    tailletot = 0
    if inv != 0:
        for c in objetOutil:
            for x in inv:
                if c.nom == str(x[1]):
                    if int(x[0]) > 0:
                        tailletot += c.poids*int(int(x[0]))

        for c in objetItem:
            for x in inv:
                if c.nom == str(x[1]):
                    if int(x[0]) > 0:
                        tailletot += c.poids*int(int(x[0]))

    if tailletot <= invMax:
        return True
    else:
        return False


def testGuildInvTaille(ID):
    """Verifie si ton coffre de guilde est plein """
    inv = DB.valueAt(ID, "Coffre", "DB/guildesDB")
    tailletot = 0
    for c in objetOutil:
        for x in inv:
            if c.nom == str(x):
                if inv[x] > 0:
                    tailletot += c.poids*int(inv[x])

    for c in objetItem:
        for x in inv:
            if c.nom == str(x):
                if inv[x] > 0:
                    tailletot += c.poids*int(inv[x])

    if tailletot <= invMax:
        return True
    else:
        return False


def taxe(solde, pourcentage):
    """Affiche la somme de la taxe en fonction du pourcentage """
    soldeTaxe = solde * pourcentage
    soldeNew = solde - soldeTaxe
    return (soldeTaxe, soldeNew)


def startKit(ID):
    gems = sql.valueAtNumber(ID, "gems", "gems")
    if gems == 0:
        sql.addGems(ID, 100)
        sql.add(ID, "pickaxe", 1, "inventory")
        sql.add(ID, "fishingrod", 1, "inventory")
        sql.add(ID, "shovel", 1, "inventory")
        sql.add(ID, "pickaxe", 20, "durability")
        sql.add(ID, "fishingrod", 20, "durability")
        sql.add(ID, "shovel", 20, "durability")


def gift(PlayerID, lang, param = False):
    desc = ""
    jour = dt.date.today()
    nbgift = r.randint(-3, 3)

    if param:
        nbgift = r.randint(1, 3)
        sql.add(PlayerID, "lootbox_gift", nbgift, "inventory")
        sql.add(PlayerID, ["boxes", "lootbox | gift | gain"], nbgift, "statgems")
        desc = lang_P.forge_msg(lang, "lootbox", [nbgift], False, 6)

    elif (jour.month == 12 and jour.day >= 22) and (jour.month == 12 and jour.day <= 25):
        if nbgift > 0:
            sql.add(PlayerID, "lootbox_gift", nbgift, "inventory")
            sql.add(PlayerID, ["boxes", "lootbox | gift | gain"], nbgift, "statgems")
            desc = lang_P.forge_msg(lang, "lootbox", [nbgift], False, 3)

    elif (jour.month == 12 and jour.day >= 30) or (jour.month == 1 and jour.day <= 2):
        if nbgift > 0:
            sql.add(PlayerID, "lootbox_gift", nbgift, "inventory")
            sql.add(PlayerID, ["boxes", "lootbox | gift | gain"], nbgift, "statgems")
            desc = lang_P.forge_msg(lang, "lootbox", [nbgift], False, 4)

    return desc


def lootbox(PlayerID, lang, param = False):
    desc = ""

    D = r.randint(-40, 40)
    if D == 0:
        sql.add(PlayerID, "lootbox_legendarygems", 1, "inventory")
        sql.add(PlayerID, ["boxes", "lootbox | legendary gems | gain"], 1, "statgems")
        desc = lang_P.forge_msg(lang, "lootbox", ["{idmoji[gem_lootbox]}"], False, 2)
    elif (D == 10) or (D == -10):
        sql.add(PlayerID, "lootbox_raregems", 1, "inventory")
        sql.add(PlayerID, ["boxes", "lootbox |  rare gems | gain"], 1, "statgems")
        desc = lang_P.forge_msg(lang, "lootbox", ["{idmoji[gem_lootbox]}"], False, 1)
    elif (D >= 29 and D <= 31) or (D >= -31 and D <= -29):
        sql.add(PlayerID, "lootbox_commongems", 1, "inventory")
        sql.add(PlayerID, ["boxes", "lootbox | common gems | gain"], 1, "statgems")
        desc = lang_P.forge_msg(lang, "lootbox", ["{idmoji[gem_lootbox]}"], False, 0)
    elif param:
        desc = gift(PlayerID, lang, True)

    return desc


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


def durability(PlayerID, outil):
    # gestion de la durabilité d'un outil
    nb = int(sql.valueAtNumber(PlayerID, outil, "inventory"))
    if nb > 0:
        sql.add(PlayerID, outil, -1, "durability")
        if sql.valueAtNumber(PlayerID, outil, "durability") <= 0:
            for c in objetOutil:
                if c.nom == outil:
                    sql.add(PlayerID, outil, c.durabilite, "durability")
            sql.add(PlayerID, outil, -1, "inventory")
            return True
    return False


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

        res["couldown"] = couldown_4s
        res["couldownMsg"] = ":clock6:`6h`"
    elif item == "pumpkinH":
        res["nbitem"] = 1
        res["gain"] = "pumpkin"
        res["nbgain"] = r.randint(2, 5)
        res["couldown"] = couldown_4s
        res["couldownMsg"] = ":clock4:`4h`"

    # Items utilisé dans la production de la cave (ferment)
    elif item == "grapes":
        res["nbitem"] = 10
        res["gain"] = "wine_glass"
        res["nbgain"] = r.randint(1, 4)
        res["couldown"] = couldown_4s
        res["couldownMsg"] = ":clock3:`3h`"
    elif item == "wheat":
        res["nbitem"] = 8
        res["gain"] = "beer"
        res["nbgain"] = r.randint(2, 6)
        res["couldown"] = couldown_4s
        res["couldownMsg"] = ":clock8:`8h`"

    # Items utilisé dans la production de la cuisine (cooking)
    elif item == "potato":
        res["nbitem"] = 6
        res["gain"] = "fries"
        res["nbgain"] = r.randint(1, 5)
        res["couldown"] = couldown_4s
        res["couldownMsg"] = ":clock3:`3h`"
    elif item == "cacao":
        res["nbitem"] = 4
        res["gain"] = "chocolate"
        res["nbgain"] = r.randint(1, 5)
        res["couldown"] = couldown_4s
        res["couldownMsg"] = ":clock2:`2h`"
    elif item == "chocolate":
        res["nbitem"] = 8
        res["gain"] = "cupcake"
        res["nbgain"] = r.randint(1, 4)
        res["couldown"] = couldown_4h
        res["couldownMsg"] = ":clock4:`4h`"
    elif item == "pumpkin":
        res["nbitem"] = 12
        res["gain"] = "pumpkinpie"
        res["nbgain"] = r.randint(1, 4)
        res["couldown"] = couldown_2h
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
    # Traduit une valeur time en valeur HH:mm:ss
    # (avec un emoji correspondant devant)
    dtime = dict()
    dtime["timeH"] = int(time / 60 / 60)
    dtime["time"] = time - dtime["timeH"] * 3600
    dtime["timeM"] = int(time / 60)
    dtime["timeS"] = int(time - dtime["timeM"] * 60)
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
