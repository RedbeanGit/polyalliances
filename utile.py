#
# PolyAlliances
#
# Date de création: 14/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

""" Apporte des fonctions utilitaires sur les fichiers et le déboggage du jeu """


import os
import sys

import config


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
		deboggue("Le dossier '{}' n'existe pas".format(chemin_dossier))
		return []


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


def arreter():
	""" Arrête le jeu sans attendre. """

	deboggue("Fin du jeu")
	sys.exit()


def chemin_valide(chemin):
	chemin = os.path.abspath(chemin)
	return os.path.exists(chemin) or os.access(os.path.dirname(chemin), os.W_OK)


def deboggue(msg):
	""" Affiche un message précédé de 'DEBUG' pour aider au développement du jeu. Cette fonction
			peut être désactivée en passant config.DEBUG à False.

		msg (str): Le message à afficher """

	if config.DEBUG:
		print("DEBUG > {}".format(msg))