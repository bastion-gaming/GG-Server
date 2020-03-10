import json
from DB import SQLite as sql
from gems import gemsItems as GI, gemsFonctions as GF


def load_dates():
    """
    Charge les dates des saisons et leur nombre total

    Return :
    dict => 5 clefs avec pour les 4 premières les int 1, 2, 3 et 4 qui donnes
        les 4 dates puis une clef string total qui donne le total de saison écoulé.
    """
    path = "core/saisons.json"
    res = dict()
    with open(path, encoding='utf-8') as json_file:
        data = json.load(json_file)
        for i in data:
            if i != "total":
                res[int(i)] = data[i]
            else:
                res[i] = data[i]
    return res


def end_season():
    res = load_dates()
    nbs = res["total"]
    for i in range(1, sql.taille("gems")+1):
        IDd = sql.userID(i, "gems")
        SuperID = sql.get_SuperID(IDd, "discord")
        PlayerID = sql.get_PlayerID(SuperID)
        solde = sql.valueAtNumber(PlayerID, "gems", "gems")
        bank = sql.valueAtNumber(PlayerID, "Solde", "bank")
        if solde != 0:
            sql.add(PlayerID, "idseasons", nbs, "seasons")
            sql.updateField(PlayerID, "gem", [solde, nbs], "seasons")
            sql.updateField(PlayerID, "bank", [bank, nbs], "seasons")
            sql.updateField(PlayerID, "gems", 0, "gems")
            sql.updateField(PlayerID, "Solde", 0, "bank")
            for x in GI.exception:
                if x != "bank_upgrade":
                    sql.updateField(PlayerID, x, 0, "inventory")
            for x in GF.ObjetEventEnd:
                if x != "bank_upgrade":
                    sql.updateField(PlayerID, x, 0, "inventory")
    return True
