#
# PolyAlliances
#
# Date de création: 14/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

""" Propose des fonctions liées à l'affichage """

import os
import config

try:
	import pygame
	import pygame.freetype as freetype
except ImportError:
	pass

from console import deboggue
from jeu import *


def init_gfx():
	""" Initialise Pygame et renvoie True si ce module est supporté (sinon False).
		Ne prend aucun argument. """

	try:
		pygame.init()
	except NameError:
		deboggue("Impossible d'initialiser Pygame")
		return False
	else:
		return True


def mettre_a_jour_gfx():
	""" Redessine l'affichage en renvoie True si l'opération réussie (sinon False).
		Ne prend aucun argument. """

	try:
		pygame.display.update()
	except NameError:
		deboggue("Impossible de mettre à jour l'affichage graphique")
		return False
	else:
		return True


def effacer_gfx(fenetre):
	""" Efface le contenu de la fenêtre en dessinant le fond uniformément.

		fenetre (pygame.surface.Surface): La fenêtre de jeu """
	
	fenetre.fill(config.COULEUR_FOND)


def creer_fenetre(titre, largeur, hauteur):
	""" Crée une fenêtre avec un titre et une taille définie.

		titre (str): Le titre de la fenêtre
		largeur (int): La largeur de la fenêtre en pixel
		hauteur (int): La hauteur de la fenêtre en pixel """

	fenetre = pygame.display.set_mode((largeur, hauteur))
	pygame.display.set_caption(titre)

	return fenetre


def charger_image(chemin_image):
	""" Charge et renvoie une image donnée. 

		chemin (str): Le chemin vers l'image à charger """

	try:
		image = pygame.image.load(chemin_image).convert_alpha()
	except pygame.error:
		deboggue("Impossible de charger l'image '" + chemin_image + "'")
		image = pygame.Surface(config.TAILLE_CARTE)

	return image


def redimensionner_image(image, largeur, hauteur):
	""" Renvoie l'image donnée redimensionnée.

		image (pygame.surface.Surface): L'image à redimensionner
		largeur (int): La nouvelle largeur de l'image
		hauteur (int): La nouvelle hauteur de l'image """

	return pygame.transform.smoothscale(image, (largeur, hauteur))


def charger_carte(valeur, couleur):
	""" Charge et renvoie l'image d'une carte donnée.

		valeur (str): La valeur de la carte
		couleur (str): La couleur de la carte """

	chemin = os.path.join("ressources", "images", f"{valeur}-{couleur}.png")
	return redimensionner_image(charger_image(chemin), *config.TAILLE_CARTE)


def charger_images_jeu():
	""" Renvoie une liste des images des cartes après les avoir chargées. 
		Ne prend aucun argument. """

	images = {}

	for valeur in config.VALEURS:
		for couleur in config.COULEURS:
			images[valeur, couleur] = charger_carte(valeur, couleur)

	for couleur in config.COULEUR_DOS:
		images["dos", couleur] = charger_carte("dos", couleur)

	return images


def dessiner_image(fenetre, image, x, y, centrer_x=False, centrer_y=False):
	""" Dessine une image dans la fenêtre à une position donnée.

		fenetre (pygame.surface.Surface): La fenêtre de jeu
		image (pygame.surface.Surface): L'image à afficher
		x (int): La position horizontale en pixel
		y (int): La position verticale en pixel """

	l, h = image.get_size()

	if centrer_x:
		x -= l // 2
	if centrer_y:
		y -= h // 2
		
	fenetre.blit(image, (x, y))


def dessiner_réussite(fenetre, images, reussite):
	""" Dessine les cartes de la réussite dans la fenêtre.

		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire associant une image à chaque carte
		reussite (list): La liste des cartes visibles du jeu """

	lf, hf = config.TAILLE_FENETRE
	lc, hc = config.TAILLE_CARTE

	interval_x = config.ESPACE_CARTES + lc
	interval_y = config.ESPACE_CARTES + hc

	min_x = config.ESPACE_CARTES
	min_y = config.ESPACE_CARTES
	nb_cartes_x = l // interval_x

	dessiner_image(fenetre, images["dos", "bleu"], l // 2, h - hc - config.ESPACE_CARTES, True)

	for i, carte in enumerate(reussite):
		v, c = carte["valeur"], carte["couleur"]
		dessiner_image(fenetre, images[v, c], (i % nb_cartes_x)*interval_x+min_x, (i // interval_y)*interval_y+min_y)


def creer_image_texte(texte, couleur, taille):
	""" Crée la surface représentant le texte donné avec une taille définie.

		texte (str): Le texte à créer
		couleur (tuple): La couleur du texte sous la forme (R, G, B)
		taille (int): La taille de la police en pixel """

	font_name = freetype.get_default_font()
	font = freetype.SysFont(font_name, taille)
	return font.render(texte, fgcolor=couleur)[0]


def demander_qcm_gfx(titre, *choix):
	pass