#
# PolyAlliances
#
# Date de création: 14/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

""" Apporte des fonctions utilitaires sur les fichiers """


import os

from console import deboggue


def obtenir_liste_fichiers(chemin_dossier, *extensions):
	""" Renvoie la liste des fichiers contenu dans un dossier donné. Il est possible de spécifier
		l' / les extension(s) voulue(s).

		chemin_dossier (str): Le chemin vers un dossier
		extensions (*str): Les extensions autorisées (ne rien préciser pour tout autoriser) """

	if fichier_existe(chemin_dossier):
		fichiers = os.listdir(chemin_dossier)

		if extensions:
			return [fichier for fichier in fichiers if os.path.splitext(fichier)[-1][1:] in extensions]
		return fichiers
	else:
		deboggue(f"Le dossier '{chemin_dossier}' n'existe pas")


def fichier_existe(chemin_fichier):
	""" Renvoie True si le fichier existe (sinon False).

		chemin_fichier (str): Le chemin vers le fichier à tester """

	return os.path.exists(chemin_fichier)


def creer_chemin(dossier, *sous_dossiers):
	""" Créer une chaine représentant le chemin vers un fichier (ou dossier) à partir du nom des
		dossier, sous_dossiers et fichier donnés.

		dossier (str): Le dossier parent
		sous_dossiers (*str): Les sous-dossiers ou fichier """

	return os.path.join(dossier, *sous_dossiers)