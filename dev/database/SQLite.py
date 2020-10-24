import sqlite3 as sql
import json
import time as t

DB_NOM = 'GetGems'
DIR = 'database'
# ===============================================================================
# Ouverture du fichier DB
# ===============================================================================
conn = sql.connect('{d}/{n}.db'.format(n=DB_NOM, d=DIR), check_same_thread=False)


def init():
    # Liste des tables
    with open("{d}/DBlist.json".format(d=DIR), "r") as f:
        list = json.load(f)
    for one in list:
        # Ouverture du template de la table en cours
        with open("{d}/Templates/{v}Template.json".format(v=one, d=DIR), "r") as f:
            template = json.load(f)
        cursor = conn.cursor()
        # Création du script
        script = "CREATE TABLE IF NOT EXISTS {}(".format(one)
        i = 0
        PRIMARYKEY = ""
        PRIMARYKEYlink = ""
        link = ""
        for x in template:
            if i != 0:
                script += ", "
            y = template[x].split("_")
            if len(y) > 1:
                if y[0] == "PRIMARYKEY":
                    script += "{0} {1} NOT NULL".format(x, y[1])
                    PRIMARYKEY = "{}".format(x)
                elif y[0] == "link":
                    script += "{0} INTEGER NOT NULL".format(x)
                    PRIMARYKEYlink = "{}".format(x)
                    link = "FOREIGN KEY({1}) REFERENCES {0}({1})".format(y[1], x)
            else:
                script += "{0} {1}".format(x, template[x])
            i += 1
        # Configuration des clés primaires
        if PRIMARYKEY != "" and PRIMARYKEYlink != "":
            script += ", PRIMARY KEY ({}, {})".format(PRIMARYKEY, PRIMARYKEYlink)
        elif PRIMARYKEY != "" and PRIMARYKEYlink == "":
            script += ", PRIMARY KEY ({})".format(PRIMARYKEY)
        elif PRIMARYKEY == "" and PRIMARYKEYlink != "":
            script += ", PRIMARY KEY ({})".format(PRIMARYKEYlink)
        if link != "":
            script += ", {}".format(link)
        script += ")"
        # éxécution du script pour la table en cours
        cursor.execute(script)
        conn.commit()
    # Quand toute les tables ont été créée (si elles n'existait pas), envoie un message de fin
    return "SQL >> DB initialisée"


# -------------------------------------------------------------------------------
def checkField():
    # Init de la variable flag
    flag = ""
    FctCheck = False
    while not FctCheck:
        try:
            FctCheck = True
            # Liste des tables
            with open("{0}/DBlist.json".format(DIR), "r") as f:
                list = json.load(f)
            for one in list:
                # Ouverture du template de la table en cours
                with open("{1}/Templates/{0}Template.json".format(one, DIR), "r") as f:
                    t = json.load(f)
                cursor = conn.cursor()
                # Récupération du nom des colonnes de la table en cours
                cursor.execute("PRAGMA table_info({0});".format(one))
                rows = cursor.fetchall()

                # Suppression
                for x in rows:
                    if x[1] not in t:
                        script = "ALTER TABLE {0} RENAME TO {0}_old".format(one)
                        cursor.execute(script)
                        init()
                        cursor.execute("PRAGMA table_info({0}_old);".format(one))
                        temp = ""
                        for z in cursor.fetchall():
                            if temp == "":
                                temp += "{}".format(z[1])
                            else:
                                temp += ", {}".format(z[1])
                        script = "INSERT INTO {0} ({1})\n    SELECT {1}\n    FROM {0}_old".format(one, temp)
                        cursor.execute(script)
                        cursor.execute("DROP TABLE {}_old".format(one))
                        conn.commit()
                        flag += "sup"

                # Type & add
                for x in t:
                    check = False
                    NotCheck = False
                    y = t[x].split("_")
                    for row in rows:
                        if row[1] == x:
                            if len(y) > 1:
                                if row[2] == y[1]:
                                    check = True
                                elif y[0] == "link":
                                    if row[2] == "INTEGER":
                                        check = True
                                    else:
                                        NotCheck = True
                                else:
                                    NotCheck = True
                            else:
                                if row[2] == t[x]:
                                    check = True
                                else:
                                    NotCheck = True
                    if NotCheck:
                        script = "ALTER TABLE {0} RENAME TO {0}_old".format(one)
                        cursor.execute(script)
                        init()
                        cursor.execute("PRAGMA table_info({0}_old);".format(one))
                        temp = ""
                        for z in cursor.fetchall():
                            if temp == "":
                                temp += "{}".format(z[1])
                            else:
                                temp += ", {}".format(z[1])
                        script = "INSERT INTO {0} ({1})\n    SELECT {1}\n    FROM {0}_old".format(one, temp)
                        cursor.execute(script)
                        cursor.execute("DROP TABLE {}_old".format(one))
                        conn.commit()
                        flag += "type"
                    elif not check:
                        if len(y) > 1:
                            temp = y[1]
                        else:
                            temp = y[0]
                        script = "ALTER TABLE {0} ADD COLUMN {1} {2}".format(one, x, temp)
                        cursor.execute(script)
                        flag += "add"
        except:
            FctCheck = False
    return flag


# ===============================================================================
# Gestion des utilisateurs
# ===============================================================================
def newPlayer(ID, platform, name = None):
    """
    Permet d'ajouter un nouveau joueur à la base de donnée en fonction de son ID.

    ID: int de l'ID du joueur
    """
    nameDB = "gems"
    langue = "EN"
    with open("{d}/Templates/gemsTemplate.json".format(d=DIR), "r") as f:
        template = json.load(f)

    PlayerID = get_PlayerID(ID, platform)
    cursor = conn.cursor()
    if PlayerID['error'] == 404:
        # Init du joueur avec les champs de base
        data = "ID_discord, Lang, Pseudo"
        values = '{ID}, "{Lang}", "{Pseudo}"'.format(ID=ID , Lang=langue, Pseudo=name)
        for x in template:
            if x != "id{}".format(nameDB) and x != "ID_discord" and x != "Pseudo" and x != "Lang":
                data += ", {}".format(x)
                if "INTEGER" in template[x]:
                    values += ", 0"
                else:
                    values += ", NULL"
        script = "INSERT INTO gems ({d}) VALUES ({v})".format(d=data, v=values)
        # print(script)
        cursor.execute(script)
        conn.commit()
        return {'error': 0, 'action': 'success'}
    else:
        return {'error': 1, 'action': 'echec'}


# -------------------------------------------------------------------------------
def get_PlayerID(ID, platform):
    """
    Permet de convertir un ID d'une platforme en PlayerID interne à la base de données
    """
    script = "SELECT * FROM gems WHERE ID_{1} = {0}".format(ID, platform)

    cursor = conn.cursor()
    # print(script)
    cursor.execute(script)
    rows = cursor.fetchall()
    if rows == []:
        # Le PlayerID n'as pas été trouvé. Envoie un code Erreur
        # print("PlayerID 404 not found")
        return {'error': 404, 'ID': 0}
    else:
        for x in rows:
            return {'error': 0, 'ID': "{}".format(x[0])}


# -------------------------------------------------------------------------------
def get_Godchilds(PlayerID):
    script = "SELECT Pseudo FROM gems WHERE Godparent = {0}".format(PlayerID)
    cursor = conn.cursor()
    cursor.execute(script)
    rows = cursor.fetchall()
    if rows == []:
        return False
    result = []
    for one in rows:
        result.append(one[0])
    return result


# -------------------------------------------------------------------------------
def in_gems(fieldName, filtre = None, filtreValue = None):
    script = "SELECT {0} FROM gems".format(fieldName)
    if filtre is not None:
        if type(filtre) is list:
            script += " WHERE {0} = '{1}'".format(filtre[0], filtreValue[0])
            for i in range(1, len(filtre)):
                script += " AND {0} = '{1}'".format(filtre[i], filtreValue[i])
        elif type(filtre) is str:
            script += " WHERE {0} = '{1}'".format(filtre, filtreValue)
    cursor = conn.cursor()
    # print(script)
    cursor.execute(script)
    rows = cursor.fetchall()
    if rows == []:
        return False
    return rows


# -------------------------------------------------------------------------------
def platformID(PlayerID, platform):
    script = "SELECT Pseudo, ID_{1} FROM gems WHERE idgems = '{0}'".format(PlayerID, platform)
    cursor = conn.cursor()
    cursor.execute(script)
    ID = cursor.fetchall()
    return ID[0]


# -------------------------------------------------------------------------------
def nom_ID(nom):
    """Convertis un nom en ID discord """
    IDd = in_gems("ID_discord", "Pseudo", nom)
    if IDd is False:
        nom = "{0}".format(nom)
        if len(nom) == 21:
            ID = int(nom[2:20])
        elif len(nom) == 22:
            ID = int(nom[3:21])
        elif len(nom) == 18:
            ID = int(nom)
        else:
            print("DB >> mauvais nom")
            ID = -1
        return(ID)
    else:
        return(IDd[0][0])


# ===============================================================================
# Compteur
# ===============================================================================
def countTotalGems():
    # Donne le nombre total de gems (somme des gems de tout les utilisateurs de Get Gems)
    script = "SELECT SUM(gems) FROM gems"
    cursor = conn.cursor()
    cursor.execute(script)
    for a in cursor.fetchall():
        return a[0]


# -------------------------------------------------------------------------------
def countTotalSpinelles():
    # Donne le nombre total de spinelles (somme des spinelles de tout les utilisateurs de Get Gems)
    script = "SELECT SUM(spinelles) FROM gems"
    cursor = conn.cursor()
    cursor.execute(script)
    for a in cursor.fetchall():
        return a[0]


# -------------------------------------------------------------------------------
def taille(nameDB):
    """Retourne la taille de la table selectionnée"""
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info({0});".format(nameDB))
    rows = cursor.fetchall()
    script = "SELECT count({1}) FROM {0}".format(nameDB, rows[0][1])
    cursor.execute(script)
    for taille in cursor.fetchall():
        return taille[0]


# ===============================================================================
# Fonctions
# ===============================================================================
def addGems(PlayerID, nb):
    """
    Permet d'ajouter un nombre de gems à quelqu'un. Il nous faut son PlayerID et le nombre de gems.
    Si vous souhaitez en retirer mettez un nombre négatif.
    Si il n'y a pas assez d'argent sur le compte la fonction retourne un nombre
    strictement inférieur à 0.
    """
    nameDB = "gems"
    old_value = value(PlayerID, nameDB, "Gems")
    new_value = int(old_value) + int(nb)
    if new_value >= 0:
        update(PlayerID, nameDB, "Gems", new_value)
        print("DB >> Le compte de {n} est maintenant de: {v} Gems".format(n=str(value(PlayerID, "gems", "Pseudo")), v=str(new_value)))
    else:
        print("DB >> Il n'y a pas assez sur ce compte !")
    return str(new_value)


# -------------------------------------------------------------------------------
def addSpinelles(PlayerID, nb):
    """
    Permet d'ajouter un nombre de gems à quelqu'un. Il nous faut son PlayerID et le nombre de gems.
    Si vous souhaitez en retirer mettez un nombre négatif.
    Si il n'y a pas assez d'argent sur le compte la fonction retourne un nombre
    strictement inférieur à 0.
    """
    nameDB = "gems"
    old_value = value(PlayerID, nameDB, "Spinelles")
    new_value = int(old_value) + int(nb)
    if new_value >= 0:
        update(PlayerID, nameDB, "Spinelles", new_value)
        print("DB >> Le compte de {n} est maintenant de: {v} Spinelles".format(n=str(value(PlayerID, "gems", "Pseudo")), v=str(new_value)))
    else:
        print("DB >> Il n'y a pas assez sur ce compte !")
    return str(new_value)


# -------------------------------------------------------------------------------
def spam(PlayerID, couldown, Commande):
    """Antispam """
    nameDB = "gems_com_time"

    ComTime = value(PlayerID, nameDB, "Com_Time", "Commande", Commande)
    if not ComTime or ComTime == None:
        return True
    elif ComTime != 0:
        time = ComTime
    else:
        return True

    # on récupère la date de la dernière commande
    return(float(time) < t.time()-couldown)


# -------------------------------------------------------------------------------
def updateComTime(PlayerID, Commande):
    """
    Met à jour la date du dernier appel à une fonction
    """
    nameDB = "gems_com_time"

    old_value = value(PlayerID, nameDB, "Com_time", "Commande", Commande)
    try:
        if old_value is not False:
            update(PlayerID, nameDB, "Com_time", t.time(), "Commande", Commande)
            return {'error': 0, 'action': 'update success'}
        else:
            create(PlayerID, nameDB, ["Commande", "Com_time"], [Commande, t.time()])
            return {'error': 0, 'action': 'update fail -> create success'}
    except:
        return {'error': 404, 'action': 'echec'}


# -------------------------------------------------------------------------------
def value(PlayerID, nameDB, fieldName, filtre = None, filtreValue = None, order = None):
    """
    int             PlayerID: id du joueur dans la base de données
    string          nameDB: Nom de la table
    string          fieldName: string du nom du champ à chercher
    string/tab      filtre: liste des filtres WHERE
    string/tab      filtreValue: liste des valeurs de chaque filtre
    tab             order: paramètre de tri
    """
    value = []
    mefn = ''
    conn = sql.connect('{d}/{n}.db'.format(n=DB_NOM, d=DIR))
    cursor = conn.cursor()

    try:
        # Récupération de la valeur de fieldName dans la table nameDB
        if type(fieldName) is str:
            mefn = fieldName
        elif type(fieldName) is list:
            for i in range(0, len(fieldName)):
                if i > 0:
                    mefn += ", "
                mefn += "{}".format(fieldName[i])
        else:
            return False
        script = "SELECT {1} FROM {0}".format(nameDB, mefn)
        script += " WHERE idgems = '{0}'".format(PlayerID)
        if filtre is not None:
            if type(filtre) is list:
                for i in range(0, len(filtre)):
                    script += " AND {0} = '{1}'".format(filtre[i], filtreValue[i])
            elif type(filtre) is str:
                script += " AND {0} = '{1}'".format(filtre, filtreValue)
        if order is not None:
            script += " ORDER BY {0}".format(order)
        # print(script)
        cursor.execute(script)
        value = cursor.fetchall()
        # print(value)
    except:
        # Aucune données n'a été trouvé
        value = []

    # print(value)
    if value == []:
        return False
    else:
        if len(value[0]) == 1:
            return value[0][0]
        else:
            return value[0]


# -------------------------------------------------------------------------------
def valueAll(PlayerID, nameDB, fieldName, filtre = None, filtreValue = None, order = None):
    """
    int             PlayerID: id du joueur dans la base de données
    string          nameDB: Nom de la table
    string/tab      fieldName: string du nom du/des champ(s) à chercher
    """
    mefn = ""
    conn = sql.connect('{d}/{n}.db'.format(n=DB_NOM, d=DIR))
    cursor = conn.cursor()

    try:
        # Récupération de la valeur de fieldName dans la table nameDB
        if type(fieldName) is str:
            mefn = fieldName
        elif type(fieldName) is list:
            for i in range(0, len(fieldName)):
                if i > 0:
                    mefn += ", "
                mefn += "{}".format(fieldName[i])
        else:
            return False
        script = "SELECT {1} FROM {0}".format(nameDB, mefn)
        script += " WHERE idgems = '{0}'".format(PlayerID)
        if filtre is not None:
            if type(filtre) is list:
                for i in range(0, len(filtre)):
                    script += " AND {0} = '{1}'".format(filtre[i], filtreValue[i])
            elif type(filtre) is str:
                script += " AND {0} = '{1}'".format(filtre, filtreValue)
        if order is not None:
            script += " ORDER BY {0}".format(order)
        # print(script)
        cursor.execute(script)
        value = cursor.fetchall()
    except:
        # Aucune données n'a été trouvé
        value = []

    # print(value)
    return value


# -------------------------------------------------------------------------------
def create(PlayerID, nameDB, fieldName, fieldValue):
    """
    int             PlayerID: id du joueur dans la base de données
    string          nameDB: Nom de la table
    string/tab      fieldName: nom du/des champ(s) à chercher
    string/tab      fieldValue: valeur associé au fieldName
    string/tab      filtre: liste des filtres WHERE
    string/tab      filtreValue: liste des valeurs de chaque filtre
    tab             order: paramètre de tri
    """
    values = "{}".format(PlayerID)
    data = "idgems"
    script = ""
    conn = sql.connect('{d}/{n}.db'.format(n=DB_NOM, d=DIR))
    cursor = conn.cursor()

    with open("{d}/Templates/{n}Template.json".format(n=nameDB, d=DIR), "r") as f:
        template = json.load(f)
    # creation de la variable data en fonctions du template
    for x in template:
        if x != "idgems":
            data += ",{}".format(x)
    # creation de la variable values en fonctions du template
    for x in template:
        y = template[x].split("_")
        if len(y) > 1:
            y2 = y[1]
        else:
            y2 = y[0]
        if type(fieldName) is list:
            skip = False
            for i in range(0, len(fieldName)):
                if x == fieldName[i]:
                    values += ",'{v}'".format(v=fieldValue[i])
                    skip = True
            if not skip:
                if y2 == "INTEGER":
                    values += ",'0'"
                elif y2 == "TEXT":
                    values += ",''"
        else:
            if x == fieldName:
                values += ",'{v}'".format(v=fieldValue)
            elif y2 == "INTEGER":
                values += ",'0'"
            elif y2 == "TEXT":
                values += ",''"

    try:
        script = "INSERT INTO {0} ({1}) VALUES ({2})".format(nameDB, data, values)
        # print("==== create ====")
        # print(script)
        cursor.execute(script)
        conn.commit()
        return True
    except:
        print('Error SQL create: {}'.format(script))
        return False


# -------------------------------------------------------------------------------
def update(PlayerID, nameDB, fieldName, fieldValue, filtre = None, filtreValue = None, order = None):
    """
    int             PlayerID: id du joueur dans la base de données
    string          nameDB: Nom de la table
    string/tab      fieldName: nom du/des champ(s) à chercher
    string/tab      fieldValue: valeur associé au fieldName
    string/tab      filtre: liste des filtres WHERE
    string/tab      filtreValue: liste des valeurs de chaque filtre
    tab             order: paramètre de tri
    """
    mefdv = ""
    script = ""
    val = value(PlayerID, nameDB, fieldName, filtre, filtreValue, order)
    conn = sql.connect('{d}/{n}.db'.format(n=DB_NOM, d=DIR))
    cursor = conn.cursor()
    # Vérification
    if val != [] or val is not False:
        # Mise en forme des data et values
        if type(fieldName) is list:
            for i in range(0, len(fieldName)):
                if i > 0:
                    mefdv += ", "
                mefdv += "{d} = '{v}'".format(d=fieldName[i], v=fieldValue[i])
        else:
            mefdv = "{d} = '{v}'".format(d=fieldName, v=fieldValue)
        # Mise en forme des filtres
        sF = "WHERE idgems = '{0}'".format(PlayerID)
        if filtre is not None:
            if type(filtre) is list:
                for i in range(0, len(filtre)):
                    sF += " AND {0} = '{1}'".format(filtre[i], filtreValue[i])
            elif type(filtre) is str:
                sF += " AND {0} = '{1}'".format(filtre, filtreValue)

        try:
            script = "UPDATE {n} SET {u} {f}".format(n=nameDB, f=sF, u=mefdv)
            # print("==== updateField ====")
            # print(script)
            cursor.execute(script)
            conn.commit()
            return True
        except:
            print('Error SQL update: {}'.format(script))
            return False
    else:
        return False
