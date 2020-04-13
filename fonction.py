#
# PolyAlliances
#
# Date de création: 08/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

""" Contient l'ensemble des fonctions de base du jeu """

import random
import config


def carte_to_chaine(carte):
	""" Renvoie une chaine de caractère représentant une carte donnée.
		
		carte (dict): La carte à représenter """
	
	return str(carte["valeur"]).rjust(2) + config.COULEURS[carte["couleur"]]


def carte_from_chaine(chaine):
	""" Renvoie une nouvelle carte à partir d'une chaine de caractère.
		(fonction auxilière)

		chaine (str): La chaine à partir de laquelle créer une carte """

	valeur, couleur = chaine.split("-")

	if valeur not in ("V", "D", "R", "A"):
		valeur = int(valeur)

	return {"valeur": valeur, "couleur": couleur}


def afficher_reussite(reussite):
	""" Affiche les cartes de la réussite les unes à côté des autres.
		
		reussite (list): Liste contenant les cartes à afficher """
	
	print(*map(carte_to_chaine, reussite))


def init_pioche_fichier(chemin_fichier):
	""" Renvoie la liste des cartes écrites dans un fichier.
		
		chemin_fichier (str): Chemin vers le fichier contenant la liste des cartes """
	
	with open(chemin_fichier, "r") as fichier:
		cartes = [carte_from_chaine(chaine) for chaine in fichier.read().split() if chaine]
	return cartes


def ecrire_fichier_reussite(nom_fichier, pioche):
	""" Ecrit la pioche dans un fichier. 
		
		nom_fichier (str): Nom du fichier dans lequel écrire la pioche
		pioche (list): Liste des cartes de la pioche """

	with open(nom_fichier, "w") as fichier:
		for carte in pioche:
			fichier.write(f"{carte['valeur']}-{carte['couleur']} ")


def genere_jeu(nb_cartes=32):
	""" Génère un jeu de cartes renvoyé sous forme d'une liste. Le jeu est trié.
		(fonction auxilière)

		nb_cartes (int): Le nombre de cartes du jeu (32 par défaut) """

	cartes = []

	for valeur in config.VALEURS:
		for couleur in config.COULEURS:
			cartes.append({"valeur": valeur, "couleur": couleur})

			if len(cartes) == nb_cartes:
				break

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


def choisir_numero(mini, maxi):
	""" Renvoie un entier compris entre mini et maxi demandé au joueur.
		(fonction auxilière)

		mini (int): Entier minimal accepté
		maxi (int): Entier maximal """

	mode = input("> ")

	while True:
		try:
			mode = int(mode)

			if mode >= mini and mode <= maxi:
				return mode
			else:
				print(f"Choix invalide, vous devez entrer un entier compris entre {mini} et {maxi}.")

		except ValueError:
			print(f"Choix invalide, vous devez entrer un entier compris entre {mini} et {maxi}.")
		mode = input("> ")


def afficher_menu(titre, *choix):
	""" Affiche un menu avec un titre personnalisé et retourne le numéro associé au choix du joueur.
		(fonction auxilière)

		titre (str): Le titre à afficher
		choix (*str): Les options proposées au joueur """

	print(titre)
	
	for i, action in enumerate(choix):
		print(f"{i+1}. {action}")

	return choisir_numero(1, len(choix))