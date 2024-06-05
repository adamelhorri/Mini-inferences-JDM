from dataHandling import *
from dataSaving import *
    # TRANSITIVITE
def transitive(data, dataEnt, idMot, idEntite, idRelation, mot, relation, entite, cpt=1):
  """
    Vérifie la transitivité d'une relation sémantique.

  Args:
      data (dict): Le dictionnaire contenant les données de JeuxDeMots.org.
      dataEnt (dict): Un dictionnaire contenant des entités. (structure supposée)
      idMot (int): L'identifiant du mot de départ.
      idEntite (int): L'identifiant de l'entité de départ.
      idRelation (int): L'identifiant de la relation sémantique à tester.
      mot (str): Le mot de départ.
      relation (str): La relation sémantique à tester (en français).
      entite (str): L'entité finale à atteindre.
      cpt (int, optional): Profondeur de la recherche transitive (défaut 1).

  Returns:
      str: Message de résultat indiquant si la relation est transitive ou non.
  """

  # Recherche des entités connectées transitivement à partir du mot et de la relation
  idCommuns = getEntiteTransitive(data, idRelation, idMot, mot, relation)  # on suppose getEntiteTransitive dans dataHandling.py
  message = ""

  # Parcours des entités connectées transitivement
  for idCommun in idCommuns:
    # Vérification si la relation existe entre l'entité intermédiaire et l'entité finale
    isRelE = isRelationEntrante(idCommun[0], idRelation, dataEnt)  # on suppose isRelationEntrante dans dataHandling.py
    if cpt > 0:  # Gestion de la profondeur de recherche
      if isRelE[0]:  # Vérification si la relation est entrante et son poids est positif
        if "-" not in isRelE[1]:
          message += f"Vrai : {mot} {relation} {idCommun[1].replace('*', '')} (W : {idCommun[2].replace('*', '')})\n"
          message += f"et {idCommun[1].replace('*', '')} {relation} {entite} (W : {isRelE[1].replace('*', '')})\n"
          print(f"Vrai : {mot} {relation} {idCommun[1].replace('*', '')} (W : {idCommun[2].replace('*', '')})")
          print(f"et {idCommun[1].replace('*', '')} {relation} {entite} (W : {isRelE[1].replace('*', '')})")
          cpt -= 1
      else:
        message += f"Faux : {mot} {relation} {idCommun[1].replace('*', '')}\n"
        message += f"et {idCommun[1].replace('*', '')} {relation} {entite} est faux (W : {isRelE[1].replace('*', '')})\n"
        print(f"Faux : {mot} {relation} {idCommun[1].replace('*', '')}")
        print(f"et {idCommun[1].replace('*', '')} {relation} {entite} est faux (W : {isRelE[1].replace('*', '')})")
        cpt -= 1

  return message

#DEDUCTION
def deduction(data, dataEnt, idMot, idEntite, idRelation, mot, relation, entite, cpt=1):
    
    idCommuns = getGenerique(data, idMot,mot,relation)
    msg=""
    '''
    Vérifie si une relation peut être déduite par des relations génériques (hyperonymes).

  Args:
      data (dict): Le dictionnaire contenant les données de JeuxDeMots.org.
      dataEnt (dict): Un dictionnaire contenant des entités. (structure supposée)
      idMot (int): L'identifiant du mot de départ.
      idEntite (int): L'identifiant de l'entité de départ.
      idRelation (int): L'identifiant de la relation sémantique à tester.
      mot (str): Le mot de départ.
      relation (str): La relation sémantique à tester (en français).
      entite (str): L'entité finale à atteindre.
      cpt (int, optional): Profondeur de la recherche transitive (défaut 1).

  Returns:
      str: Message de résultat indiquant si la relation peut être déduite ou non.
    '''
    for idCommun in idCommuns:
        for entity in idCommuns[idCommun]:

            if cpt > 0:
                teste = isRelationEntrante(entity[0], idRelation, dataEnt)
                isRelE = teste[0]

                if isRelE:
                    if "-" not in teste[1]:
                        msg += "Vrai : " + mot + " " + idCommun + " " + entity[1].replace("'", "")+" (W : "+entity[2].replace("'", "")+")\n"
                        msg += "et " + entity[1].replace("'", "") + " " + relation + " " + entite + "(W : "+teste[1].replace("'", "")+"\n"
                        print("Vrai : " + mot + " " + idCommun + " " + entity[1].replace("'", "")+" (W : "+entity[2].replace("'", "")+")")
                        print("et " + entity[1].replace("'", "") + " " + relation + " " + entite + "(W : "+teste[1].replace("'", "")+")")
                        cpt -= 1
                    else:

                        msg+="Faux : " + mot + " " + idCommun + " " + entity[1].replace("'", "")+"\n"
                        msg+="et " + entity[1].replace("'", "") + " " + relation + " " + entite + " est faux" + "(W : "+teste[1].replace("'", "")+")\n"
                        print("Faux : " + mot + " " + idCommun + " " + entity[1].replace("'", ""))
                        print("et " + entity[1].replace("'", "") + " " + relation + " " + entite + " est faux" + "(W : "+teste[1].replace("'", "")+")")
                        cpt = cpt - 1
    return msg
#INDUCTION
def induction(data, dataEnt, idMot, idEntite, idRelation, mot, relation, entite, cpt=1):
  """
    Vérifie si une relation peut être induite par des relations hyponymes (spécifiques).

  Args:
      data (dict): Le dictionnaire contenant les données de JeuxDeMots.org.
      dataEnt (dict): Un dictionnaire contenant des entités. (structure supposée)
      idMot (int): L'identifiant du mot de départ.
      idEntite (int): L'identifiant de l'entité de départ.
      idRelation (int): L'identifiant de la relation sémantique à tester.
      mot (str): Le mot de départ.
      relation (str): La relation sémantique à tester (en français).
      entite (str): L'entité finale à atteindre.
      cpt (int, optional): Profondeur de la recherche transitive (défaut 1).

  Returns:
      str: Message de résultat indiquant si la relation peut être induite ou non.
  """

  # Initialisation
  msg = ""  # Chaîne de caractères pour stocker les messages de résultat
  negative = 0  # Compteur pour suivre le nombre d'hyponymes non vérifiés
  idCommuns = getSpecifique(data, idMot, mot, relation)  # On suppose getSpecifique dans dataHandling.py (fournit les hyponymes)

  # Parcours des hyponymes trouvés
  for idCommun in idCommuns:
    for entity in idCommuns[idCommun]:
      if cpt > 0:  # Vérification de la profondeur de recherche
        teste = isRelationEntrante(entity[0], idRelation, dataEnt)  # Vérifie la relation entre entité et entité finale (supposé de dataHandling.py)
        isRelE = teste[0]

        if isRelE:  # Si la relation existe entre l'entité et l'entité finale
          if "-" not in teste[1]:  # Vérification du poids de la relation (positif)
            msg += f"Vrai car : {mot} {idCommun} {entity[1].replace('*', '')} (Poids : {entity[2].replace('*', '')})\n"
            msg += f"et {entity[1].replace('*', '')} {relation} {entite} (W : {teste[1].replace('*', '')})\n"
            print(f"Vrai car : {mot} {idCommun} {entity[1].replace('*', '')} (Poids : {entity[2].replace('*', '')})")
            print(f"et {entity[1].replace('*', '')} {relation} {entite} (W : {teste[1].replace('*', '')})")
            cpt -= 1
          else:
            negative += 1  # On compte si la relation n'est pas vérifiée

        # Vérification si tous les hyponymes ont été testés et aucun n'est vérifié
        if negative == len(idCommuns):
          msg += f"Faux car : {mot} {idCommun} {entity[1].replace('*', '')}\n"
          msg += f"et {entity[1].replace('*', '')} {relation} {entite} est faux\n"
          print(f"Faux car : {mot} {idCommun} {entity[1].replace('*', '')}")
          print(f"et {entity[1].replace('*', '')} {relation} {entite} est faux")
          cpt -= 1

  return msg

