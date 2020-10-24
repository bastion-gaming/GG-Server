from database import SQLite as sql
from languages import lang as lang_P
from core import level as lvl
from gems import gemsFonctions as GF, gemsItems as GI
import random as r


# ========== Success ==========
class Success:

    def __init__(self, id, sid, nom, titre, desc, type, objectif):
        self.id = id
        self.sid = sid
        self.nom = nom
        self.titre = titre
        self.desc = desc
        self.type = type
        self.objectif = objectif # nombre de gems minimum necessaire


objetSuccess = [
    # Daily
    Success(0, 1, "Daily", 0, 34, "gems|DailyMult", 2),
    Success(0, 2, "Daily", 0, 34, "gems|DailyMult", 5),
    Success(0, 3, "Daily", 0, 34, "gems|DailyMult", 8),
    Success(0, 4, "Daily", 0, 34, "gems|DailyMult", 15),
    Success(0, 5, "Daily", 0, 34, "gems|DailyMult", 30),
    Success(0, 6, "Daily", 0, 34, "gems|DailyMult", 45),
    Success(0, 7, "Daily", 0, 34, "gems|DailyMult", 60),
    Success(0, 8, "Daily", 0, 34, "gems|DailyMult", 90),
    Success(0, 9, "Daily", 0, 34, "gems|DailyMult", 120),
    Success(0, 10, "Daily", 0, 34, "gems|DailyMult", 150),
    Success(0, 11, "Daily", 0, 34, "gems|DailyMult", 200),
    Success(0, 12, "Daily", 0, 34, "gems|DailyMult", 300),
    Success(0, 13, "Daily", 0, 34, "gems|DailyMult", 400),
    Success(0, 14, "Daily", 0, 34, "gems|DailyMult", 500),
    Success(0, 15, "Daily", 0, 34, "gems|DailyMult", 600),
    Success(0, 16, "Daily", 0, 34, "gems|DailyMult", 800),
    Success(0, 17, "Daily", 0, 34, "gems|DailyMult", 1000),


    # Argent
    Success(1, 1, "Gems", 1, 0, "gems|Gems", 500),                  # 500
    Success(1, 2, "Gems", 1, 1, "gems|Gems", 1000),                 # 1k
    Success(1, 3, "Gems", 1, 2, "gems|Gems", 5000),                 # 5k
    Success(1, 4, "Gems", 1, 3, "gems|Gems", 50000),                # 50k
    Success(1, 5, "Gems", 1, 4, "gems|Gems", 200000),               # 200k
    Success(1, 6, "Gems", 1, 5, "gems|Gems", 500000),               # 500k
    Success(1, 7, "Gems", 1, 6, "gems|Gems", 1000000),              # 1M
    Success(1, 8, "Gems", 1, 7, "gems|Gems", 10000000),             # 10M
    Success(1, 9, "Gems", 1, 8, "gems|Gems", 100000000),            # 100M
    Success(1, 10, "Gems", 1, 9, "gems|Gems", 500000000),           # 500M
    Success(1, 11, "Gems", 1, 10, "gems|Gems", 1000000000),         # 1G
    Success(1, 12, "Gems", 1, 18, "gems|Gems", 5000000000),         # 5G
    Success(1, 13, "Gems", 1, 19, "gems|Gems", 20000000000),        # 20G
    Success(1, 14, "Gems", 1, 20, "gems|Gems", 50000000000),        # 50G
    Success(1, 15, "Gems", 1, 21, "gems|Gems", 200000000000),       # 200G
    Success(1, 16, "Gems", 1, 22, "gems|Gems", 500000000000),       # 500G
    Success(1, 17, "Gems", 1, 23, "gems|Gems", 1000000000000),      # 1T

    Success(2, 1, "Gamble", 2, 17, "gamble|max", 10),               # 10
    Success(2, 2, "Gamble", 2, 17, "gamble|max", 50),               # 50
    Success(2, 3, "Gamble", 2, 17, "gamble|max", 100),              # 100
    Success(2, 4, "Gamble", 2, 17, "gamble|max", 300),              # 300
    Success(2, 5, "Gamble", 2, 17, "gamble|max", 700),              # 700
    Success(2, 6, "Gamble", 2, 17, "gamble|max", 1000),             # 1k
    Success(2, 7, "Gamble", 2, 17, "gamble|max", 10000),            # 10k
    Success(2, 8, "Gamble", 2, 17, "gamble|max", 100000),           # 100k
    Success(2, 9, "Gamble", 2, 17, "gamble|max", 1000000),          # 1M
    Success(2, 10, "Gamble", 2, 17, "gamble|max", 10000000),         # 10M
    Success(2, 11, "Gamble", 2, 17, "gamble|max", 100000000),        # 100M
    Success(2, 12, "Gamble", 2, 17, "gamble|max", 1000000000),       # 1G
    Success(2, 13, "Gamble", 2, 17, "gamble|max", 10000000000),      # 10G
    Success(2, 14, "Gamble", 2, 17, "gamble|max", 100000000000),    # 100G
    Success(2, 15, "Gamble", 2, 17, "gamble|max", 1000000000000),   # 1T

    Success(3, 1, "Robin Hood", 3, 24, "stealing|gain", 1000),
    Success(3, 2, "Robin Hood", 3, 24, "stealing|gain", 15000),
    Success(3, 3, "Robin Hood", 3, 24, "stealing|gain", 42000),
    Success(3, 4, "Robin Hood", 3, 24, "stealing|gain", 100000),
    Success(3, 5, "Robin Hood", 3, 24, "stealing|gain", 300000),
    Success(3, 6, "Robin Hood", 3, 24, "stealing|gain", 600000),
    Success(3, 7, "Robin Hood", 3, 24, "stealing|gain", 1000000),
    Success(3, 8, "Robin Hood", 3, 24, "stealing|gain", 6000000),

    Success(21, 1, "Lobbyiste", 23, 30, "pay|don max", 100),
    Success(21, 2, "Lobbyiste", 23, 30, "pay|don max", 1000),
    Success(21, 3, "Lobbyiste", 23, 30, "pay|don max", 10000),
    Success(21, 4, "Lobbyiste", 23, 30, "pay|don max", 100000),
    Success(21, 5, "Lobbyiste", 23, 30, "pay|don max", 1000000),
    Success(21, 6, "Lobbyiste", 23, 30, "pay|don max", 10000000),

    Success(22, 1, "Politicien", 24, 31, "pay|recu max", 200),
    Success(22, 2, "Politicien", 24, 31, "pay|recu max", 2000),
    Success(22, 3, "Politicien", 24, 31, "pay|recu max", 20000),
    Success(22, 4, "Politicien", 24, 31, "pay|recu max", 200000),
    Success(22, 5, "Politicien", 24, 31, "pay|recu max", 2000000),
    Success(22, 6, "Politicien", 24, 31, "pay|recu max", 20000000),


    # Minage
    Success(4, 1, "Pickaxe", 4, 11, "broken|mine|pickaxe", 1),
    Success(4, 2, "Pickaxe", 4, 11, "broken|mine|pickaxe", 2),
    Success(4, 3, "Pickaxe", 4, 11, "broken|mine|pickaxe", 4),
    Success(4, 4, "Pickaxe", 4, 11, "broken|mine|pickaxe", 6),
    Success(4, 5, "Pickaxe", 4, 11, "broken|mine|pickaxe", 10),
    Success(4, 6, "Pickaxe", 4, 11, "broken|mine|pickaxe", 15),
    Success(4, 7, "Pickaxe", 4, 11, "broken|mine|pickaxe", 20),
    Success(4, 8, "Pickaxe", 4, 11, "broken|mine|pickaxe", 50),
    Success(4, 9, "Pickaxe", 4, 11, "broken|mine|pickaxe", 100),

    Success(5, 1, "Miner", 5, 12, "mine|cobblestone", 300),
    Success(5, 2, "Miner", 5, 12, "mine|cobblestone", 500),
    Success(5, 3, "Miner", 5, 12, "mine|iron", 200),
    Success(5, 4, "Miner", 5, 12, "mine|gold", 300),
    Success(5, 5, "Miner", 5, 12, "mine|iron", 550),
    Success(5, 6, "Miner", 5, 12, "mine|gold", 800),
    Success(5, 7, "Miner", 5, 12, "mine|iron", 2000),
    Success(5, 8, "Miner", 5, 12, "mine|gold", 3000),

    Success(6, 1, "Wonders Miner", 6, 12, "mine|diamond", 10),
    Success(6, 2, "Wonders Miner", 6, 12, "mine|diamond", 25),
    Success(6, 3, "Wonders Miner", 6, 12, "mine|diamond", 50),
    Success(6, 4, "Wonders Miner", 6, 12, "mine|emerald", 70),
    Success(6, 5, "Wonders Miner", 6, 12, "mine|diamond", 200),
    Success(6, 6, "Wonders Miner", 6, 12, "mine|ruby", 100),
    Success(6, 7, "Wonders Miner", 6, 12, "mine|emerald", 500),
    Success(6, 8, "Wonders Miner", 6, 12, "mine|diamond", 1000),
    Success(6, 9, "Wonders Miner", 6, 12, "mine|ruby", 1000),


    # Excavation
    Success(7, 1, "Shovel", 7, 11, "broken|dig|shovel", 1),
    Success(7, 2, "Shovel", 7, 11, "broken|dig|shovel", 2),
    Success(7, 3, "Shovel", 7, 11, "broken|dig|shovel", 4),
    Success(7, 4, "Shovel", 7, 11, "broken|dig|shovel", 6),
    Success(7, 5, "Shovel", 7, 11, "broken|dig|shovel", 10),
    Success(7, 6, "Shovel", 7, 11, "broken|dig|shovel", 15),
    Success(7, 7, "Shovel", 7, 11, "broken|dig|shovel", 20),
    Success(7, 8, "Shovel", 7, 11, "broken|dig|shovel", 50),
    Success(7, 9, "Shovel", 7, 11, "broken|dig|shovel", 100),

    Success(8, 1, "Digger", 8, 13, "dig|seed", 100),
    Success(8, 2, "Digger", 8, 13, "dig|cacao", 100),
    Success(8, 3, "Digger", 8, 13, "dig|potato", 600),
    Success(8, 4, "Digger", 8, 13, "dig|seed", 800),
    Success(8, 5, "Digger", 8, 13, "dig|potato", 2000),


    # Pêche
    Success(9, 1, "Fishingrod", 9, 11, "broken|fish|fishingrod", 1),
    Success(9, 2, "Fishingrod", 9, 11, "broken|fish|fishingrod", 2),
    Success(9, 3, "Fishingrod", 9, 11, "broken|fish|fishingrod", 4),
    Success(9, 4, "Fishingrod", 9, 11, "broken|fish|fishingrod", 6),
    Success(9, 5, "Fishingrod", 9, 11, "broken|fish|fishingrod", 10),
    Success(9, 6, "Fishingrod", 9, 11, "broken|fish|fishingrod", 15),
    Success(9, 7, "Fishingrod", 9, 11, "broken|fish|fishingrod", 20),
    Success(9, 8, "Fishingrod", 9, 11, "broken|fish|fishingrod", 50),
    Success(9, 9, "Fishingrod", 9, 11, "broken|fish|fishingrod", 100),

    Success(10, 1, "Fisher", 10, 14, "fish|fish", 200),
    Success(10, 2, "Fisher", 10, 14, "fish|fish", 500),
    Success(10, 3, "Fisher", 10, 14, "fish|tropicalfish", 150),
    Success(10, 4, "Fisher", 10, 14, "fish|blowfish", 300),
    Success(10, 5, "Fisher", 10, 14, "fish|octopus", 500),
    Success(10, 6, "Fisher", 10, 14, "fish|fish", 8000),


    # Marché
    Success(11, 1, "Buy", 11, 15, "buy|total", 20),
    Success(11, 2, "Buy", 11, 15, "buy|total", 60),
    Success(11, 3, "Buy", 11, 15, "buy|total", 180),
    Success(11, 4, "Buy", 11, 15, "buy|total", 400),
    Success(11, 5, "Buy", 11, 15, "buy|total", 1000),
    Success(11, 6, "Buy", 11, 15, "buy|total", 2500),
    Success(11, 7, "Buy", 11, 15, "buy|total", 4800),
    Success(11, 8, "Buy", 11, 15, "buy|total", 10000),
    Success(11, 9, "Buy", 11, 15, "buy|total", 22000),
    Success(11, 10, "Buy", 11, 15, "buy|total", 50000),

    Success(12, 1, "Sell", 12, 16, "sell|total", 50),
    Success(12, 2, "Sell", 12, 16, "sell|total", 500),
    Success(12, 3, "Sell", 12, 16, "sell|total", 2000),
    Success(12, 4, "Sell", 12, 16, "sell|total", 6000),
    Success(12, 5, "Sell", 12, 16, "sell|total", 13000),
    Success(12, 6, "Sell", 12, 16, "sell|total", 30000),
    Success(12, 7, "Sell", 12, 16, "sell|total", 55000),
    Success(12, 8, "Sell", 12, 16, "sell|total", 130000),
    Success(12, 9, "Sell", 12, 16, "sell|total", 400000),
    Success(12, 10, "Sell", 12, 16, "sell|total", 1000000),

    Success(23, 1, "Banquier", 29, 32, "buy|bank_upgrade", 1),
    Success(23, 2, "Banquier", 29, 32, "buy|bank_upgrade", 2),
    Success(23, 3, "Banquier", 29, 32, "buy|bank_upgrade", 5),
    Success(23, 4, "Banquier", 29, 32, "buy|bank_upgrade", 10),
    Success(23, 5, "Banquier", 29, 32, "buy|bank_upgrade", 15),
    Success(23, 6, "Banquier", 30, 32, "buy|bank_upgrade", 25),
    Success(23, 7, "Banquier", 31, 32, "buy|bank_upgrade", 40),
    Success(23, 8, "Banquier", 32, 32, "buy|bank_upgrade", 60),

    Success(24, 1, "Rentré des classes", 25, 32, "buy|backpack", 1),
    Success(24, 2, "Rentré des classes", 25, 32, "buy|backpack", 5),
    Success(24, 3, "Rentré des classes", 25, 32, "buy|backpack", 10),
    Success(24, 4, "Rentré des classes", 25, 32, "buy|hyperpack", 2),
    Success(24, 5, "Rentré des classes", 25, 32, "buy|hyperpack", 5),
    Success(24, 6, "Rentré des classes", 25, 32, "buy|hyperpack", 10),
    Success(24, 7, "Rentré des classes", 25, 32, "buy|hyperpack", 25),
    Success(24, 8, "Rentré des classes", 25, 32, "buy|hyperpack", 42),


    # Serre | Cave | Cuisine
    Success(13, 1, "Nature lover", 13, 27, "hothouse|plant|seed", 100),
    Success(13, 2, "Nature lover", 13, 27, "hothouse|plant|seed", 200),
    Success(13, 3, "Nature lover", 13, 27, "hothouse|plant|seed", 500),
    Success(13, 4, "Nature lover", 13, 27, "hothouse|plant|seed", 1500),
    Success(13, 5, "Nature lover", 13, 27, "hothouse|plant|seed", 5000),
    Success(13, 6, "Nature lover | Amazonian filler", 14, 27, "hothouse|plant|seed", 15000),
    Success(13, 7, "Nature lover | Amazonian filler", 14, 27, "hothouse|plant|seed", 50000),
    Success(13, 8, "Nature lover | Amazonian filler", 14, 27, "hothouse|plant|seed", 200000),

    Success(14, 1, "Woodcutter", 15, 25, "hothouse|harvest|oak", 100),
    Success(14, 2, "Woodcutter", 15, 25, "hothouse|harvest|spruce", 200),
    Success(14, 3, "Woodcutter", 15, 25, "hothouse|harvest|palm", 300),
    Success(14, 4, "Woodcutter", 15, 25, "hothouse|harvest|oak", 1000),
    Success(14, 5, "Woodcutter", 15, 25, "hothouse|harvest|spruce", 2000),
    Success(14, 6, "Woodcutter", 15, 25, "hothouse|harvest|palm", 3000),

    Success(15, 1, "Vineyard", 16, 25, "ferment|harvest|wine_glass", 100),
    Success(15, 2, "Vineyard", 16, 25, "ferment|harvest|wine_glass", 500),
    Success(15, 3, "Vineyard", 16, 25, "ferment|harvest|wine_glass", 1500),
    Success(15, 4, "Vineyard", 16, 25, "ferment|harvest|wine_glass", 4000),
    Success(15, 5, "Vineyard", 16, 25, "ferment|harvest|wine_glass", 12000),
    Success(15, 6, "Vineyard", 16, 25, "ferment|harvest|wine_glass", 50000),
    Success(15, 7, "Vineyard", 16, 25, "ferment|harvest|wine_glass", 100000),
    Success(15, 8, "Vineyard", 16, 25, "ferment|harvest|wine_glass", 300000),
    Success(15, 9, "Vineyard", 16, 25, "ferment|harvest|wine_glass", 800000),
    Success(15, 10, "Vineyard", 16, 25, "ferment|harvest|wine_glass", 2000000),
    Success(15, 11, "Vineyard", 16, 25, "ferment|harvest|wine_glass", 10000000),

    Success(16, 1, "Apero", 17, 25, "ferment|harvest|beer", 100),
    Success(16, 2, "Apero", 17, 25, "ferment|harvest|beer", 500),
    Success(16, 3, "Apero", 17, 25, "ferment|harvest|beer", 1500),
    Success(16, 4, "Apero", 17, 25, "ferment|harvest|beer", 4000),
    Success(16, 5, "Apero", 17, 25, "ferment|harvest|beer", 12000),
    Success(16, 6, "Apero", 17, 25, "ferment|harvest|beer", 50000),
    Success(16, 7, "Apero", 17, 25, "ferment|harvest|beer", 100000),
    Success(16, 8, "Apero", 17, 25, "ferment|harvest|beer", 300000),
    Success(16, 9, "Apero", 17, 25, "ferment|harvest|beer", 800000),
    Success(16, 10, "Apero", 17, 25, "ferment|harvest|beer", 2000000),
    Success(16, 11, "Apero", 17, 25, "ferment|harvest|beer", 10000000),

    Success(17, 1, "Reaper", 18, 25, "hothouse|harvest|wheat", 100),
    Success(17, 2, "Reaper", 18, 25, "hothouse|harvest|wheat", 500),
    Success(17, 3, "Reaper", 18, 25, "hothouse|harvest|wheat", 1500),
    Success(17, 4, "Reaper", 18, 25, "hothouse|harvest|wheat", 4000),
    Success(17, 5, "Reaper", 18, 25, "hothouse|harvest|wheat", 12000),
    Success(17, 6, "Reaper", 18, 25, "hothouse|harvest|wheat", 50000),
    Success(17, 7, "Reaper", 18, 25, "hothouse|harvest|wheat", 100000),
    Success(17, 8, "Reaper", 18, 25, "hothouse|harvest|wheat", 300000),
    Success(17, 9, "Reaper", 18, 25, "hothouse|harvest|wheat", 800000),
    Success(17, 10, "Reaper", 18, 25, "hothouse|harvest|wheat", 2000000),
    Success(17, 11, "Reaper", 18, 25, "hothouse|harvest|wheat", 5000000),
    Success(17, 12, "Reaper", 18, 25, "hothouse|harvest|wheat", 15000000),
    Success(17, 13, "Reaper", 18, 25, "hothouse|harvest|wheat", 40000000),
    Success(17, 14, "Reaper", 18, 25, "hothouse|harvest|wheat", 100000000),

    Success(18, 1, "My life is Potato", 19, 28, "cooking|plant|potato", 100),
    Success(18, 2, "My life is Potato", 19, 28, "cooking|plant|potato", 300),
    Success(18, 3, "My life is Potato", 19, 28, "cooking|plant|potato", 700),
    Success(18, 4, "My life is Potato", 19, 28, "cooking|plant|potato", 1200),
    Success(18, 5, "My life is Potato", 19, 28, "cooking|plant|potato", 3000),
    Success(18, 6, "My life is Potato", 19, 28, "cooking|plant|potato", 10000),
    Success(18, 7, "My life is Potato", 19, 28, "cooking|plant|potato", 30000),
    Success(18, 8, "My life is Potato", 19, 28, "cooking|plant|potato", 100000),

    Success(19, 1, "Barack à frite", 20, 26, "cooking|harvest|fries", 10),
    Success(19, 2, "Barack à frite", 20, 26, "cooking|harvest|fries", 20),
    Success(19, 3, "Barack à frite", 20, 26, "cooking|harvest|fries", 50),
    Success(19, 4, "Barack à frite", 20, 26, "cooking|harvest|fries", 100),
    Success(19, 5, "Barack à frite", 20, 26, "cooking|harvest|fries", 200),
    Success(19, 6, "Barack à frite", 20, 26, "cooking|harvest|fries", 500),
    Success(19, 7, "Barack à frite", 20, 26, "cooking|harvest|fries", 1500),
    Success(19, 8, "Barack à frite", 20, 26, "cooking|harvest|fries", 4000),
    Success(19, 9, "Barack à frite", 20, 26, "cooking|harvest|fries", 12000),


    # Forge
    Success(20, 1, "Germinal", 21, 29, "forge|iron_pickaxe", 1),
    Success(20, 2, "Germinal", 21, 29, "forge|iron_pickaxe", 5),
    Success(20, 3, "Germinal", 21, 29, "forge|iron_pickaxe", 10),
    Success(20, 4, "Germinal", 22, 29, "forge|diamond_pickaxe", 1),
    Success(20, 5, "Germinal", 22, 29, "forge|diamond_pickaxe", 5),
    Success(20, 6, "Germinal", 22, 29, "forge|diamond_pickaxe", 10),


    # Inventaire
    Success(25, 1, "#Tragédie", 28, 33, "inv|cookie", 10),
    Success(25, 2, "#Tragédie", 28, 33, "inv|cookie", 50),
    Success(25, 3, "#Tragédie", 28, 33, "inv|cookie", 100),
    Success(25, 4, "#Tragédie", 28, 33, "inv|cookie", 300),
    Success(25, 5, "#Tragédie", 28, 33, "inv|cookie", 500),
    Success(25, 6, "#Tragédie", 28, 33, "inv|cookie", 1000),
    Success(25, 7, "#Tragédie", 28, 33, "inv|cookie", 2000),
    Success(25, 8, "#Tragédie", 28, 33, "inv|cookie", 5000),
    Success(25, 9, "#Tragédie", 28, 33, "inv|cookie", 10000),
    Success(25, 10, "#Tragédie", 28, 33, "inv|cookie", 50000),
    Success(25, 11, "#Tragédie", 28, 33, "inv|cookie", 100000)
]


def checkSuccess(PlayerID, lang):
    result = []
    i = -1
    for x in objetSuccess:
        if x.id > i:
            i = x.id
    myStat = 0
    for i in range(0, i+1):
        iS = sql.value(PlayerID, 'success', 'Stock', 'idsuccess', i)
        if iS is not None:
            for x in objetSuccess:
                if x.id == i and x.sid == iS+1:
                    type = x.type.split("|")
                    nom = ""

                    if type[0] == "gems":
                        myStat = sql.value(PlayerID, "gems", "{0}".format(type[1]))
                        if myStat >= x.objectif:
                            nom = lang_P.forge_msg(lang, "success titre", [GF.ChiffreRomain(x.sid)], False, x.titre)

                    elif type[0] == "broken":
                        myStat = sql.value(PlayerID, "statgems", 'Stock', 'Nom', "{0} | broken | {1}".format(type[1], type[2]))
                        if myStat >= x.objectif:
                            nom = lang_P.forge_msg(lang, "success titre", [GF.ChiffreRomain(x.sid)], False, x.titre)

                    elif type[0] == "mine" or type[0] == "dig" or type[0] == "fish":
                        myStat = sql.value(PlayerID, "statgems", 'Stock', 'Nom', "{0} | item | {1}".format(type[0], type[1]))
                        if myStat >= x.objectif:
                            nom = lang_P.forge_msg(lang, "success titre", [GF.ChiffreRomain(x.sid)], False, x.titre)

                    elif type[0] == "buy" or type[0] == "sell" or type[0] == "gamble" or type[0] == "stealing":
                        if (type[0] == "buy" or type[0] == "sell") and type[1] != "total":
                            myStat = sql.value(PlayerID, "statgems", 'Stock', 'Nom', "{0} | item | {1}".format(type[0], type[1]))
                        else:
                            myStat = sql.value(PlayerID, "statgems", 'Stock', 'Nom', "{0} | {1}".format(type[0], type[1]))
                        if myStat >= x.objectif:
                            nom = lang_P.forge_msg(lang, "success titre", [GF.ChiffreRomain(x.sid)], False, x.titre)

                    elif type[0] == "hothouse" or type[0] == "ferment" or type[0] == "cooking":
                        myStat = sql.value(PlayerID, "statgems", 'Stock', 'Nom', "{0} | {1} | item | {2}".format(type[0], type[1], type[2]))
                        if myStat >= x.objectif:
                            nom = lang_P.forge_msg(lang, "success titre", [GF.ChiffreRomain(x.sid)], False, x.titre)

                    elif type[0] == "forge":
                        myStat = sql.value(PlayerID, "statgems", 'Stock', 'Nom', "forge | item | {0}".format(type[1]))
                        if myStat >= x.objectif:
                            nom = lang_P.forge_msg(lang, "success titre", [GF.ChiffreRomain(x.sid)], False, x.titre)

                    elif type[0] == "pay":
                        myStat = sql.value(PlayerID, "statgems", 'Stock', 'Nom', "pay | {0}".format(type[1]))
                        if myStat >= x.objectif:
                            nom = lang_P.forge_msg(lang, "success titre", [GF.ChiffreRomain(x.sid)], False, x.titre)

                    elif type[0] == "inv":
                        myStat = sql.value(PlayerID, "statgems", 'Stock', 'Nom', "{0}".format(type[1]))
                        if myStat >= x.objectif:
                            nom = lang_P.forge_msg(lang, "success titre", [GF.ChiffreRomain(x.sid)], False, x.titre)

    #                 elif type[0] == "":
    #                     myStat = sql.value(PlayerID, "statgems", 'Stock', 'Nom', "")
    #                     if myStat >= x.objectif:
    #                         nom = lang_P.forge_msg(lang, "success titre", [GF.ChiffreRomain(x.sid)], False, x.titre)

                    if nom != "":
                        GF.addSuccess(PlayerID, i, 1)
                        result.append(nom)
                        desc = "{0}".format(lang_P.forge_msg(lang, "success", [nom], False, 0))
                        result.append(desc)
                        if iS == 0:
                            iS = 1
                        gain = r.randint(1, 3)*(6*(iS))
                        lvl.addxp(PlayerID, gain)
                        desc = "{0} XP".format(lang_P.forge_msg(lang, "success", [gain], False, 1))
                        result.append(desc)
                        return result
    return result


# Commandes
def stats(param):
    nom = param["nom"]
    if nom != "None":
        nom = sql.nom_ID(nom)
        ID = sql.get_PlayerID(nom, param["name_pl"])
    else:
        ID = sql.get_PlayerID(param["ID"], param["name_pl"])
    lang = param["lang"]
    if ID['error'] == 404:
        msg = ["WarningMsg", lang_P.forge_msg(lang, "WarningMsg", None, False, 0)]
        return {'error': 404, 'etat': 'Warning'}
    PlayerID = ID['ID']
    desc = []
    stat = sql.valueAll(PlayerID, 'statgems', ['Nom', 'Type', 'Stock'])
    if stat is not False or stat != []:
        for x in stat:
            desc.append(str(x))
        msg = {'error': 0, 'etat': 'OK', 'lang': lang, 'stats': desc}
    else:
        msg = {'error': 1, 'etat': 'NOK', 'lang': lang, 'stats': False}
    return msg


def success(param):
    lang = param["lang"]
    PlayerID = param["PlayerID"]
    msg = {}
    msg["lang"] = lang
    result = []
    dict = {}
    i = -1
    for x in objetSuccess:
        if x.id > i:
            i = x.id
        dict[x.id] = x.sid
    for i in range(0, i+1):
        iS = sql.value(PlayerID, 'success', 'Stock', 'idsuccess', i)
        for x in objetSuccess:
            arg = None
            if x.id == i:
                type = x.type.split("|")
                if type[0] == "gems" or type[0] == "daily":
                    myStat = sql.value(PlayerID, "gems", "{0}".format(type[1]))
                    if type[0] == "gems":
                        arg = None
                    else:
                        arg = [x.objectif]

                elif type[0] == "broken":
                    myStat = sql.value(PlayerID, "statgems", 'Stock, Type, Nom', 'Nom', "{0} | broken | {1}".format(type[1], type[2]))
                    arg = [x.objectif, type[2], "{idmoji[gem_" + type[2] + "]}"]

                elif type[0] == "mine" or type[0] == "dig" or type[0] == "fish":
                    myStat = sql.value(PlayerID, "statgems", 'Stock, Type, Nom', 'Nom', "{0} | item | {1}".format(type[0], type[1]))
                    arg = [x.objectif, type[1], "{idmoji[gem_" + type[1] + "]}"]

                elif type[0] == "buy" or type[0] == "sell":
                    if (type[0] == "buy" or type[0] == "sell") and type[1] != "total":
                        myStat = sql.value(PlayerID, "statgems", 'Stock, Type, Nom', 'Nom', "{0} | item | {1}".format(type[0], type[1]))
                        arg = [x.objectif, type[1], "{idmoji[gem_" + type[1] + "]}"]
                    else:
                        myStat = sql.value(PlayerID, "statgems", 'Stock, Type, Nom', 'Nom', "{0} | {1}".format(type[0], type[1]))
                        arg = [x.objectif]

                elif type[0] == "gamble" or type[0] == "stealing" or type[0] == "slots":
                    myStat = sql.value(PlayerID, "statgems", 'Stock, Type, Nom', 'Nom', "{0} | {1}".format(type[0], type[1]))
                    arg = [x.objectif]

                elif type[0] == "pay":
                    myStat = sql.value(PlayerID, "statgems", 'Stock, Type, Nom', 'Nom', "pay | {0}".format(type[1]))
                    arg = [x.objectif]

                elif type[0] == "forge":
                    myStat = sql.value(PlayerID, "statgems", 'Stock, Type, Nom', 'Nom', "forge | item | {0}".format(type[1]))
                    arg = [x.objectif, type[1], "{idmoji[gem_" + type[1] + "]}"]

                elif type[0] == "hothouse" or type[0] == "ferment" or type[0] == "cooking":
                    myStat = sql.value(PlayerID, "statgems", 'Stock, Type, Nom', 'Nom', "{0} | {1} | item | {2}".format(type[0], type[1], type[2]))
                    if type[2] in GI.objetEmoji:
                        idmoji = ":{0}:".format(type[2])
                    else:
                        idmoji = "<:gem_{0}:{1}>".format(type[2], "{idmoji[gem_" + type[2] + "]}")
                    arg = [x.objectif, type[2], idmoji]

                elif type[0] == "inv":
                    myStat = sql.value(PlayerID, "statgems", 'Stock, Type, Nom', 'Nom', "{0}".format(type[1]))
                    if type[1] in GI.objetEmoji:
                        idmoji = ":{0}:".format(type[1])
                    else:
                        idmoji = "<:gem_{0}:{1}>".format(type[1], "{idmoji[gem_" + type[1] + "]}")
                    arg = [x.objectif, type[1], idmoji]

                if x.sid == iS+1:
                    result.append(lang_P.forge_msg(lang, "success titre", [GF.ChiffreRomain(x.sid)], False, x.titre))
                    desc = "{0} | `{1}`/`{2}`".format(lang_P.forge_msg(lang, "success desc", arg, False, x.desc), myStat, x.objectif)
                    result.append(desc)
                elif iS == dict[i] and x.sid == iS:
                    desc = "{0} | **_{1}_**".format(lang_P.forge_msg(lang, "success desc", arg, False, x.desc), lang_P.forge_msg(lang, "success", None, False, 2))
                    result.append(lang_P.forge_msg(lang, "success titre", [GF.ChiffreRomain(x.sid)], False, x.titre))
                    result.append(desc)
    msg["type"] = "OK"
    msg["error"] = 0
    msg["result"] = result
    return msg
