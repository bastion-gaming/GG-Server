import random as r
import time as t
import datetime as dt
from DB import TinyDB as DB, SQLite as sql
import json
from gems import gemsItems as GI, gemsStats as GS
from operator import itemgetter

idBaBot = 604776153458278415
idGetGems = 620558080551157770

WarningMsg = ["Error", "Aucun compte utilisateur n'a été trouvé"]

def checkDB_Guilde():
    if DB.dbExist("DB/guildesDB"):
        print("Guildes >> La DB existe, poursuite sans soucis.")
    else :
        print("Guildes >> La DB n'existait pas. Elle a été (re)créée.")
    flag = DB.checkField("DB/guildesDB", "DB/Templates/guildesTemplate")
    if flag == 0:
        print("DB >> Aucun champ n'a été ajouté, supprimé ou modifié.")
    elif "add" in flag:
        print("DB >> Un ou plusieurs champs ont été ajoutés à la DB.")
    elif "type" in flag:
        print("DB >> Un ou plusieurs type ont été modifié sur la DB.")
    elif "sup" in flag:
        print("DB >> Un ou plusieurs champs ont été supprimés de la DB.")

# Array
message_crime = ["Vous avez volé la Société Eltamar et vous êtes retrouvé dans un lac, mais vous avez quand même réussi à voler" #You robbed the Society of Schmoogaloo and ended up in a lake,but still managed to steal
,"Tu as volé une pomme qui vaut"
,"Tu as volé une carotte ! Prend tes"
, "Tu voles un bonbon ! Prend tes"
, "Tu as gangé au loto ! Prends tes"
, "J'ai plus d'idée prends ça:"]

message_gamble = ["Tu as remporté le pari ! Tu obtiens"
,"Une grande victoire pour toi ! Tu gagnes"
,"Bravo prends"
, "Heu...."
,"Pourquoi jouer à Fortnite quand tu peux gamble! Prends tes"]

# se sont les phrases prononcé par le bot pour plus de diversité

# Taille max de l'Inventaire
invMax = 15000


def itemBourse(item, type):
    """Version 2.3 | Attribue les prix de la bourse """
    # récupération du fichier de sauvegarde de la bourse
    with open('gems/bourse.json', 'r') as fp:
        dict = json.load(fp)
    temp = dict[item]
    # Récuperation de la valeur courante
    if type == "vente":
        pnow = temp["vente"]
    elif type == "achat":
        pnow = temp["achat"]

    #Verification pour l'actualisation de la bourse
    if sql.spam(idBaBot, couldown_12h, "bourse", "gems"):
        # Gestion des exceptions
        if item in GI.exception:
            return pnow

        #Calcul du prix mini
        for c in GI.PrixItem:
            if c.nom == item:
                if type == "vente":
                    pmini = c.vente - (c.vente*(85/100))
                elif type == "achat":
                    pmini = c.achat - (c.achat*(85/100))
        for c in GI.PrixOutil:
            if c.nom == item:
                if type == "vente":
                    pmini = c.vente - (c.vente*(85/100))
                elif type == "achat":
                    pmini = c.achat - (c.achat*(85/100))
        pmini = int(pmini)
        # print("{} {} >> {}".format(type, item, pmini))

        # Fonctionnement de la bourse
        DcrackB = r.randint(1, 1000)
        # crack boursier négatif
        if DcrackB <= 5:
            Prix = pnow - (pnow*(50//100))
        # crack boursier positif
        elif DcrackB >= 995:
            Prix = pnow + (pnow*(50//100))
        # évolution de la bourse normale (entre -10% et +10% de la valeur courante)
        else:
            D21 = r.randint(0,20)
            # valeur minimal dynamique (permet au item dont le prix est au plus bas de remonter en valeur plus facilement)
            if (pnow < 30 and type == "vente") or (pnow < 50 and type == "achat"):
                if D21 >= 5:
                    pourcentage = D21 + 5
                    Prix = pnow + ((pnow*pourcentage)//100)
                elif D21 < 5:
                    pourcentage = -1*(D21 + 5)
                    Prix = pnow + ((pnow*pourcentage)//100)
            else:
                if D21 > 10:
                    pourcentage = D21 - 10
                    Prix = pnow + ((pnow*pourcentage)//100)
                elif D21 < 10:
                    pourcentage = -1*(D21 + 1)
                    Prix = pnow + ((pnow*pourcentage)//100)
                else:
                    Prix = pnow
                if Prix < pmini:
                    Prix = pmini
                elif Prix <= 10:
                    Prix = 10
        #objet evenementiels
        zE = False
        for z in ObjetEventEnd:
            if z == item:
                zE = True
                if type == "vente":
                    temp["vente"] = get_default_price(item, type)
                    temp["precVente"] = get_default_price(item, type)
                elif type == "achat":
                    temp["achat"] = get_default_price(item, type)
                    temp["precAchat"] = get_default_price(item, type)
        # La valeur de vente ne peux etre supérieur à la valeur d'achat
        if not zE:
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


#Fonction d'actualisation/initialisation des items
def loadItem(F = None):
    jour = dt.date.today()
    if F == True:
        GI.initBourse()
    global ObjetEventEnd
    ObjetEventEnd = []
    #========== Items ==========
    class Item:

        def __init__(self,nom,vente,achat,poids,type):
            self.nom = nom
            self.vente = vente
            self.achat = achat
            self.poids = poids
            self.type = type

    global objetItem
    objetItem = [Item("backpack", itemBourse("backpack", "vente"), itemBourse("backpack", "achat"), -200, "special")
    ,Item("hyperpack", itemBourse("hyperpack", "vente"), itemBourse("hyperpack", "achat"), -20000, "spinelle")
    ,Item("fishhook", itemBourse("fishhook", "vente"), itemBourse("fishhook", "achat"), 1, "special")
    ,Item("cobblestone", itemBourse("cobblestone", "vente"), itemBourse("cobblestone", "achat"), 4, "minerai")
    ,Item("iron", itemBourse("iron", "vente"), itemBourse("iron", "achat"), 10, "minerai")
    ,Item("gold", itemBourse("gold", "vente"), itemBourse("gold", "achat"), 20, "minerai")
    ,Item("diamond", itemBourse("diamond", "vente"), itemBourse("diamond", "achat"), 40, "minerai")
    ,Item("emerald", itemBourse("emerald", "vente"), itemBourse("emerald", "achat"), 50, "minerai")
    ,Item("ruby", itemBourse("ruby", "vente"), itemBourse("ruby", "achat"), 70, "minerai")
    ,Item("fish", itemBourse("fish", "vente"), itemBourse("fish", "achat"), 2, "poisson")
    ,Item("tropicalfish", itemBourse("tropicalfish", "vente"), itemBourse("tropicalfish", "achat"), 8, "poisson")
    ,Item("blowfish", itemBourse("blowfish", "vente"), itemBourse("blowfish", "achat"), 8, "poisson")
    ,Item("octopus", itemBourse("octopus", "vente"), itemBourse("octopus", "achat"), 16, "poisson")
    ,Item("seed", itemBourse("seed", "vente"), itemBourse("seed", "achat"), 0.5, "plante")
    ,Item("oak", itemBourse("oak", "vente"), itemBourse("oak", "achat"), 50, "plante")
    ,Item("spruce", itemBourse("spruce", "vente"), itemBourse("spruce", "achat"), 70, "plante")
    ,Item("palm", itemBourse("palm", "vente"), itemBourse("palm", "achat"), 60, "plante")
    ,Item("wheat", itemBourse("wheat", "vente"), itemBourse("wheat", "achat"), 3, "plante")
    ,Item("cookie", itemBourse("cookie", "vente"), itemBourse("cookie", "achat"), 1, "emoji")
    ,Item("grapes", itemBourse("grapes", "vente"), itemBourse("grapes", "achat"), 1, "emoji")
    ,Item("wine_glass", itemBourse("wine_glass", "vente"), itemBourse("wine_glass", "achat"), 2, "emoji")
    ,Item("beer", itemBourse("beer", "vente"), itemBourse("beer", "achat"), 2, "emoji")
    ,Item("chocolate", itemBourse("chocolate", "vente"), itemBourse("chocolate", "achat"), 2, "consommable")
    ,Item("cacao", itemBourse("cacao", "vente"), itemBourse("cacao", "achat"), 1, "plante")
    ,Item("potato", itemBourse("potato", "vente"), itemBourse("potato", "achat"), 0.5, "consommable")
    ,Item("candy", itemBourse("candy", "vente"), itemBourse("candy", "achat"), 1, "emoji")
    ,Item("lollipop", itemBourse("lollipop", "vente"), itemBourse("lollipop", "achat"), 2, "emoji")]

    if not (jour.month == 10 and jour.day >= 22) or (jour.month == 11 and jour.day <= 10):
        for one in GI.ObjetHalloween:
            ObjetEventEnd.append(one)
    if not (jour.month == 12 and jour.day >= 13) or (jour.month == 1 and jour.day <= 5):
        for one in GI.ObjetChristmas:
            ObjetEventEnd.append(one)

    objetItem += [Item("pumpkin", itemBourse("pumpkin", "vente"), itemBourse("pumpkin", "achat"), 5, "halloween")
    ,Item("pumpkinpie", itemBourse("pumpkinpie", "vente"), itemBourse("pumpkinpie", "achat"), 5, "halloween")]

    objetItem += [Item("cupcake", itemBourse("cupcake", "vente"), itemBourse("cupcake", "achat"), 4, "christmas")]

    #========== Outils ==========
    class Outil:

        def __init__(self,nom,vente,achat,poids,durabilite,type):
            self.nom = nom
            self.vente = vente
            self.achat = achat
            self.poids = poids
            self.durabilite = durabilite
            self.type = type

    global objetOutil
    objetOutil = [Outil("pickaxe", itemBourse("pickaxe", "vente"), itemBourse("pickaxe", "achat"), 15, 75, "")
    ,Outil("iron_pickaxe", itemBourse("iron_pickaxe", "vente"), itemBourse("iron_pickaxe", "achat"), 70, 200, "forge")
    ,Outil("diamond_pickaxe", itemBourse("diamond_pickaxe", "vente"), itemBourse("diamond_pickaxe", "achat"), 150, 450, "forge")
    ,Outil("shovel", itemBourse("shovel", "vente"), itemBourse("shovel", "achat"), 10, 35, "")
    ,Outil("iron_shovel", itemBourse("iron_shovel", "vente"), itemBourse("iron_shovel", "achat"), 60, 100, "forge")
    ,Outil("diamond_shovel", itemBourse("diamond_shovel", "vente"), itemBourse("diamond_shovel", "achat"), 120, 240, "forge")
    ,Outil("fishingrod", itemBourse("fishingrod", "vente"), itemBourse("fishingrod", "achat"), 25, 100, "")
    ,Outil("sword", itemBourse("sword", "vente"), itemBourse("sword", "achat"), 55, 50, "forge")
    ,Outil("planting_plan", itemBourse("planting_plan", "vente"), itemBourse("planting_plan", "achat"), 4, 4, "consommable")
    ,Outil("barrel", itemBourse("barrel", "vente"), itemBourse("barrel", "achat"), 3, 3, "consommable")
    ,Outil("furnace", itemBourse("furnace", "vente"), itemBourse("furnace", "achat"), 2, 2, "consommable")
    ,Outil("bank_upgrade", itemBourse("bank_upgrade", "vente"), itemBourse("bank_upgrade", "achat"), 10000, None, "bank")]


    #========== Trophées ==========
    class Trophy:

        def __init__(self,nom,desc,type,mingem):
            self.nom = nom
            self.desc = desc
            self.type = type
            self.mingem = mingem #nombre de gems minimum necessaire

    global objetTrophy
    objetTrophy = [Trophy("Gamble Jackpot", "`Gagner plus de 10000`:gem:`gems au gamble`", "special", 10000)
    ,Trophy("Super Gamble Jackpot", "`Gagner plus de 100000`:gem:`gems au gamble`", "special", 100000)
    ,Trophy("Hyper Gamble Jackpot", "`Gagner plus de 1000000`:gem:`gems au gamble`", "special", 1000000)
    ,Trophy("Super Jackpot :seven::seven::seven:", "`Gagner le super jackpot sur la machine à sous`", "special", 0)
    ,Trophy("Mineur de Merveilles", "`Trouvez un `<:gem_ruby:{}>`ruby`".format(get_idmoji("ruby")), "special", 0)
    ,Trophy("La Squelatitude", "`Avoir 2`:beer:` sur la machine à sous`", "special", 0)
    ,Trophy("Gems 500", "`Avoir 500`:gem:`gems`", "unique", 500)
    ,Trophy("Gems 1k", "`Avoir 1k`:gem:`gems`", "unique", 1000)
    ,Trophy("Gems 5k", "`Avoir 5k`:gem:`gems`", "unique", 5000)
    ,Trophy("Gems 50k", "`Avoir 50k`:gem:`gems`", "unique", 50000)
    ,Trophy("Gems 200k", "`Avoir 200k`:gem:`gems`", "unique", 200000)
    ,Trophy("Gems 500k", "`Avoir 500k`:gem:`gems`", "unique", 500000)
    ,Trophy("Gems 1M", "`Avoir 1 Million`:gem:`gems`", "unique", 1000000)
    ,Trophy("Gems 10M", "`Avoir 10 Millions`:gem:`gems`", "unique", 10000000)
    ,Trophy("Gems 100M", "`Avoir 100 Millions`:gem:`gems`", "unique", 100000000)
    ,Trophy("Gems 500M", "`Avoir 500 Millions`:gem:`gems`", "unique", 500000000)
    ,Trophy("Le Milliard !!!", "`Avoir 1 Milliard`:gem:`gems`", "unique", 1000000000)]


    #========== Statistiques affiché dans info ==========
    class StatGems:

        def __init__(self,nom,desc):
            self.nom = nom
            self.desc = desc

    global objetStat
    objetStat = [StatGems("DiscordCop Arrestation", "`Nombre d'arrestation par la DiscordCop`")
    ,StatGems("DiscordCop Amende", "`Nombre d'ammende recue par la DiscordCop`")
    ,StatGems("Gamble Win", "`Nombre de gamble gagné`")
    ,StatGems("Super Jackpot :seven::seven::seven:", "`Nombre de super jackpot gagné sur la machine à sous`")
    ,StatGems("Mineur de Merveilles", "`Nombre de `<:gem_ruby:{}>`ruby` trouvé".format(get_idmoji("ruby")))
    ,StatGems("La Squelatitude", "`Avoir 2`:beer:` sur la machine à sous`")]


    #========== Loot Box ==========
    class Box:

        def __init__(self,nom, titre, achat , min, max, type):
            self.nom = nom
            self.titre = titre
            self.achat = achat
            self.min = min
            self.max = max
            self.type = type

    global objetBox
    objetBox = [Box("commongems", "Gems Common", 300, 100, 500, "gems")
    ,Box("raregems", "Gems Rare", 3000, 1000, 5000, "gems")
    ,Box("legendarygems", "Gems Legendary", 30000, 10000, 50000, "gems")
    ,Box("gift", "Items en folie", 2, 1000, 1000000, "spinelle")
    ,Box("gift_heart", "Cadeau de la Saint Valentin", 0, 100000, 500000, "")]


    if sql.spam(idBaBot, couldown_12h, "bourse", "gems"):
        sql.updateComTime(idBaBot, "bourse", "gems")
        for x in objetItem:
            GS.csv_add(x.nom)
        for x in objetOutil:
            GS.csv_add(x.nom)
# <<< def loadItem(F = None):

##############################################
#========== Recettes ==========
class Recette:

    def __init__(self,nom,type, nb1,item1, nb2,item2, nb3,item3, nb4,item4):
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

objetRecette = [Recette("iron_pickaxe", "forge", 10, "iron", 1, "pickaxe", 0, "", 0, "")
,Recette("diamond_pickaxe", "forge", 25, "diamond", 1, "iron_pickaxe", 0, "", 0, "")
,Recette("iron_shovel", "forge", 4, "iron", 1, "shovel", 0, "", 0, "")
,Recette("diamond_shovel", "forge", 10, "diamond", 1, "iron_shovel", 0, "", 0, "")
,Recette("sword", "forge", 6, "iron", 1, "oak", 0, "", 0, "")]




#========== Couldown pour la fonction antispam ==========
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


# def recette(ctx):
#     """Liste de toutes les recettes disponibles !"""
#     d_recette="Permet de voir la liste de toutes les recettes disponible !\n\n"
#     d_recette+="▬▬▬▬▬▬▬▬▬▬▬▬▬\n**Forge**\n"
#     for c in objetOutil:
#         for r in objetRecette :
#             if c.type == "forge":
#                 if c.nom == r.nom:
#                     d_recette += "<:gem_{0}:{1}>`{0}`: ".format(c.nom,get_idmoji(c.nom))
#                     if r.nb1 > 0:
#                         d_recette += "{0} <:gem_{1}:{2}>`{1}` ".format(r.nb1, r.item1, get_idmoji(r.item1))
#                     if r.nb2 > 0:
#                         d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb2, r.item2, get_idmoji(r.item2))
#                     if r.nb3 > 0:
#                         d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb3, r.item3, get_idmoji(r.item3))
#                     if r.nb4 > 0:
#                         d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb4, r.item4, get_idmoji(r.item4))
#                     d_recette += "\n"
#
#     msg = discord.Embed(title = "Recettes",color= 15778560, description = d_recette)
#     return msg


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


def get_default_price(nameElem, type = None):
    """Permet de connaitre le prix par defaut de l'item"""
    jour = dt.date.today()
    if type == None or type == "vente":
        for c in GI.PrixItem:
            if c.nom == nameElem:
                return c.vente

        for c in GI.PrixOutil:
            if c.nom == nameElem:
                return c.vente
    elif type == "achat":
        for c in GI.PrixItem:
            if c.nom == nameElem:
                for one in GI.ObjetHalloween:
                    if one == nameElem:
                        if (jour.month == 10 and jour.day >= 21) or (jour.month == 11 and jour.day <= 10):
                            return c.achat
                        else:
                            return 0
                for one in GI.ObjetChristmas:
                    if one == nameElem:
                        if (jour.month == 12 and jour.day >= 12) or (jour.month == 1 and jour.day <= 5):
                            return c.achat
                        else:
                            return 0
                return c.achat

        for c in GI.PrixOutil:
            if c.nom == nameElem:
                return c.achat
    return 0



def testInvTaille(ID):
    """Verifie si l'inventaire est plein """
    inv = sql.valueAt(ID, "all", "inventory")
    tailletot = 0
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



def testTrophy(ID, nameElem):
    """
    Permet de modifier le nombre de nameElem pour ID dans les trophées
    Pour en retirer mettez nbElemn en négatif
    """
    trophy = sql.valueAt(ID, "all", "trophy")
    gems = sql.valueAtNumber(ID, "gems", "gems")
    i = 2
    for c in objetTrophy:
        nbGemsNecessaire = c.mingem
        if c.type == "unique":
            if nameElem == c.nom:
                for x in trophy:
                    if nameElem == x[1]:
                        if sql.valueAtNumber(ID, c.nom, "trophy") > 1:
                            sql.updateField(ID, c.nom, 1, "trophy")
                        return 0
                if int(gems) >= nbGemsNecessaire:
                    if sql.valueAtNumber(ID, c.nom, "trophy") < 1:
                        sql.add(ID, c.nom, 1, "trophy")
                    elif sql.valueAtNumber(ID, c.nom, "trophy") > 1:
                        sql.updateField(ID, c.nom, 1, "trophy")
                    return 1



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
