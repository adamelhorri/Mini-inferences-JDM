# Importation des bibliothèques nécessaires
from bs4 import BeautifulSoup as bs  # BeautifulSoup pour parser le HTML
import requests  # Bibliothèque pour effectuer des requêtes HTTP
import time  # Bibliothèque pour gérer les délais

# Fonction getFromURL(mot, entrant, relation)
def getFromURL(mot, entrant, relation):
    """
     Récupère des données du site JeuxDeMots.org en fonction d'un mot,
     d'une direction relationnelle (entrant ou sortant) et d'une relation spécifique.

    Args:
        mot (str): Le mot pour lequel on recherche des relations.
        entrant (bool): Indique si on recherche des relations entrantes (True) ou sortantes (False).!!!
        relation (str): La relation sémantique spécifique à rechercher (par exemple, "r_lieu").

    Returns:
        list | None: Une liste d'éléments de code HTML contenant les données récupérées,
                     ou None si la récupération échoue après plusieurs tentatives.
    """

    # URL de base pour accéder aux données de JeuxDeMots.org
    url = 'http://www.jeuxdemots.org/rezo-dump.php?'

    # Création d'une session pour gérer les requêtes HTTP
    session = requests.Session()

    # Préparation des paramètres de la requête HTTP en fonction de la direction relationnelle
    if entrant:
        payload = {
            'gotermsubmit': 'Chercher',  # Paramètre de soumission du formulaire
            'gotermrel': mot,           # Le mot pour lequel on recherche des relations
            'relation': relation,       # La relation sémantique spécifique
            'relin': 'norelout'          # Récupérer uniquement les relations entrantes
        }
    else:
        payload = {
            'gotermsubmit': 'Chercher',
            'gotermrel': mot,
            'relation': relation,
            'relout': 'norelin'          # Récupérer uniquement les relations sortantes
        }

    # Nombre maximum de tentatives en cas d'erreurs réseau
    retries = 5

    # Boucle for pour effectuer les tentatives de récupération avec gestion d'erreurs
    for attempt in range(retries):
        try:
            # Envoi d'une requête GET à l'URL construite avec les paramètres
            response = session.get(url, params=payload)

            # Lever une exception si le code de réponse HTTP indique une erreur
            response.raise_for_status()

            # Parser la réponse HTML avec BeautifulSoup
            soup = bs(response.text, 'html.parser')

            # Récupérer les éléments de code HTML contenant les données
            prod = soup.find_all('code')

            # Vérification de la présence d'un message d'erreur
            if "MUTED_PLEASE_RESEND" not in str(prod):
                # Données récupérées avec succès, on renvoie la liste d'éléments de code
                return prod

        except requests.exceptions.RequestException as e:
            # Impression d'un message d'erreur en cas d'exception
            print("Échec de la requête:", e)

            # Délai exponentiel avant la prochaine tentative (gestion des erreurs temporaires)
            delay = 2**attempt
            time.sleep(delay)

    # Retourne None si toutes les tentatives échouent
    return None
