# Importation de la fonction getData (probablement définie dans un autre script)
from dataSaving import getData

# Fonction idEntite(mot, entite, data)
def idEntite(mot, entite, data):
    """
    Récupère les identifiants uniques (id) du mot et de l'entité à partir des données.

    Args:
        mot (str): Le mot pour lequel on recherche l'identifiant.
        entite (str): L'entité pour laquelle on recherche l'identifiant.
        data (dict): Le dictionnaire contenant les données de JeuxDeMots.org.

    Returns:
        dict: Un dictionnaire contenant les identifiants:
              - "idEntite": Identifiant de l'entité.
              - "idMot": Identifiant du mot.

    """

    # Accès au dictionnaire des entités dans les données
    jdex = data["e"]

    # Variables pour stocker les identifiants (-1 par défaut si non trouvés)
    ide = -1
    idm = -1

    # Parcours du dictionnaire des entités
    for entity, info in jdex.items():
        # Nettoyage du nom de l'entité (suppression de quotes)
        name = info['name'].replace("'", "", 2)

        # Comparaison du nom de l'entité avec l'entité recherchée
        if name == entite:
            ide = entity

        # Comparaison du nom de l'entité avec le mot recherché
        if name == mot:
            idm = entity

    # Retourne un dictionnaire contenant les identifiants trouvés
    return {"idEntite": ide, "idMot": idm}

# Fonction idRelation(relation, data)
def idRelation(relation, data):
    """
    Récupère l'identifiant unique (id) de la relation à partir des données.

    Args:
        relation (str): La relation sémantique pour laquelle on recherche l'identifiant.
        data (dict): Le dictionnaire contenant les données de JeuxDeMots.org.

    Returns:
        int: L'identifiant de la relation sémantique, ou -1 si non trouvée.
    """

    # Accès au dictionnaire des relations dans les données
    jdr = data["rt"]

    # Variable pour stocker l'identifiant (-1 par défaut si non trouvé)
    idr = -1

    # Parcours du dictionnaire des relations
    for entity, info in jdr.items():
        # Nettoyage du nom de la relation (suppression de quotes)
        name = info['trname'].replace("'", "", 2)

        # Comparaison du nom de la relation avec la relation recherchée
        if name == relation:
            idr = entity
            break  # On arrête la boucle dès que la relation est trouvée

    # Retourne l'identifiant de la relation, ou -1 si non trouvée
    return idr

# Fonction isRelationEntrante(ide, idr, data)
def isRelationEntrante(ide, idr, data):
    """
    Vérifie si une relation entrante spécifique existe pour une entité donnée.

    Args:
        ide (int): L'identifiant de l'entité.
        idr (int): L'identifiant de la relation.
        data (dict): Le dictionnaire contenant les données de JeuxDeMots.org.

    Returns:
        list: Une liste contenant:
              - [0] (bool): True si la relation entrante existe, False sinon.
              - [1] (str): Le poids de la relation (information optionnelle).
    """

    # Accès au dictionnaire des relations entrantes et sortantes dans les données
    jdr = data["r"]

    # Variables pour stocker le résultat et le poids de la relation
    resultat = False
    w = ""

    # Parcours du dictionnaire des relations
    for entity, info in jdr.items():
        # Nettoyage du noeud cible (entité liée)
        node2 = info['node1'].replace("'", "", 2)
        # Nettoyage du type de relation
        type_val = info['type'].replace("'", "", 2)
        # Stockage du poids de la relation (éventuellement utilisé plus tard)
        w = info["w"]

    
        # Comparaison du noeud cible avec l'entité et du type de relation avec la relation recherchée
        if node2 == ide and type_val == idr:
            resultat = True
            break  # On arrête la boucle dès que la relation est trouvée

    # Retourne une liste contenant le résultat (relation existante) et le poids (facultatif)
    return [resultat, w]

# Fonction isRelSortantePositive(ide, idr, data)
def isRelSortantePositive(ide, idr, data):
    """
    Vérifie si une relation sortante positive (poids positif) existe pour une entité donnée.

    Args:
        ide (int): L'identifiant de l'entité.
        idr (int): L'identifiant de la relation.
        data (dict): Le dictionnaire contenant les données de JeuxDeMots.org.

    Returns:
        bool: True si la relation sortante positive existe, False sinon.
    """

    # Accès au dictionnaire des relations entrantes et sortantes dans les données
    jdr = data["r"]

    # Variable pour stocker le résultat
    resultat = False

    # Parcours du dictionnaire des relations
    for entity, info in jdr.items():
        # Nettoyage du noeud source (entité de départ)
        node2 = info['node2'].replace("'", "", 2)
        # Nettoyage du type de relation
        type_val = info['type'].replace("'", "", 2)

        # Comparaison du noeud source avec l'entité et du type de relation avec la relation recherchée
        # On vérifie aussi l'absence de poids négatif (indiquant une relation négative)
        if node2 == ide and type_val == idr and "-" not in info["w"]:
            resultat = True
            break  # On arrête la boucle dès que la relation est trouvée

    # Retourne True si une relation sortante positive existe, False sinon
    return resultat

# Fonction isRelSortanteNegative(ide, idr, data)
def isRelSortanteNegative(ide, idr, data):
    """
    Vérifie si une relation sortante négative (poids négatif) existe pour une entité donnée.

    Args:
        ide (int): L'identifiant de l'entité.
        idr (int): L'identifiant de la relation.
        data (dict): Le dictionnaire contenant les données de JeuxDeMots.org.

    Returns:
        bool: True si la relation sortante négative existe, False sinon.
    """

    # Accès au dictionnaire des relations entrantes et sortantes dans les données
    jdr = data["r"]

    # Variable pour stocker le résultat
    resultat = False

    # Parcours du dictionnaire des relations
    for entity, info in jdr.items():
        # Nettoyage du noeud source (entité de départ)
        node2 = info['node2'].replace("'", "", 2)
        # Nettoyage du type de relation
        type_val = info['type'].replace("'", "", 2)

        # Comparaison du noeud source avec l'entité et du type de relation avec la relation recherchée
        # On vérifie la présence d'un poids négatif (indiquant une relation négative)
        if node2 == ide and type_val == idr and "-" in info["w"]:
            resultat = True
            break  # On arrête la boucle dès que la relation est trouvée

    # Retourne True si une relation sortante négative existe, False sinon
    return resultat

# Fonction poids(M)
def poids(M):
    """
    Extrait la valeur numérique du poids d'une relation (à partir de la chaîne de caractères).

    Args:
        M (str): La chaîne de caractères contenant le poids de la relation.

    Returns:
        int: La valeur numérique du poids (converti en entier).
    """

    # On suppose que le poids est au 3ème caractère de la chaîne
    # Conversion en entier de la sous-chaîne correspondante
    return int(M[2])

# Fonction getEntiteTransitive(data, idRelation, idMot, mot, relation)
def getEntiteTransitive(data, idRelation, idMot, mot, relation):
    """
    Recherche des entités connectées transitivement à une entité donnée par une relation spécifique.

    Args:
        data (dict): Le dictionnaire contenant les données de JeuxDeMots.org.
        idRelation (int): L'identifiant de la relation de connexion transitive.
        idMot (int): L'identifiant du mot de départ.
        mot (str): Le mot de départ (pour affichage).
        relation (str): La relation de connexion transitive (pour affichage).

    Returns:
        list: Une liste d'entités connectées transitivement, chacune représentée par une liste:
              - [0] (str): Identifiant de l'entité connectée.
              - [1] (str): Nom de l'entité connectée.
              - [2] (str): Poids de la relation empruntée pour atteindre l'entité (facultatif).
    """

    # Accès aux dictionnaires des entités et relations dans les données
    jsonDataE = data["e"]
    jsonDataR = data["r"]

    # Liste pour stocker les entités trouvées transitivement
    resultat = []

    # Parcours du dictionnaire des relations
    for relation in jsonDataR:
        # Vérification de la correspondance avec la relation recherchée et du poids positif
        if (jsonDataR[relation]['type'] == idRelation and ("-") not in jsonDataR[relation]['w']):
            # Récupération du noeud cible (entité liée)
            node2 = jsonDataR[relation]['node2']
            # Nettoyage du noeud cible
            x = node2.replace("'", "", 2)

            # Vérification du type d'entité et qu'il ne s'agisse pas du mot de départ
            if (jsonDataE[x]['type'] == '1' and x != idMot):
                # Ajout de l'entité trouvée à la liste des résultats
                resultat.append([x, jsonDataE[x]['name'], jsonDataR[relation]['w']])

    # Tri des entités trouvées par poids décroissant (entités les plus fortement reliées en premier)
    resultat = sorted(resultat, key=poids, reverse=True)

    # Si aucune entité n'est trouvée en premier passage, on recharge les données pour la relation
    # et on recommence la recherche (gestion potentielle de relations multi-sauts)
    if len(resultat) == 0:
        dataRel = getData(mot, True, relation)
        jsonDataE = dataRel["e"]
        jsonDataR = dataRel["r"]
        for relation in jsonDataR:
            if (jsonDataR[relation]['type'] == idRelation and ("-") not in jsonDataR[relation]['w']):
                node2 = jsonDataR[relation]['node2']
                x = node2.replace("'", "", 2)
                if (jsonDataE[x]['type'] == '1' and x != idMot):
                    resultat.append([x, jsonDataE[x]['name'], jsonDataR[relation]['w']])

    # Tri des entités trouvées par poids décroissant (au cas où on a rechargé les données)
    resultat = sorted(resultat, key=poids, reverse=True)

    # Retourne la liste des entités connectées transitivement
    return resultat

# Fonction getGenerique(data, idMot, mot, relation)
def getGenerique(data, idMot, mot, relation):
    """
    Recherche des entités génériques d'un mot par des relations génériques.

    Args:
        data (dict): Le dictionnaire contenant les données de JeuxDeMots.org.
        idMot (int): L'identifiant du mot de départ.
        mot (str): Le mot de départ (pour affichage).
        relation (str): La relation générique à explorer (par défaut on exclut la relation utilisée).

    Returns:
        dict: Un dictionnaire où les clés sont les noms des relations génériques explorées.
              La valeur associée à chaque clé est une liste d'entités génériques trouvées
              pour la relation correspondante (même structure que la fonction getEntiteTransitive).
    """

    # Définition d'un dictionnaire contenant des relations de généralisation par défaut
    dico_generalisation = {"r_isa": "6", "r_holo": "10"}

    # Suppression de la relation fournie en argument (si elle est présente dans le dictionnaire)
    if relation in dico_generalisation:
        del dico_generalisation[relation]

    # Dictionnaire pour stocker les entités génériques trouvées par type de relation
    resultat = {}
    # Parcours du dictionnaire des relations de généralisation restantes
    for key in dico_generalisation:
        # Recherche des entités génériques pour la relation courante
        resultat[key] = getEntiteTransitive(data, dico_generalisation[key], idMot, mot, key)

    # Retourne le dictionnaire contenant les entités génériques par type de relation
    return resultat

# Fonction getSpecifique(data, idMot, mot, relation)
def getSpecifique(data, idMot, mot, relation):
    """
    Recherche des entités spécifiques d'un mot par des relations de spécialisation.

    Args:
        data (dict): Le dictionnaire contenant les données de JeuxDeMots.org.
        idMot (int): L'identifiant du mot de départ.
        mot (str): Le mot de départ (pour affichage).
        relation (str): La relation de spécialisation à explorer (par défaut on exclut la relation utilisée).

    Returns:
        dict: Un dictionnaire où les clés sont les noms des relations de spécialisation explorées.
              La valeur associée à chaque clé est une liste d'entités spécifiques trouvées
              pour la relation correspondante (même structure que la fonction getEntiteTransitive).
    """

    # Définition d'un dictionnaire contenant des relations de spécialisation par défaut
    dico_specialisation = {"r_hypo": "8", "r_has_part": "9"}

    # Suppression de la relation fournie en argument (si elle est présente dans le dictionnaire)
    if relation in dico_specialisation:
        del dico_specialisation[relation]

    # Dictionnaire pour stocker les entités spécifiques trouvées par type de relation
    resultat = {}
    # Parcours du dictionnaire des relations de spécialisation restantes
    for key in dico_specialisation:
        # Recherche des entités spécifiques pour la relation courante
        resultat[key] = getEntiteTransitive(data, dico_specialisation[key], idMot, mot, key)

    # Retourne le dictionnaire contenant les entités spécifiques par type de relation
    return resultat
