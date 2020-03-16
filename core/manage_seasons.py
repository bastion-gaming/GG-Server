import json
from DB import SQLite as sql
from gems import gemsItems as GI, gemsFonctions as GF
from datetime import date, datetime
from apscheduler.schedulers.background import BackgroundScheduler


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


def parse_dates():
    dict_Dates = load_dates()
    Dyear = dict()
    Dmonth = dict()
    Dday = dict()

    for i in range(1, 5):
        Dyear[i] = int(dict_Dates[i][6:10])
        Dmonth[i] = int(dict_Dates[i][3:5])
        Dday[i] = int(dict_Dates[i][:2])

    return Dday, Dmonth, Dyear, dict_Dates


def new_season(idS):
    # 3 temps
    # fermer la précédente saisons
    # lancer la nouvelle saison
    # lancer la saison dans 1 an
    Dday, Dmonth, Dyear, dict_Dates = parse_dates()
    idS_old = 0

    if idS == 1:
        idS_old = 4
    else:
        idS_old = idS - 1

    print("Nouvelle saison en cours de lancement...")
    if end_season():

        # Ecriture de la nouvelle année dans le fichier
        dict_Dates[idS_old] = dict_Dates[idS_old][:6] + str(Dyear[idS_old]+1)
        path = "core/saisons.json"
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(dict_Dates, json_file, indent=4)

        # Reprogrammation de la nouvelle date
        scheduler = BackgroundScheduler()
        scheduler.reschedule_job('S'+str(idS_old), trigger='date', run_date=date(dict_Dates[idS_old], Dmonth[idS_old], Dday[idS_old]))

    else:
        print("\n\n\n ...Impossible de mettre fin à la précédente saison.")


def init_season():

    Dday, Dmonth, Dyear, dict_Dates = parse_dates()

    scheduler = BackgroundScheduler()
    # scheduler.add_job(new_season, 'date', run_date=date(Dyear[1], Dmonth[1], Dday[1]), args=[1], id="S1")
    # scheduler.add_job(new_season, 'date', run_date=date(Dyear[2], Dmonth[2], Dday[2]), args=[2], id="S2")
    # scheduler.add_job(new_season, 'date', run_date=date(Dyear[3], Dmonth[3], Dday[3]), args=[3], id="S3")
    # scheduler.add_job(new_season, 'date', run_date=date(Dyear[4], Dmonth[4], Dday[4]), args=[4], id="S4")
    scheduler.add_job(new_season, 'date', run_date=datetime(Dyear[1], Dmonth[1], Dday[1], 2, 12, 5), args=[1], id="S1")
    scheduler.add_job(new_season, 'date', run_date=datetime(Dyear[2], Dmonth[2], Dday[2], 2, 13, 5), args=[2], id="S2")
    scheduler.add_job(new_season, 'date', run_date=datetime(Dyear[3], Dmonth[3], Dday[3], 2, 14, 5), args=[3], id="S3")
    scheduler.add_job(new_season, 'date', run_date=datetime(Dyear[4], Dmonth[4], Dday[4], 2, 15, 5), args=[4], id="S4")

    scheduler.start()

    scheduler.print_jobs()


def end_season():
    """
    recupere le nombre de gems et le nombre de gems dans la banque,
    stock ces valeurs dans la base de donnée (table seasons) et met
    ces 2 valeurs a 0 + supprime tous les items a prix fixe dans l'inventaire
    """
    res = load_dates()
    nbs = res["total"]
    for i in range(1, sql.taille("gems")+1):
        # Récupération des données par Joueur
        IDs = sql.userID(i, "gems")
        IDd = IDs[1]
        IDm = IDs[2]
        if IDd is not None:
            SuperID = sql.get_SuperID(IDd, "discord")
        elif IDm is not None:
            SuperID = sql.get_SuperID(IDd, "messenger")
        else:
            SuperID = 0
        PlayerID = sql.get_PlayerID(SuperID)
        solde = sql.valueAtNumber(PlayerID, "gems", "gems")
        bank = sql.valueAtNumber(PlayerID, "Solde", "bank")
        # Sauvegarde des valeurs de la saison en  cours par Joueur
        save = sql.add(PlayerID, "idseasons", nbs, "seasons")
        if save != 404 and save != 102:
            sql.updateField(PlayerID, "gem", [solde, nbs], "seasons")
            sql.updateField(PlayerID, "bank", [bank, nbs], "seasons")
            # Reset solde de gems et solde de la banque
            sql.updateField(PlayerID, "gems", 0, "gems")
            sql.updateField(PlayerID, "Solde", 0, "bank")
            # Reset dans l'inventaire des objets à prix fixe du marché
            for x in GI.exception:
                if x != "bank_upgrade":
                    sql.updateField(PlayerID, x, 0, "inventory")
            # reset dans l'inventaire des objets événementiels
            for x in GF.ObjetEventEnd:
                if x != "bank_upgrade":
                    sql.updateField(PlayerID, x, 0, "inventory")
    with open('gems/bourse.json', 'r') as fp:
        dict = json.load(fp)
    dict["total"] = nbs + 1
    with open('gems/bourse.json', 'w') as fp:
        json.dump(dict, fp, indent=4)
    return True
