import csv
import datetime as dt
from gems import gemsFonctions as GF, gemsItems as GI
from languages import lang as lang_P


def csv_add(name):
    temp = []
    vente = 0
    achat = 0
    for x in GF.objetItem:
        if x.nom == name:
            vente = x.vente
            achat = x.achat
    for x in GF.objetOutil:
        if x.nom == name:
            if x.type == "bank":
                return True
            else:
                vente = x.vente
                achat = x.achat
    now = dt.datetime.now()
    try:
        with open('gems/bourse/{item}-{year}-{month}.csv'.format(item=name, year=now.year, month=now.month), 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in csvreader:
                temp.append(row)
        temp.append([now, vente, achat])
        with open('gems/bourse/{item}-{year}-{month}.csv'.format(item=name, year=now.year, month=now.month), 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerows(temp)
    except:
        with open('gems/bourse/{item}-{year}-{month}.csv'.format(item=name, year=now.year, month=now.month), 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow([now, vente, achat])
    return True


def csv_read(param):
    lang = param["lang"]
    item = param["item"]
    year = param["year"]
    month = param["month"]
    msg = []
    temp = []
    try:
        with open('gems/bourse/{item}-{year}-{month}.csv'.format(item=item, year=year, month=month), 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in csvreader:
                temp.append(row)
    except:
        msg.append("NOK")
        msg.append([])
        msg.append(lang)
        return msg
    msg.append("OK")
    msg.append(lang)
    msg.append(temp)
    return msg


def listobjet(param):
    type = param["type"]
    lang = param["lang"]
    msg = []
    list = []
    if type == "item" or type == "items":
        for c in GF.objetItem:
            check = False
            for x in GI.exception:
                if x == c.nom:
                    check = True
            for x in GF.ObjetEventEnd:
                if x == c.nom:
                    check = True
            if not check:
                list.append(c.nom)
    elif type == "outil" or type == "outils":
        for c in GF.objetOutil:
            check = False
            for x in GI.exception:
                if x == c.nom:
                    check = True
            if c.type != "bank" and not check:
                list.append(c.nom)
    else:
        msg.append("NOK")
        msg.append(lang_P.forge_msg(lang, "WarningMsg", None, False, 1))
        return msg
    msg.append("OK")
    msg.append(list)
    return msg
