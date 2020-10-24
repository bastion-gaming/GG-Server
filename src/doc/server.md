# server
Fichier central, permettant l'exécution du Bot.
Il est découpé en plusieurs parties :

1. Ouverture des ports : Le port `tcp://*:5555` sera ouvert grâce à
ZMQ
2. L'Initialisation des variables et affichage des message de bon déroulement du lancement.
  - Les bots ayant besoin de déjà exister dans la base de donnée sont créer et injecter dans cette dernière
  - Les langues sont initialisées
  - Les saisons sont initialisées
  - La bourse est recréée si elle n'existe pas, si oui elle est relancée.
3. Puis va avoir lieu le traitement des messages
  - La verification du message dit **GGconect** qui est le signal envoyé par les clients lorsque ces derniers se connecte. Le serveur leur renvoie alors des informations primordiales tel que les dates des saisons et le nombre de saison.
  - Les messages admin qui permettent via le seul client administrateur de stopper le serveur ou d'intéragir avec la base de donnée
  - Seulement dans le dernier `else` grâce à la fonction `exec_commands` issue du package "manage commands" le message vas être traité

4. La réponse au client en fonction du retour de la fonction `exec_commands`
