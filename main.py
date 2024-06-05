import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from dataSaving import *
from dataHandling import *
from operators import *

def chercher_preuve(mot, relation, entite):
    """
    Fonction principale pour rechercher des preuves de relations sémantiques entre des entités.

    Args:
        mot (str): Le mot de départ.
        relation (str): La relation sémantique à tester (en français).
        entite (str): L'entité finale à atteindre.

    Returns:
        str: Message de résultat indiquant les preuves trouvées pour chaque type de relation (transitive, déduction, induction).
    """

    # Création des fichiers texte et JSON pour le mot et l'entité
    createTxt(mot, True, "")
    createJSON(mot, True, "")
    data = getData(mot, True, "")

    # Récupération des identifiants du mot et de l'entité
    infos = idEntite(mot, entite, data)
    idEntite_result = infos["idEntite"]  # Renommage pour éviter le conflit
    idMot = infos["idMot"]

    # Variable pour stocker le message de résultat
    message = ""

    # Vérification si l'entité a été trouvée
    if idEntite_result != "null":
        # Récupération de l'identifiant de la relation
        idRelation_result = idRelation(relation, data)  # Renommage pour éviter le conflit

        # Création des fichiers texte et JSON pour l'entité
        createTxt(entite, False, "")
        createJSON(entite, False, "")
        dataEnt = getData(entite, False, "")

        # Liste des relations transitives
        relationTransitive = ["r_lieu", "r_lieu-1", "r_isa", "r_holo", "r_hypo", "r_has_part",
                             "r_own", "r_own-1", "r_product_of", "r_similar"]

        # **Transitivité**
        message += "## TRANSITIVITE :\n"
        print("TRANSITIVITE :")

        if relation in relationTransitive:
            trmsg = transitive(data, dataEnt, idMot, idEntite_result, idRelation_result, mot, relation, entite)
            if trmsg == "":
                message += "Il n'y a pas de preuve\n"
                print("Il n'y a pas de preuve")
            else:
                message += trmsg
        else:
            message += "La relation n'est pas transitive\n"
            print("La relation n'est pas transitive")

        # **Déduction**
        message += "## DEDUCTION :\n"
        print("DEDUCTION :")

        msgded = deduction(data, dataEnt, idMot, idEntite_result, idRelation_result, mot, relation, entite)
        if msgded == "":
            message += "il n'y a pas de preuve\n"
            print("il n'y a pas de preuve")
        else:
            message += msgded

        # **Induction**
        message += "## INDUCTION :\n"
        print("INDUCTION :")

        msgind = induction(data, dataEnt, idMot, idEntite_result, idRelation_result, mot, relation, entite)
        if msgind == "":
            message += "il n'y a pas de preuve\n"
            print("il n'y a pas de preuve")
        else:
            message += msgind

        # **Essai en inversant la relation**
        message += "## Essai en inversant la relation : :\n"
        print("Essai en inversant la relation :")

        relation_reversed = relation + "-1"

        if idEntite_result != "null":
            idRelation_reversed = idRelation(relation_reversed, data)
            createTxt(entite, False, "")
            createJSON(entite, False, "")
            dataEnt = getData(entite, False, "")

            message += "## TRANSITIVITE :\n"
            print("TRANSITIVITE :")

            if relation in relationTransitive:
                trmsg = transitive(data, dataEnt, idMot, idEntite_result, idRelation_reversed, mot, relation, entite)
                if trmsg == "":
                    message += "Il n'y a pas de preuve\n"
                    print("Il n'y a pas de preuve")
                else:
                    message += trmsg
            else:
                message += "La relation n'est pas transitive\n"
                print("La relation n'est pas transitive")

            message += "## DEDUCTION :\n"
            print("DEDUCTION :")

            msgded = deduction(data, dataEnt, idMot, idEntite_result, idRelation_reversed, mot, relation, entite)
            if msgded == "":
                message += "il n'y a pas de preuve\n"
                print("il n'y a pas de preuve")
            else:
                message += msgded

            message += "## INDUCTION :\n"
            print("INDUCTION :")

            msgind = induction(data, dataEnt, idMot, idEntite_result, idRelation_reversed, mot, relation, entite)
            if msgind == "":
                message += "il n'y a pas de preuve\n"
                print("il n'y a pas de preuve")
            else:
                message += msgind

    print(message)

# Exemples de test
exemples = [
    ("panda", "r_carac", "carnivore"),
    ("pigeon", "r_agent-1", "pondre"),
    ("couper", "r_patient", "pain"),
    ("cuire", "r_patient", "steak"),
    ("découper", "r_patient", "poulet"),
    ("Airbus A380", "r_agent-1", "atterrir"),
    ("chat", "r_agent-1", "miauler"),
    ("serveuse", "r_agent-1", "apporter à boire")
]

# Exécution de la fonction pour chaque exemple
for exemple in exemples:
    print(*exemple)
    resultat = chercher_preuve(*exemple)
    print("****************************************")
