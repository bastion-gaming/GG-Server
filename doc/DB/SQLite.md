# SQLite
## def nom_ID(nom):
La fonction convertit une chaine de caractère (nom) provenant de l'API discord contenant l'ID discord d'un joueur en nombre entier.

## def init():
Initialisation de la base de données.
- Récupère la liste des tables de la base de données dans le fichier DBlist.json.
- A partir de cette liste, pour chaque tables, la fonction va chercher la structure de la table dans le dossier Templates et génère le script de création de cette table.
- Exécute chaque script de création.
PS: si la table existe déja, la table n'est pas créée.

## def checkField():
A partir de la liste des tables de la base de données stocké dans le fichier DBlist.json et des structure associés de chaque table ce trouvant dans le dossier Templates, la fonction va vérifié si la structure de chaque table est correct dans la base de données.
- Si la structure de la base de données est identique au template alors la fonction passe a la table suivante.
- Si une colonne de la table présente dans la base de données n'est pas dans le template, alors la fonction supprime cette colonne de la base de données.
- Si une colonne du template est manquante dans la base de données alors cette colonne est ajouté a la base de données.

## def get_SuperID(ID, name_pl):
La fonction va chercher le SuperID d'un joueur (identifiant principal permettant le multi plateformes) dans la table centrale de la base de données.
Pour trouver cette identifiant principal, la fonction a besoin du nom de la plateforme (name_pl) et de l'identifiant personnel du compte de cette plateforme (ID)

Exemple: Si l'on prend la plateforme Discord, name_pl sera "discord" et l'ID correspond à l'identifiant du compte discord du joueur (un nombre à 18 chiffre)

## def get_PlayerID(SuperID, nameDB = None):
La fonction va chercher le PlayerID d'un joueur (identifiant dans le jeu)
- SuperID correspond au SuperID du joueur en question
- nameDB est le nom de la table principale du jeu (pour Get Gems cette table principale est "gems")

## def userID(i, nameDB = None):
Permet de retourner les informations provenant de la table principale IDs en fonction de la ligne de la table principale du jeu selectionné.
- i: numero de la ligne de la table nameDB
- nameDB: nom de la table sélectionnée


## def newPlayer(ID, nameDB, platform, name = None):
Ajoute un nouveau joueur dans la table principale IDs
- ID: identifant du compte de la platforme du nouveau joueur
- nameDB: nom de la table principale du jeu
- platform: nom de la plateforme du nouveau joueur
- name: (optionnel) pseudo du nouveau joueur sur la platforme  

## def newGuild(param):
A chaque fois que le bot se connecte sur un nouveau serveur discord, les information sur ce serveur sont ajouté dans la table Guild.
param: dictionnaire contenant les informations sur le serveur discord (ID, nom)

## def countTotalGems():
Retourne la somme total des lignes de la colonne gems dans la table gems.

## def countTotalSpinelles():
Retourne la somme total des lignes de la colonne spinelles dans la table gems.

## def taille(nameDB):
Retourne la taille de la table selectionnée.

## def updateField(PlayerID, fieldName, fieldValue, nameDB):
Met à jour un élement d'une ligne, identifié par le PlayerID, et d'une colonne selectionnée.
- PlayerID: ID du joueur dans le jeu
- fieldName: Nom de la colonne
- fieldValue: Nouvelle valeur qui remplacera l'ancienne se trouvant dans la table.
- nameDB: Nom de la table

## def valueAt(PlayerID, fieldName, nameDB):
Retourne une liste de valeurs se trouvant sur une meme line de la table selectionnée.
- PlayerID: ID du joueur dans le jeu
- fieldName: Nom de la colonne selectionnée
- nameDB: Nomd de la table
Dans la plupart des cas, le PlayerID permet de selectionner la ligne et fieldName la colonne. La fonction va alors retourner une liste contenant 1 seul élément.

Dans les cas particuliers, une ligne peut être identifiée grace a 2 clés, PlayerID est la première clé et fieldName est alors la deuxième clé. Dans ce cas la fonction va retourner une liste de plusieurs éléments.

## def valueAtNumber(PlayerID, fieldName, nameDB):
Fonctionne comme la fonction valueAt.
La particularité de cette fonction est que, comparé a la fonction valueAt, elle retourne directement l'élément et non une liste.

Lorsqu'il n'y as qu'un seul élément dans la liste de la fonction valueAt, la fonction va alors retourner directement cette valeur.
Dans le cas ou plusieurs éléments sont présent dans la liste, seul le premier élément sera retourner.

## def addGems(PlayerID, nb):
Ajoute des gems au compteur de gems d'un joueur.
- PlayerID: Id du joueur dans le jeu
- nb: nombre entier de gems à ajouter au joueur

## def addSpinelles(PlayerID, nb):
Ajoute des spinelles au compteur de spinelles d'un joueur.
- PlayerID: Id du joueur dans le jeu
- nb: nombre entier de spinelles à ajouter au joueur

## def spam(PlayerID, couldown, nameElem, nameDB):
Récupère l'heure de la dernière exécution de la commande selectionnée. Calcul le temps restant en se basant sur la durée du couldown avant de pouvoir exécuter une nouvelle fois la commande.
Si la valeur est inférieur à 0 retourne True sinon retourne False.
- PlayerID: ID du joueur dans le jeu
- couldown: Nombre de seconde d'attente entre 2 commandes du même nom
- nameElem: nom de la commande
- nameDB: Nom de la table principale du jeu

## def updateComTime(PlayerID, nameElem, nameDB):
Met à jour l'heure stocké de la ligne représenter par les deux clé PlayerID et nameElem dans la table nameDB.
- PlayerID: ID du jeu dans le jeu
- nameElem: Nom de la commande du jeu
- nameDB: Nom de la table principale du jeu

## def add(PlayerID, nameElem, nbElem, nameDB):
Permet d'ajouter une valeur a un champ d'une table.
Si le champ existe, alors les valeurs sont additionnée.
Si le champ n'éxiste pas, une nouvelle ligne est créée avec la valeur que l'on souhaite modifier.
- PlayerID: ID du joeur en jeu
- nameElem: Nom de la colonne a modifier
- nbElem: Valeur à ajouter
- nameDB: Nom de la table
