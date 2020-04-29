#
# PolyAlliances
#
# Date de création: 16/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

""" Propose des fonctions pour interagir plus facilement avec l'utilisateur en console """

import config

from jeu import *
from utile import *


def afficher_reussite(reussite):
	""" Affiche les cartes de la réussite les unes à côté des autres.
		
		reussite (list): Liste contenant les cartes à afficher """

	print(*map(carte_to_chaine, reussite))
	print()


def demander_qcm(titre, *choix):
	""" Affiche un menu avec un titre personnalisé et retourne le numéro associé au choix du joueur.
		(fonction auxilière)

		titre (str): Le titre à afficher
		choix (*str): Les options proposées au joueur """

	dire(titre)
	
	for i, action in enumerate(choix):
		print("\t{}. {}".format(i, action))
	print()

	entree = demander()

	while not nombre_valide(entree, 0, len(choix)-1):
		dire("Vous devez entrer un entier compris entre {} et {}.".format(0, len(choix)-1))
		entree = demander()

	return int(entree)


def demander_entier(titre, mini, maxi):
	""" Demande un entier à l'utilisateur compris entre min et max.

		titre (str): Le titre à afficher
		min (int): Valeur minimale acceptée
		max (int): Valeur maximale accepté """

	dire(titre)
	print("\tEntrez un entier compris entre {} et {}".format(mini, maxi))
	print()

	entree = demander()

	while not nombre_valide(entree, mini, maxi):
		dire("Vous devez entrer un entier compris entre {} et {}.".format(mini, maxi))
		entree = demander()

	return int(entree)


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