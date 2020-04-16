#
# PolyAlliances
#
# Date de création: 16/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

""" Propose des fonctions pour interagir plus facilement avec l'utilisateur en console """

import config


def choisir_numero(mini, maxi):
	""" Renvoie un entier compris entre mini et maxi demandé au joueur.
		(fonction auxilière)

		mini (int): Entier minimal accepté
		maxi (int): Entier maximal """

	mode = input(config.NOM_JOUEUR + " > ")

	while True:
		try:
			mode = int(mode)

			if mode >= mini and mode <= maxi:
				return mode
			else:
				faire_parler(f"Vous devez entrer un entier compris entre {mini} et {maxi}.", config.NOM_ORDI)

		except ValueError:
			faire_parler(f"Vous devez entrer un entier compris entre {mini} et {maxi}.", config.NOM_ORDI)
		mode = input(config.NOM_JOUEUR + " > ")


def demander_qcm(titre, *choix):
	""" Affiche un menu avec un titre personnalisé et retourne le numéro associé au choix du joueur.
		(fonction auxilière)

		titre (str): Le titre à afficher
		choix (*str): Les options proposées au joueur """

	faire_parler(titre, config.NOM_ORDI)
	
	for i, action in enumerate(choix):
		print(f"\t{i}. {action}")
	print()

	return choisir_numero(0, len(choix)-1)


def demander_entier(titre, mini, maxi):
	""" Demande un entier à l'utilisateur compris entre min et max.

		titre (str): Le titre à afficher
		min (int): Valeur minimale acceptée
		max (int): Valeur maximale accepté """

	faire_parler(titre, config.NOM_ORDI)
	print(f"\tEntrez un entier compris entre {mini} et {maxi}")
	print()

	return choisir_numero(mini, maxi)


def demander_chaine(titre):
	""" Demande une chaine de caractère à l'utilisateur.

		titre (str): Le titre à afficher """

	faire_parler(titre, config.NOM_ORDI)
	return input(config.NOM_JOUEUR + " > ")


def faire_parler(msg, auteur):
	""" Affiche un message avec son auteur.

		msg (str): Le message à afficher
		auteur (str): L'auteur du message """

	print(auteur + " > " + msg)


def deboggue(msg):
	if config.DEBUG:
		print("DEBUG > " + msg)