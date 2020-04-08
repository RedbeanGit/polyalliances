#
# PolyAlliances
#
# Date de création: 08/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

""" Contient l'ensemble des fonctions de base du jeu """

import sys
import config


def deboggue(msg, erreur=False):
	""" Affiche un message en console et arrête le programme en cas de problème.
		msg (str): Le message a afficher
		erreur (bool) [optionnel]: Si True arrête le jeu après avoir affiche le message. False par defaut """
		
	if config.DEBUG:
		if erreur:
			print(f"[ERREUR] {msg}")
			sys.exit(1)
		else:
			print(f"[INFO] {msg}")