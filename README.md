# Mini-inferences-JDM
## Read-me: Analyseur de relations sémantiques (JeuxDeMots.org)

**Outil**

Ce programme analyse les relations sémantiques entre des entités dans la base de données JeuxDeMots.org. Il exploite des techniques d'induction, de déduction et de transitivité pour identifier les liens conceptuels entre les mots.

**Installation**

```bash
pip install -r requirements.txt
```

**Fonctionnement**

Le programme s'exécute en ligne de commande et attend trois arguments :

* `mot`: Le mot de départ.
* `relation`: La relation sémantique à tester (en français).
* `entité`: L'entité finale à atteindre.

**Exemple**

```bash
python chercher_preuve.py "Tour Eiffel" "r_lieu" "Europe"
```

Cette commande recherche des preuves de la relation "lieu" ("r_lieu") entre "Tour Eiffel" et "Europe".

**Résultats**

Le programme affiche un message de résultat détaillant :

* Les preuves de transitivité (si applicables).
* Les preuves par déduction à partir de relations génériques.
* Les preuves par induction à partir de relations spécifiques.
* Les résultats pour la relation inversée (test de symétrie).

**Structure**

Le code est modulaire :

* `dataSaving.py` gère la sauvegarde des données téléchargées (fichiers texte et JSON).
* `dataHandling.py` interagit avec l'API de JeuxDeMots.org, récupère et traite les données.
* `operators.py` implémente les fonctions de recherche de relations (transitivité, déduction, induction).
* `main.py` est le point d'entrée, gérant l'interface utilisateur et l'affichage des résultats.

**Utilisation**

Exécutez **main.py** pour analyser des paires mot-entité et explorer les relations sémantiques vous pouvez changer les relations souhaitées au sein du main.

**Remarques**

* Le programme utilise des données téléchargées localement de JeuxDeMots.org.
* Il est conçu pour être extensible pour intégrer de nouvelles fonctionnalités ou sources de données.


