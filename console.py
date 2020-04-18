#
# PolyAlliances
#
# Date de création: 16/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

""" Propose des fonctions pour interagir plus facilement avec l'utilisateur en console """

import config

from utile import *


def choisir_numero(mini, maxi):
	""" Renvoie un entier compris entre mini et maxi demandé au joueur.
		(fonction auxilière)

		mini (int): Entier minimal accepté
		maxi (int): Entier maximal """

	mode = demander()

	while True:
		try:
			mode = int(mode)

			if mode >= mini and mode <= maxi:
				return mode
			else:
				dire(f"Vous devez entrer un entier compris entre {mini} et {maxi}.")

		except ValueError:
			dire(f"Vous devez entrer un entier compris entre {mini} et {maxi}.")
		mode = demander()


def demander_qcm(titre, *choix):
	""" Affiche un menu avec un titre personnalisé et retourne le numéro associé au choix du joueur.
		(fonction auxilière)

		titre (str): Le titre à afficher
		choix (*str): Les options proposées au joueur """

	dire(titre)
	
	for i, action in enumerate(choix):
		print(f"\t{i}. {action}")
	print()

	return choisir_numero(0, len(choix)-1)


def demander_entier(titre, mini, maxi):
	""" Demande un entier à l'utilisateur compris entre min et max.

		titre (str): Le titre à afficher
		min (int): Valeur minimale acceptée
		max (int): Valeur maximale accepté """

	dire(titre)
	print(f"\tEntrez un entier compris entre {mini} et {maxi}")
	print()

	return choisir_numero(mini, maxi)


def demander_chaine(titre):
	""" Demande une chaine de caractère à l'utilisateur.

		titre (str): Le titre à afficher """

	dire(titre)
	return demander()


def demander_fichier(titre, existe=True):
	""" Demande le chemin vers un fichier. Il est possible de forcer le joueur à entrer un chemin
			existant.

		titre (str): Le chemin"""

	dire(titre)
	chemin = demander()

	if existe:
		while not fichier_existe(chemin):
			dire("Le chemin spécifié est invalide")
			chemin = demander()
	else:
		while not chemin_valide(chemin):
			dire("Le chemin spécifié est invalide")
			chemin = demander()

	return chemin


def dire(msg):
	""" Affiche un message avec son auteur.

		msg (str): Le message à afficher """

	print(config.NOM_ORDI + " > " + msg)


def demander():
	try:
		return input(config.NOM_JOUEUR + " > ")
	except KeyboardInterrupt:
		deboggue("Arrêt par Ctrl+C du jeu")
		arreter()