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

from evenement import *
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


def creer_widgets_reussite(images, liste_tas, fonction=None):
	""" Crée et renvoie une liste de widgets correspondant aux cartes de la réussite, ainsi que
			leur action associée. Laissez 'fonction' à None pour empecher l'utilisateur d'interagir
			avec la partie.

		images (dict): Le dictionnaire des images chargées
		liste_tas (list): Liste des cartes visibles de la réussite
		fonction (function, method): La fonction à executer lors d'un clic sur une carte """

	widgets = []
	actions = []

	def quand_clic(evenememt, carte_id):
		if fonction:
			fonction(carte_id)

	def quand_survol(evenement, carte_id):
		pass

	lf, hf = config.TAILLE_FENETRE
	lc, hc = config.TAILLE_CARTE
	lm, hm = config.MARGES
	lv, hv = config.MAX_CARTE_VISIBLE

	carte = {"valeur": "dos", "couleur": "bleu"}
	image = obtenir_image_carte(images, carte)

	widget = creer_widget(image, lf // 2, hf - hm, 0.5, 1)
	widgets.append(widget)
	
	action = creer_action("clic", quand_clic, 0, widget=widget)
	actions.append(action)

	inter_x = (lf - lm) // (lv + 1)
	inter_y = (hf - hm) // (hv + 1)

	for i, carte in enumerate(liste_tas):
		x = int(lm + inter_x * (i % lv + 1))
		y = int(hm + inter_y * (i // lv + 1))

		image = obtenir_image_carte(images, carte)
		
		widget = creer_widget(image, x, y, 0.5, 0.5)
		widgets.append(widget)

		if i > 0 and i < len(liste_tas) - 1:
			action = creer_action("clic", quand_clic, i, widget=widget)
			actions.append(action)
			action = creer_action("survol", quand_survol, i, widget=widget)
			actions.append(action)

	return widgets, actions


def creer_widgets_qcm(titre, fonction, *choix):
	""" Crée et renvoie une liste de widgets ainsi que leur action associée en proposant plusieurs
			choix à l'utilisateur.

		titre (str): Le titre du QCM
		fonction (function, method): La fonction à executer une fois une option choisie
		choix (*str): Les options du QCM """

	def quand_clic(evenememt, widget_id):
		fonction(widget_id)

	widgets = []
	actions = []

	lf, hf = config.TAILLE_FENETRE
	couleur = config.COULEUR_TEXTE

	min_y = hf // 2 - len(choix) * 20

	image = creer_image_texte(titre, couleur, 30)
	widgets.append(creer_widget(image, lf // 2, min_y - 75, 0.5, 0.5))

	for i, option in enumerate(choix):
		image = creer_image_texte(option, couleur, 22)
		widget = creer_widget(image, lf // 2, min_y + i * 40, 0.5, 0.5)
		action = creer_action("clic", quand_clic, i, widget=widget)

		widgets.append(widget)
		actions.append(action)

	return widgets, actions


def creer_widgets_input(titre, fonction, fct_change, type_accepte=str, texte=""):
	""" Crée et renvoie une liste de widgets ainsi que leur action associée en proposant au joueur
			de taper au clavier.

		titre (str): Le message à afficher
		fonction (function, method): La fonction à executer une fois la touche entrée pressée
		fct_change (function, method): La fonction à executer à chaque changement du texte
		type_accepte (type): Le type d'entrée attendue (str par défaut)
		texte (str): Le texte déjà tapé ('' par défaut) """

	def quand_appui(evenement):
		if evenement.key == pygame.K_RETURN:
			try:
				entree = type_accepte(texte)
			except ValueError:
				fct_change(None)
			else:
				fonction(entree)
		elif evenement.key == pygame.K_BACKSPACE:
			fct_change(texte[:-1])
		else:
			fct_change(texte + evenement.unicode)

	widgets = []
	actions = []

	lf, hf = config.TAILLE_FENETRE
	couleur = config.COULEUR_TEXTE

	min_y = hf // 2 - 20

	image = creer_image_texte(titre, couleur, 30)
	widget = creer_widget(image, lf // 2, min_y - 75, 0.5, 1)
	widgets.append(widget)

	if texte == None:
		texte = ""
		image = creer_image_texte("Entrée invalide", config.COULEUR_TEXTE, 18)
		widget = creer_widget(image, lf // 2, min_y - 70, 0.5)
		widgets.append(widget)

	if texte:
		image = creer_image_texte(texte, couleur, 22)
	else:
		image = creer_image_texte("Tapez maintenant", couleur, 22)

	widget = creer_widget(image, lf // 2, min_y, 0.5, 0.5)
	widgets.append(widget)

	action = creer_action("appui", quand_appui)
	actions.append(action)

	return widgets, actions


def creer_widgets_input_fichier(titre, fonction, fct_change, texte="", existe=True):
	""" Crée et renvoie une liste de widgets ainsi que leur action associée en proposant au joueur
			d'entrer le chemin vers un fichier ou de glisser déposer.

		titre (str): Le message à afficher
		fonction (function, method): La fonction à executer une fois la touche entrée pressée
		fct_change (function, method): La fonction à executer à chaque changement du texte
		texte (str): Le texte déjà tapé ('' par défaut)
		existe (bool): Si True, execute 'fonction' uniquement si le fichier existe """

	def quand_drop(evenement):
		fonction(evenement.file)

	def quand_valide(chemin):
		if not existe or fichier_existe(chemin):
			fonction(chemin)
		else:
			fct_change(None)

	lf, hf = config.TAILLE_FENETRE
	min_y = hf // 2 - 20
	widget = None

	if texte == None:
		texte = ""
		image = creer_image_texte("Chemin invalide", config.COULEUR_TEXTE, 18)
		widget = creer_widget(image, lf // 2, min_y - 70, 0.5)

	widgets, actions = creer_widgets_input(titre, quand_valide, fct_change, texte=texte)

	if widget:
		widgets.append(widget)

	action = creer_action("drop", quand_drop)
	actions.append(action)

	return widgets, actions