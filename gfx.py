#
# PolyAlliances
#
# Date de création: 14/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

""" Propose des fonctions liées à l'affichage. Un widget est un dictionnaire stockant une image,
	une position et un point d'ancrage. """

import os
import config

try:
	import pygame
	import pygame.freetype as freetype
except ImportError:
	pass

from evenement import *
from jeu import *
from utile import *


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


def redessiner_gfx(fenetre, activite):
	""" Redessine l'affichage.

		fenetre (pygame.Surface): La fenêtre de jeu
		activite (dict): L'activite à dessiner """

	fenetre.fill(config.COULEUR_FOND)
	for widget in activite["widgets"]:
		dessiner_widget(fenetre, widget)

	pygame.display.update()


def creer_fenetre(titre, largeur, hauteur):
	""" Crée une fenêtre avec un titre et une taille définie. Ne fonctionne que si Pygame a été
			initialisé.

		titre (str): Le titre de la fenêtre
		largeur (int): La largeur de la fenêtre en pixel
		hauteur (int): La hauteur de la fenêtre en pixel """

	fenetre = pygame.display.set_mode((largeur, hauteur))
	definir_titre(titre)

	return fenetre


def definir_titre(titre):
	""" Change le titre de la fenêtre. Ne fonctionne que si Pygame a été initialisé.

		titre (str): Le nouveau de titre """

	pygame.display.set_caption(titre)


def charger_image(chemin_image):
	""" Charge et renvoie une image donnée. Si le chargement échoue, une image noire de 16x16p
			est renvoyée.

		chemin_image (str): Le chemin vers l'image à charger """

	try:
		image = pygame.image.load(chemin_image)
	except pygame.error:
		deboggue("Impossible de charger l'image '" + chemin_image + "'")
		image = creer_image(16, 16, (0, 0, 0))

	return image


def charger_images_jeu():
	""" Renvoie une liste des images des cartes après les avoir chargées. 
		Ne prend aucun argument. """

	images = {}
	dossier_images = creer_chemin("ressources", "images")
	image_noms = obtenir_liste_fichiers(dossier_images, "png")

	for image_nom in image_noms:
		chemin_image = creer_chemin(dossier_images, image_nom)
		images[chemin_image] = charger_image(chemin_image)

	return images


def redimensionner_image(image, largeur, hauteur):
	""" Renvoie l'image donnée redimensionnée. Ne fonctionne que si Pygame a été initialisé.

		image (pygame.surface.Surface): L'image à redimensionner
		largeur (int): La nouvelle largeur de l'image
		hauteur (int): La nouvelle hauteur de l'image """

	return pygame.transform.smoothscale(image, (largeur, hauteur))


def obtenir_image_carte(images, carte):
	""" Renvoie l'image d'une carte donnée. Ne fonctionne que si Pygame a été initialisé.

		images (dict): Le dictionnaire des images chargées
		carte (dict): La carte dont on veut obtenir l'image """

	v, c = str(carte["valeur"]), carte["couleur"]
	chemin_image = creer_chemin("ressources", "images", v+"-"+c+".png")
	image = images.get(chemin_image, pygame.surface.Surface((16, 16)))

	return redimensionner_image(image.convert_alpha(), *config.TAILLE_CARTE)


def creer_image(largeur, hauteur, couleur):
	""" Renvoie une surface unicolore d'une taille définie.

		largeur (int): La largeur de l'image
		hauteur (int): La hauteur de l'image
		couleur (tuple): La couleur de l'image sous la forme (R, G, B) """

	image = pygame.Surface((largeur, hauteur))
	image.fill(couleur)

	return image


def creer_image_texte(texte, couleur, taille):
	""" Crée la surface représentant le texte donné avec une taille définie.

		texte (str): Le texte à créer
		couleur (tuple): La couleur du texte sous la forme (R, G, B)
		taille (int): La taille de la police en pixel """

	font_name = freetype.get_default_font()
	font = freetype.SysFont(font_name, taille)
	return font.render(texte, fgcolor=couleur)[0]


def creer_widget(image, x, y, ancrage_x=0, ancrage_y=0):
	""" Crée et renvoie un widget. Cet objet stocke une image, sa position et un point d'ancrage.
			(0,0) représente le coin supérieur gauche et (1,1) le coin inférieur droit.

		image (pygame.Surface): L'image du widget
		x (int): La position horizontale du widget
		y (int): La position verticale du widget
		ancrage_x (float): Le décalage vers la gauche par rapport à x (0 par défaut)
		ancrage_y (float): Le décalage vers le haut par rapport à y (0 par défaut) """

	return {"image": image, "position": (x, y), "ancrage": (ancrage_x, ancrage_y)}


def dessiner_widget(fenetre, widget):
	""" Dessine une image dans la fenêtre à une position donnée.

		fenetre (pygame.Surface): La fenêtre de jeu
		image (pygame.Surface): L'image à afficher
		x (int): La position horizontale en pixel
		y (int): La position verticale en pixel """

	image = widget["image"]
	ax, ay = widget["ancrage"]
	x, y = widget["position"]
	l, h = image.get_size()

	x -= int(ax * l)
	y -= int(ay * h)
		
	fenetre.blit(image, (x, y))