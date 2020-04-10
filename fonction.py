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
			sys.exit(1) # Arrête le programme même s'il reste des instructions à executer
		else:
			print(f"[INFO] {msg}")


def carte_to_chaine(carte):
	""" Renvoie une chaine de caractère représentant une carte donnée.
		
		carte (dict): La carte à représenter """
	pass


def afficher_reussite(reussite):
	""" Affiche les cartes de la réussite les unes à côté des autres.
		
		reussite (list): Liste contenant les cartes à afficher """
	pass


def init_pioche_fichier(chemin_fichier):
	""" Renvoie la liste des cartes écrites dans un fichier.
		
		chemin_fichier (str): Chemin vers le fichier contenant la liste des cartes """
	pass


def ecrire_fichier_reussite(nom_fichier, pioche):
	""" Ecrit la pioche dans un fichier. 
		
		nom_fichier (str): Nom du fichier dans lequel écrire la pioche
		pioche (list): Liste des cartes de la pioche """
	pass


def init_pioche_alea(nb_cartes=32):
	""" Renvoie une liste mélangée de toutes les cartes du jeu. 
		
		nb_cartes (int): Nombre de cartes du jeu (32 par défaut) """
	pass


def alliance(carte1, carte2):
	""" Renvoie True si les deux cartes sont de même valeur ou de même couleur (sinon False).
		
		carte1 (dict): La première carte à comparer
		carte2 (dict): La deuxième carte à comparer """
	pass


def saut_si_possible(liste_tas, num_tas):
	""" Si possible effectue le saut d'un tas donné et renvoie True sinon renvoie False.
		
		liste_tas (list): Liste des cartes visibles de la réussite
		num_tas (int): Numéro du tas à faire sauter (de gauche à droite en partant de 0) """
	pass


def une_etape_reussite(liste_tas, pioche, affiche=False):
	""" Place la première carte de la pioche à la suite de la réussite et effectue les sauts
		nécessaires (la réussite peut être affichée à chaque étape).
		
		liste_tas (list): Liste des cartes visibles de la réussite
		pioche (list): Liste des cartes de la pioche
		affiche (bool): Si True, affiche la réussite après chaque changement (False par défaut) """
	pass