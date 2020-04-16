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


def redessiner_gfx(fenetre, widgets):
	""" Redessine l'affichage.

		fenetre (pygame.surface.Surface): La fenêtre de jeu
		widgets (list): La liste des widgets à dessiner """

	fenetre.fill(config.COULEUR_FOND)
	for widget in widgets:
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

		chemin (str): Le chemin vers l'image à charger """

	try:
		image = pygame.image.load(chemin_image)
	except pygame.error:
		deboggue("Impossible de charger l'image '" + chemin_image + "'")
		image = pygame.Surface((16, 16))

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

	v, c = carte["valeur"], carte["couleur"]
	chemin_image = creer_chemin("ressources", "images", f"{v}-{c}.png")
	image = images.get(chemin_image, pygame.surface.Surface((16, 16)))

	return redimensionner_image(image.convert_alpha(), *config.TAILLE_CARTE)


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

		image (pygame.surface.Surface): L'image du widget
		x (int): La position horizontale du widget
		y (int): La position verticale du widget
		ancrage_x (float): Le décalage vers la gauche par rapport à x (0 par défaut)
		ancrage_y (float): Le décalage vers le haut par rapport à y (0 par défaut) """

	return {"image": image, "position": (x, y), "ancrage": (ancrage_x, ancrage_y)}


def dessiner_widget(fenetre, widget):
	""" Dessine une image dans la fenêtre à une position donnée.

		fenetre (pygame.surface.Surface): La fenêtre de jeu
		image (pygame.surface.Surface): L'image à afficher
		x (int): La position horizontale en pixel
		y (int): La position verticale en pixel """

	image = widget["image"]
	ax, ay = widget["ancrage"]
	x, y = widget["position"]
	l, h = image.get_size()

	x -= int(ax * l)
	y -= int(ay * h)
		
	fenetre.blit(image, (x, y))


def creer_widgets_reussite(images, liste_tas):
	""" Crée et renvoie une liste de widgets correspondant aux cartes de la réussite.

		images (dict): Le dictionnaire des images chargées
		liste_tas (list): Liste des cartes visibles de la réussite """

	widgets = []

	lf, hf = config.TAILLE_FENETRE
	lc, hc = config.TAILLE_CARTE
	lm, hm = config.MARGES
	lv, hv = config.MAX_CARTE_VISIBLE

	carte = {"valeur": "dos", "couleur": "bleu"}
	image = obtenir_image_carte(images, carte)
	widgets.append(creer_widget(image, lf // 2, hf - hm, 0.5, 1))

	inter_x = (lf - lm) // (lv + 1)
	inter_y = (hf - hm) // (hv + 1)

	for i, carte in enumerate(liste_tas):
		image = obtenir_image_carte(images, carte)
		x = int(lm + inter_x * (i % lv + 1))
		y = int(hm + inter_y * (i // lv + 1))
		widgets.append(creer_widget(image, x, y, 0.5, 0.5))

	return widgets


def creer_widgets_qcm(titre, *choix):
	""" Crée et renvoie une liste de widgets proposant plusieurs choix à l'utilisateur.

		titre (str): Le titre du QCM
		choix (*str): Les options du QCM """

	widgets = []

	lf, hf = config.TAILLE_FENETRE
	lm, hm = config.MARGES
	couleur = config.COULEUR_TEXTE

	image = creer_image_texte(titre, couleur, 30)
	widgets.append(creer_widget(image, lf // 2, hm, 0.5))

	min_y = hf // 2 - len(choix) * 21

	for i, option in enumerate(choix):
		image = creer_image_texte(option, couleur, 24)
		widgets.append(creer_widget(image, lf // 2, min_y + i * 42, 0.5, 0.5))

	return widgets