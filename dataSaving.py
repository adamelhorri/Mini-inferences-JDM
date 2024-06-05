# Importation des bibliothèques nécessaires
import os
import json
import requests
from bs4 import BeautifulSoup as bs
from scrapping import getFromURL  # On suppose que scrapping.py contient la fonction getFromURL

# Fonction createTxt(mot, entrant, relation)
def createTxt(mot, entrant, relation):
    """
    Créer un fichier texte contenant les données brutes récupérées de JeuxDeMots.org.

    Args:
        mot (str): Le mot pour lequel on recherche des relations.
        entrant (bool): Indique si on recherche des relations entrantes (True) ou sortantes (False).
        relation (str): La relation sémantique spécifique à rechercher.

    Returns:
        str: Le chemin du fichier texte créé.
    """

    # Récupération des données brutes via la fonction getFromURL
    prod = getFromURL(mot, entrant, relation)

    # Nettoyage du mot pour utilisation dans le nom de fichier (remplacement d'espaces et apostrophes)
    mot_cleaned = mot.replace(" ", "_").replace("'", "")

    # Construction du nom de fichier en fonction du sens de la relation (entrant ou sortant)
    fileTxtName = f"data/{mot_cleaned}{relation}_{'e' if entrant else 's'}.txt"

    # Vérification de l'existence du fichier et de sa taille (vide ou non)
    if not os.path.exists(fileTxtName) or os.path.getsize(fileTxtName) == 0:
        # Création du fichier texte en mode écriture avec encodage UTF-8
        with open(fileTxtName, "w", encoding="utf-8") as fileTxt:
            # Ecriture des données brutes dans le fichier
            fileTxt.write(str(prod))

    # Retourne le chemin du fichier texte créé
    return fileTxtName

# Fonction convert(expression)
def convert(expression):
    """
    Convertit une chaîne de caractères contenant des éléments séparés par des points-virgules,
    en tenant compte des apostrophes qui peuvent faire partie des éléments.

    Args:
        expression (str): La chaîne de caractères à convertir.

    Returns:
        list: Une liste d'éléments extraits de la chaîne de caractères d'origine.
    """

    resultat = []
    tmp = ""  # Variable temporaire pour stocker un élément en cours de construction
    cond = False  # Indicateur d'apostrophe "ouverte"

    # Parcours de la chaîne de caractères caractère par caractère
    for i in range(len(expression)):
        # Gestion du dernier caractère (éviter un index hors limites)
        if i + 1 == len(expression):
            tmp += expression[i]
            resultat.append(tmp)  # Ajout du dernier élément à la liste
        else:
            # Détection d'une apostrophe suivie d'un point-virgule (fermeture d'apostrophe)
            if expression[i] == "'" and expression[i + 1] != ";":
                cond = True
            elif expression[i] == "'" and expression[i + 1] == ";":
                cond = False

            # Ajout d'un caractère à l'élément en cours de construction si on est pas dans une apostrophe "ouverte"
            # ou si le caractère n'est pas un point-virgule
            if cond or expression[i] != ";":
                tmp += expression[i]
            else:  # Si on rencontre un point-virgule hors apostrophe, on a un élément complet
                resultat.append(tmp)  # Ajout de l'élément précédent à la liste
                tmp = ""  # Réinitialisation de la variable temporaire pour le prochain élément

    return resultat

# Fonction createJSON(mot, entrant, relation)
def createJSON(mot, entrant, relation):
    """
    Créer un fichier JSON à partir des données brutes récupérées et stockées dans un fichier texte.

    Args:
        mot (str): Le mot pour lequel on recherche des relations.
        entrant (bool): Indique si on recherche des relations entrantes (True) ou sortantes (False).
        relation (str): La relation sémantique spécifique à rechercher.

    Returns:
        str: Le chemin du fichier JSON créé.
    """

    # Nettoyage du mot pour utilisation dans le nom de fichier (remplacement d'espaces et apostrophes)
    mot_cleaned = mot.replace(" ", "_").replace("'", "")

    # Construction du nom de fichier texte source (à partir duquel on va lire les données brutes)
    fileTxtName = f"data/{mot_cleaned}{relation}_{'e' if entrant else 's'}.txt"

    # Construction du nom de fichier JSON cible
    fileJSONName = f"data/{mot_cleaned}{relation}_{'e' if entrant else 's'}.json"

    # Ouverture du fichier texte en lecture avec encodage UTF-8
    with open(f"data/{mot_cleaned}{relation}_{'e' if entrant else 's'}.txt", "r", encoding="utf-8") as fileTxt:
        # Lecture du contenu du fichier texte ligne par ligne
        lines = fileTxt.readlines()

    # Ouverture du fichier JSON en écriture avec encodage UTF-8
    with open(fileJSONName, "w", encoding="utf-8") as fileJSON:

        # Définition des champs attendus pour chaque type de données ("nt", "e", "rt", "r")
        fields_nt = ['ntname']
        fields_e = ["name", "type", "w", "formated name"]
        fields_rt = ['trname', 'trgpname', 'rthelp']
        fields_r = ["node1", "node2", "type", "w"]

        # Dictionnaires pour stocker les données extraites
        dict0, dict_e, dict_rt, dict_r, dict_nt = {}, {}, {}, {}, {}

        # Parcours de chaque ligne du fichier texte
        for line in lines:
            # Nettoyage de la ligne en supprimant les caractères d'espace en fin de ligne
            description = list(convert(line.strip()))

            # Traitement de la ligne en fonction du premier élément (indicateur de type de donnée)
            if description:
                if description[0] == "nt":
                    # Stockage des données de type "nt" dans le dictionnaire dédié
                    dict_nt[description[1]] = {fields_nt[i]: description[i + 2] for i in range(len(fields_nt)) if i + 2 < len(description)}
                elif description[0] == "e":
                    # Stockage des données d'entité ("e") dans le dictionnaire dédié
                    dict_e[description[1]] = {fields_e[i]: description[i + 2] for i in range(len(fields_e)) if i + 2 < len(description)}
                    # Gestion d'un champ optionnel ("formated name") si la description a plus de 5 éléments
                    if len(description) > 5:
                        dict_e[description[1]][fields_e[3]] = description[5]
                elif description[0] == "rt":
                    # Stockage des données de relation thématique ("rt") dans le dictionnaire dédié
                    dict_rt[description[1]] = {fields_rt[i]: description[i + 2] for i in range(len(fields_rt)) if i + 2 < len(description)}
                    # Gestion d'un champ optionnel ("rthelp") si la description a plus de 4 éléments
                    if len(description) > 4:
                        dict_rt[description[1]][fields_rt[2]] = description[4]
                elif description[0] == "r":
                    # Stockage des données de relation ("r") dans le dictionnaire dédié
                    dict_r[description[1]] = {fields_r[i]: description[i + 2] for i in range(len(fields_r)) if i + 2 < len(description)}

        # Création d'un dictionnaire principal contenant les sous-dictionnaires par type de données
        dict0.update({"nt": dict_nt, "e": dict_e, "r": dict_r, "rt": dict_rt})

        # Ecriture du dictionnaire principal dans le fichier JSON avec indentation pour lisibilité
        json.dump(dict0, fileJSON, indent=4)

    # Retourne le chemin du fichier JSON créé
    return fileJSONName

# Fonction getData(mot, entrant, relation)
def getData(mot, entrant, relation):
    """
    Fonction principale pour récupérer des données de JeuxDeMots.org, 
    les stocker dans des fichiers et retourner un dictionnaire contenant ces données.

    Args:
        mot (str): Le mot pour lequel on recherche des relations.
        entrant (bool): Indique si on recherche des relations entrantes (True) ou sortantes (False).
    
        relation (str): La relation sémantique spécifique à rechercher.

    Returns:
        dict: Le dictionnaire contenant les données chargées depuis les fichiers JSON.
    """

    # Création du fichier texte s'il n'existe pas déjà (via createTxt)
    createTxt(mot, entrant, relation)

    # Création du fichier JSON à partir du fichier texte (via createJSON)
    createJSON(mot, entrant, relation)

    # Nettoyage du mot pour utilisation dans le nom de fichier (remplacement d'espaces et apostrophes)
    mot_cleaned = mot.replace(" ", "_").replace("'", "")

    # Construction du nom de fichier JSON contenant les données finales
    fileJSONName = f"data/{mot_cleaned}{relation}_{'e' if entrant else 's'}.json"

    # Ouverture du fichier JSON en lecture avec encodage UTF-8
    with open(fileJSONName, "r", encoding="utf-8") as fileJSON:
        # Chargement du contenu du fichier JSON dans un dictionnaire
        data = json.load(fileJSON)

    # Retourne le dictionnaire chargé à partir du fichier JSON
    return data
