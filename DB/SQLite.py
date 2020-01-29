import sqlite3 as sql
import time as t
import json


DB_NOM = 'bastionDB'


def nom_ID(nom):
    """Convertis un nom en ID discord """
    if len(nom) == 21:
        ID = int(nom[2:20])
    elif len(nom) == 22:
        ID = int(nom[3:21])
    else:
        print("DB >> mauvais nom")
        ID = -1
    return(ID)


# ===============================================================================
# Ouverture du fichier DB
# ===============================================================================
conn = sql.connect('DB/{}.db'.format(DB_NOM))


# ===============================================================================
# Initialisation et vérification de la DB
# ===============================================================================
def init():
    # Liste des tables
    with open("DB/DBlist.json", "r") as f:
        list = json.load(f)
    for one in list:
        # Ouverture du template de la table en cours
        with open("DB/Templates/{}Template.json".format(one), "r") as f:
            t = json.load(f)
        cursor = conn.cursor()
        # Création du script
        script = "CREATE TABLE IF NOT EXISTS {}(".format(one)
        i = 0
        PRIMARYKEY = ""
        PRIMARYKEYlink = ""
        link = ""
        for x in t:
            if i != 0:
                script += ", "
            y = t[x].split("_")
            if len(y) > 1:
                if y[0] == "ID":
                    script += "{0} {1} NOT NULL".format(x, y[1])
                    link = "FOREIGN KEY(ID) REFERENCES IDs(ID)"
                elif y[0] == "PRIMARYKEY":
                    script += "{0} {1} NOT NULL".format(x, y[1])
                    PRIMARYKEY = "{}".format(x)
                elif y[0] == "link":
                    script += "{0} INTEGER NOT NULL".format(x)
                    PRIMARYKEYlink = "{}".format(x)
                    link = "FOREIGN KEY({1}) REFERENCES {0}({1})".format(y[1], x)
            else:
                script += "{0} {1}".format(x, t[x])
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
    flag = 0
    FctCheck = False
    while not FctCheck:
        try:
            FctCheck = True
            # Liste des tables
            with open("DB/DBlist.json", "r") as f:
                list = json.load(f)
            for one in list:
                # Ouverture du template de la table en cours
                with open("DB/Templates/{}Template.json".format(one), "r") as f:
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
                        flag = "sup"+str(flag)

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
                        flag = "type"+str(flag)
                    elif not check:
                        if len(y) > 1:
                            temp = y[1]
                        else:
                            temp = y[0]
                        script = "ALTER TABLE {0} ADD COLUMN {1} {2}".format(one, x, temp)
                        cursor.execute(script)
                        flag = "add"+str(flag)
        except:
            FctCheck = False
    return flag


# ===============================================================================
# Gestion des utilisateurs
# ===============================================================================

def get_SuperID(ID, name_pl):
    """
    Permet de convertir un ID discord en PlayerID interne à la base de données
    """
    script = "SELECT * FROM IDs WHERE ID_{1} = {0}".format(ID, name_pl)

    cursor = conn.cursor()
    # print(script)
    cursor.execute(script)
    rows = cursor.fetchall()
    if rows == []:
        # Le PlayerID n'as pas été trouvé. Envoie un code Erreur
        print("SuperID 404 not found")
        return "Error 404"
    else:
        for x in rows:
            return "{}".format(x[0])

# -------------------------------------------------------------------------------


def get_PlayerID(ID, nameDB = None):
    """
    Permet de convertir un ID discord en PlayerID interne à la base de données
    """
    if nameDB == None:
        nameDB = "gems"

    script = "SELECT id{0} FROM {0} WHERE ID = {1}".format(nameDB, ID)
    cursor = conn.cursor()
    # print(script)
    cursor.execute(script)
    rows = cursor.fetchall()
    if rows == []:
        # Le PlayerID n'as pas été trouvé. Envoie un code Erreur
        print("PlayerID 404 not found")
        return "Error 404"
    else:
        for x in rows:
            return "{}".format(x[0])

# -------------------------------------------------------------------------------


def userID(i, nameDB = None):
    if nameDB == None:
        nameDB = "bastion"
    script = "SELECT ID_discord FROM {1} JOIN IDs USING(ID) WHERE id{1} = '{0}'".format(i, nameDB)
    cursor = conn.cursor()
    cursor.execute(script)
    ID = cursor.fetchall()
    return ID[0][0]

# -------------------------------------------------------------------------------


def newPlayer(ID, nameDB, platform):
    """
    Permet d'ajouter un nouveau joueur à la base de donnée en fonction de son ID.

    ID: int de l'ID du joueur
    """
    with open("DB/Templates/{}Template.json".format(nameDB), "r") as f:
        t = json.load(f)
    if nameDB == "gems":
        with open("DB/Templates/dailyTemplate.json", "r") as f:
            t2 = json.load(f)
        with open("DB/Templates/bankTemplate.json", "r") as f:
            t3 = json.load(f)

    SuperID = get_SuperID(ID, platform)
    cursor = conn.cursor()
    if SuperID == "Error 404":
        # Init du joueur avec les champs de base
        script = "INSERT INTO IDs (ID_{1}) VALUES ({0})".format(ID, platform)
        cursor.execute(script)
        conn.commit()
        SuperID = get_SuperID(ID, platform)
        data = "ID"
        values = SuperID
        for x in t:
            if x != "id{}".format(nameDB) and x != "ID":
                data += ", {}".format(x)
                if "INTEGER" in t[x]:
                    values += ", 0"
                else:
                    values += ", NULL"
        script = "INSERT INTO {0} ({1}) VALUES ({2})".format(nameDB, data, values)
        cursor.execute(script)
        conn.commit()
        if nameDB == "gems":
            # Init du joueur dans Get Gems avec les champs de base
            PlayerID = get_PlayerID(SuperID, "gems")
            data = "idgems"
            values = PlayerID
            for x in t2:
                if x != "id{}".format(nameDB) and x != "ID":
                    data += ", {}".format(x)
                    if "INTEGER" in t2[x]:
                        values += ", 0"
                    else:
                        values += ", NULL"
            script = "INSERT INTO daily ({0}) VALUES ({1})".format(data, values)
            # print(script)
            cursor.execute(script)
            conn.commit()

            data = "idgems"
            values = PlayerID
            for x in t3:
                if x != "id{}".format(nameDB) and x != "ID":
                    data += ", {}".format(x)
                    if "INTEGER" in t3[x]:
                        values += ", 0"
                    else:
                        values += ", NULL"
            script = "INSERT INTO bank ({0}) VALUES ({1})".format(data, values)
            # print(script)
            cursor.execute(script)
            conn.commit()
        return ("Le joueur a été ajouté !")
    else:
        return ("Le joueur existe déjà")


# ===============================================================================
# Compteur
# ===============================================================================
def countTotalMsg():
    # Donne le nombre total de messages écrit sur le discord de Bastion
    script = "SELECT SUM(nbmsg) FROM bastion"
    cursor = conn.cursor()
    cursor.execute(script)
    for a in cursor.fetchall():
        return a[0]

# -------------------------------------------------------------------------------


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
    """Retourne la taille de la table selectionner"""
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
# Liste des tables dont l'enregistrement des données est spécifique
nameDBexcept = ["inventory", "durability", "hothouse", "cooking", "ferment", "trophy", "statgems", "gems_com_time"]

# -------------------------------------------------------------------------------


def updateField(PlayerID, fieldName, fieldValue, nameDB):
    """
    Permet de mettre à jour la valeur fieldName par la fieldValue.

    PlayerID: int de l'PlayerID du joueur.
    fieldName: string du nom du champ à changer
    fieldValue: string qui va remplacer l'ancienne valeur
    """
    if PlayerID != "Error 404":
        if nameDB == None:
            nameDB = "bastion"
        cursor = conn.cursor()

        # Vérification que la donnée fieldName existe dans la table nameDB
        one = valueAt(PlayerID, fieldName, nameDB)
        if one == 0:
            # print("DB >> Le champ n'existe pas")
            return "201"
        else:
            IDname = "idgems"
            script = "UPDATE {0} SET {1} = '{2}' WHERE {4} = '{3}'".format(nameDB, fieldName, fieldValue, PlayerID, IDname)
            for x in nameDBexcept:
                if x == nameDB:
                    if x == "inventory":
                        script = "UPDATE {0} SET Stock = '{2}' WHERE Item = '{1}' and idgems = '{3}'".format(nameDB, fieldName, fieldValue, PlayerID)
                    elif x == "trophy" or x == "statgems":
                        script = "UPDATE {0} SET Stock = '{2}' WHERE Nom = '{1}' and idgems = '{3}'".format(nameDB, fieldName, fieldValue, PlayerID, IDname)
                    elif x == "durability":
                        script = "UPDATE {0} SET Durability = '{2}' WHERE Item = '{1}' and idgems = '{3}'".format(nameDB, fieldName, fieldValue, PlayerID, IDname)
                    elif x == "gems_com_time":
                        script = "UPDATE {0} SET Com_time = '{2}' WHERE Commande = '{1}' and id{4} = '{3}'".format(nameDB, fieldName, fieldValue, PlayerID, IDname)
                    elif x == "hothouse":
                        script = "UPDATE {0} SET Time = '{2}', Plante = '{5}' WHERE idPlantation = '{1}' and idgems = '{3}'".format(nameDB, fieldName, fieldValue[0], PlayerID, IDname, fieldValue[1])
                    elif x == "cooking":
                        script = "UPDATE {0} SET Time = '{2}', Plat = '{5}'  WHERE idFour = '{1}' and idgems = '{3}'".format(nameDB, fieldName, fieldValue[0], PlayerID, IDname, fieldValue[1])
                    elif x == "ferment":
                        script = "UPDATE {0} SET Time = '{2}', Alcool = '{5}'  WHERE idBarrel = '{1}' and idgems = '{3}'".format(nameDB, fieldName, fieldValue[0], PlayerID, IDname, fieldValue[1])
                    else:
                        return "202"
            # print("==== updateField ====")
            # print(script)
            cursor.execute(script)
            conn.commit()
            return "200"
    else:
        return "404"

# -------------------------------------------------------------------------------


def valueAt(PlayerID, fieldName, nameDB):
    """
    Permet de récupérer la valeur contenue dans le champ fieldName de PlayerID

    PlayerID: int de l'PlayerID du joueur
    fieldName: string du nom du champ à chercher
    """
    if PlayerID != "Error 404":
        cursor = conn.cursor()

        if not nameDB in nameDBexcept:
            try:
                # Récupération de la valeur de fieldName dans la table nameDB
                if nameDB == "gems":
                    script = "SELECT {1} FROM {0} WHERE id{0} = '{2}'".format(nameDB, fieldName, PlayerID)
                else:
                    script = "SELECT {1} FROM {0} JOIN gems USING(idgems) WHERE idgems = '{2}'".format(nameDB, fieldName, PlayerID)
                # print(script)
                cursor.execute(script)
                value = cursor.fetchall()
            except:
                # Aucune données n'a été trouvé
                value = []
        else:
            fieldName2 = ""
            for x in nameDBexcept:
                if x == nameDB:
                    if x == "inventory" or x == "durability":
                        fieldName2 = "Item"
                        if x == "inventory":
                            fieldName3 = "Stock, Item"
                        else:
                            fieldName3 = "Durability, Item"
                    elif x == "trophy" or x == "statgems":
                        fieldName2 = "Nom"
                        fieldName3 = "Stock, Nom"
                    elif x == "hothouse":
                        fieldName2 = "idPlantation"
                        fieldName3 = "Time, Plante, idPlantation"
                    elif x == "cooking":
                        fieldName2 = "idFour"
                        fieldName3 = "Time, Plat, idFour"
                    elif x == "ferment":
                        fieldName2 = "idBarrel"
                        fieldName3 = "Time, Alcool, idBarrel"
                    elif x == "gems_com_time":
                        fieldName2 = "Commande"
                        fieldName3 = "Com_time, Commande"
                    link = "gems"
            try:
                # Paramètre spécial (à mettre a la place du fieldName) permettant de retourner toutes les valeurs liées à un PlayerID dans la table nameDB
                if fieldName == "all":
                    script = "SELECT {2} FROM {0} JOIN {3} USING(id{3}) WHERE id{3} = '{4}'".format(nameDB, fieldName, fieldName3, link, PlayerID)
                else:
                    # Récupération de la valeur de fieldName dans la table nameDB
                    script = "SELECT {5} FROM {0} JOIN {3} USING(id{3}) WHERE id{3} = '{4}' and {2} = '{1}'".format(nameDB, fieldName, fieldName2, link, PlayerID, fieldName3)
                # print(script)
                cursor.execute(script)
                value = cursor.fetchall()
            except:
                # Aucune données n'a été trouvé
                value = []

        if value == []:
            return 0
        else:
            if fieldName == "all":
                return value
            else:
                return value[0]

# -------------------------------------------------------------------------------


def valueAtNumber(PlayerID, fieldName, nameDB):
    if fieldName != "all":
        VAN = valueAt(PlayerID, fieldName, nameDB)
        if VAN != 0 and VAN != None:
            VAN = VAN[0]
        return VAN
    else:
        return 0

# -------------------------------------------------------------------------------


def addGems(PlayerID, nb):
    """
    Permet d'ajouter un nombre de gems à quelqu'un. Il nous faut son PlayerID et le nombre de gems.
    Si vous souhaitez en retirer mettez un nombre négatif.
    Si il n'y a pas assez d'argent sur le compte la fonction retourne un nombre
    strictement inférieur à 0.
    """
    old_value = valueAtNumber(PlayerID, "gems", "gems")
    new_value = int(old_value) + int(nb)
    if new_value >= 0:
        updateField(PlayerID, "gems", new_value, "gems")
        print("DB >> Le compte de " + str(PlayerID) + " est maintenant de: " + str(new_value))
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
    old_value = valueAtNumber(PlayerID, "spinelles", "gems")
    new_value = int(old_value) + int(nb)
    if new_value >= 0:
        updateField(PlayerID, "spinelles", new_value, "gems")
        print("DB >> Le compte de " + str(PlayerID) + " est maintenant de: " + str(new_value))
    else:
        print("DB >> Il n'y a pas assez sur ce compte !")
    return str(new_value)

# -------------------------------------------------------------------------------


def spam(PlayerID, couldown, nameElem, nameDB):
    """Antispam """
    if nameDB == "gems":
        nameDB = "{}_com_time".format(nameDB)

    ComTime = valueAt(PlayerID, nameElem, nameDB)
    if ComTime == 0 or ComTime == None:
        return True
    elif ComTime[0] != 0:
        time = ComTime[0]
    else:
        return True

    # on récupère la date de la dernière commande
    return(float(time) < t.time()-couldown)

# -------------------------------------------------------------------------------


def updateComTime(PlayerID, nameElem, nameDB):
    """
    Met à jour la date du dernier appel à une fonction
    """
    if nameDB == "gems":
        nameDB = "{}_com_time".format(nameDB)
    else:
        return "Error 404"

    old_value = valueAtNumber(PlayerID, nameElem, nameDB)
    try:
        if old_value != 0:
            new_value = t.time()
            updateField(PlayerID, nameElem, new_value, nameDB)
            return 100
        else:
            add(PlayerID, nameElem, t.time(), nameDB)
            return 101
    except:
        return 404

# -------------------------------------------------------------------------------


def add(PlayerID, nameElem, nbElem, nameDB):
    """
    Permet de modifier le nombre de nameElem pour PlayerID dans la table nameDB
    Pour en retirer mettez nbElemn en négatif
    """
    # print("PlayerID: {}".format(PlayerID))
    old_value = valueAt(PlayerID, nameElem, nameDB)
    # print(old_value)
    if old_value != 0:
        if nameDB == "hothouse" or nameDB == "cooking" or nameDB == "daily" or nameDB == "ferment":
            updateField(PlayerID, nameElem, nbElem, nameDB)
        else:
            new_value = int(old_value[0]) + int(nbElem)
            if new_value < 0:
                new_value = 0
            updateField(PlayerID, nameElem, new_value, nameDB)
        return 100
    else:
        cursor = conn.cursor()
        data = []
        with open("DB/Templates/{}Template.json".format(nameDB), "r") as f:
            t = json.load(f)
        for x in t:
            if x == "idgems":
                data = "{}".format(x)
            else:
                data += ",{}".format(x)

        if not nameDB in nameDBexcept:
            values = "{}".format(PlayerID)
            for x in t:
                y = t[x].split("_")
                if len(y) > 1:
                    y2 = y[1]
                else:
                    y2 = y[0]
                if x == nameElem:
                    values += ",'{}'".format(nbElem)
                elif y2 == "INTEGER":
                    values += ",'0'"
                elif y2 == "TEXT":
                    values += ",''"
        else:
            if nameDB == "inventory" or nameDB == "durability" or nameDB == "trophy" or nameDB == "statgems" or nameDB == "gems_com_time":
                if nameDB == "inventory":
                    data = "idgems, Item, Stock"
                elif nameDB == "durability":
                    data = "idgems, Item, Durability"
                elif nameDB == "trophy" or nameDB == "statgems":
                    data = "idgems, Nom, Stock"
                elif nameDB == "gems_com_time":
                    data = "idgems, Commande, Com_time"
                values = "'{2}', '{0}', '{1}'".format(nameElem, nbElem, PlayerID)
            elif nameDB == "hothouse" or nameDB == "cooking" or nameDB == "ferment":
                if nameDB == "ferment":
                    data = "idgems, idBarrel, Time, Alcool"
                elif nameDB == "cooking":
                    data = "idgems, idFour, Time, Plat"
                elif nameDB == "hothouse":
                    data = "idgems, idPlantation, Time, Plante"
                values = "'{3}', '{0}', '{1}', '{2}'".format(nameElem, nbElem[0], nbElem[1], PlayerID)
        try:
            script = "INSERT INTO {0} ({1}) VALUES ({2})".format(nameDB, data, values)
            # print("==== add ====")
            # print(script)
            cursor.execute(script)
            conn.commit()
            return 101
        except:
            return 404
