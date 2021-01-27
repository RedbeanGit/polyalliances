#
# PolyAlliances
#
# Date de création: 08/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

""" Contient l'ensemble des fonctions de base du jeu. Une carte est un dictionnaire stockant une
	valeur et une couleur. """

import random
import config

from utile import *


def carte_to_chaine(carte):
	""" Renvoie une chaine de caractère représentant une carte donnée.
		
		carte (dict): La carte à représenter """
	
	return str(carte["valeur"]).rjust(2) + config.COULEURS[carte["couleur"]]


def carte_from_chaine(chaine):
	""" Renvoie une nouvelle carte à partir d'une chaine de caractère.
		(fonction auxilière)

		chaine (str): La chaine à partir de laquelle créer une carte """

	valeur, couleur = chaine.split("-")

	if valeur not in ("V", "D", "R", "A", "dos"):
		valeur = int(valeur)

	return {"valeur": valeur, "couleur": couleur}


def init_pioche_fichier(chemin_fichier):
	""" Renvoie la liste des cartes écrites dans un fichier.
		
		chemin_fichier (str): Chemin vers le fichier contenant la liste des cartes """

	deboggue("Chargement de la pioche depuis '" + chemin_fichier + "'")
	with open(chemin_fichier, "r") as fichier:
		cartes = [carte_from_chaine(chaine) for chaine in fichier.read().split() if chaine]
	return cartes


def ecrire_fichier_reussite(nom_fichier, pioche):
	""" Ecrit la pioche dans un fichier. 
		
		nom_fichier (str): Nom du fichier dans lequel écrire la pioche
		pioche (list): Liste des cartes de la pioche """

	deboggue("Sauvegarde de la pioche dans '" + nom_fichier + "'")
	with open(nom_fichier, "w") as fichier:
		for carte in pioche:
			fichier.write(str(carte['valeur'])+"-"+carte['couleur']+" ")


def genere_jeu(nb_cartes=32):
	""" Génère un jeu de cartes renvoyé sous forme d'une liste. Le jeu est trié.
		(fonction auxilière)

		nb_cartes (int): Le nombre de cartes du jeu (32 par défaut) """

	cartes = []

	for valeur in config.VALEURS:
		if valeur in "2345678910":
			valeur = int(valeur)

		for couleur in config.COULEURS:
			cartes.append({"valeur": valeur, "couleur": couleur})

			if len(cartes) == nb_cartes:
				return cartes


def init_pioche_alea(nb_cartes=32):
	""" Renvoie une liste mélangée de toutes les cartes du jeu. 
		
		nb_cartes (int): Nombre de cartes du jeu (32 par défaut) """
	
	jeu = genere_jeu(nb_cartes)
	random.shuffle(jeu)
	return jeu


def alliance(carte1, carte2):
	""" Renvoie True si les deux cartes sont de même valeur ou de même couleur (sinon False).
		
		carte1 (dict): La première carte à comparer
		carte2 (dict): La deuxième carte à comparer """

	return carte1["valeur"] == carte2["valeur"] or carte1["couleur"] == carte2["couleur"]


def saut_si_possible(liste_tas, num_tas):
	""" Si possible effectue le saut d'un tas donné et renvoie True sinon renvoie False.
		
		liste_tas (list): Liste des cartes visibles de la réussite
		num_tas (int): Numéro du tas à faire sauter (de gauche à droite en partant de 0) """
	
	if num_tas > 0 and num_tas < len(liste_tas) - 1:
		if alliance(liste_tas[num_tas-1], liste_tas[num_tas+1]):
			liste_tas.pop(num_tas-1)
		
			return True
	return False


def piocher(liste_tas, pioche):
	""" Pioche une carte et ajoute cette carte à la réussite.
		(fonction auxilière)

		liste_tas (list): Liste des cartes visibles de la réussite
		pioche (list): Liste des cartes de la pioche """

	liste_tas.append(pioche.pop())


def une_etape_reussite(liste_tas, pioche, affiche=False):
	""" Place la première carte de la pioche à la suite de la réussite et effectue les sauts
			nécessaires (la réussite peut être affichée à chaque étape).
		
		liste_tas (list): Liste des cartes visibles de la réussite
		pioche (list): Liste des cartes de la pioche
		affiche (bool): Si True, affiche la réussite après chaque changement (False par défaut) """
	
	piocher(liste_tas, pioche)

	if affiche:
		afficher_reussite(liste_tas)

	num_tas = 1

	while num_tas < len(liste_tas) - 1:
		if saut_si_possible(liste_tas, num_tas):
			if affiche:
				afficher_reussite(liste_tas)
	
			num_tas = 0
		num_tas += 1


def verifier_pioche(pioche, nb_cartes=32):
	""" Vérifie si une pioche n'est pas truquée (pas de cartes en double et nombre de cartes
			correct).

		pioche (list): La liste des cartes de la pioche
		nb_cartes (int): Le nombre de cartes du jeu (32 par défaut) """

	if len(pioche) != nb_cartes:
		return False

	pioche = pioche[:]
	testees = []

	while pioche:
		carte = pioche.pop()

		if carte in testees:
			break

		testees.append(carte)

	return len(testees) == nb_cartes


def chaine_est_pioche(chaine):
	""" Renvoie True si chaine représente une pioche sinon False.

		chaine (str): La chaine à tester """
		
	for carte in chaine.split():
		if carte:
			attr = carte.split("-")

			if len(attr) != 2:
				return False
			elif attr[0] not in config.VALEURS:
				return False
			elif attr[1] not in config.COULEURS:
				return False
	return True


def obtenir_liste_pioche():
	""" Recherche tous les fichiers susceptible de d'être une pioche dans le répertoire 
			ressources/pioches. """

	dossier_pioches = creer_chemin("ressources", "pioches")
	nom_fichiers = obtenir_liste_fichiers(dossier_pioches, "txt")
	fichiers_valides = []

	for nom_fichier in nom_fichiers:
		chemin_fichier = creer_chemin(dossier_pioches, nom_fichier)

		with open(chemin_fichier, "r") as file:
			contenu = file.read()

		if chaine_est_pioche(contenu):
			fichiers_valides.append(nom_fichier)

	return fichiers_valides