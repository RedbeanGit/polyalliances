#
# PolyAlliances
#
# Date de création: 08/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

""" Script principal du jeu """

import config
import time

from gfx import *
from console import *
from jeu import *


def reussite_mode_auto(pioche, affichage=False):
	""" Joue automatiquement la réussite en partant sur la pioche donnée (peut afficher ou non les
			étapes).
		
		pioche (list): La liste des cartes de la pioche
		affichage (bool): Si True, affiche la pioche et la réussite après chaque changement (False
			par défaut) """

	if affichage:
		faire_parler("Voici la pioche", config.NOM_ORDI)
		afficher_reussite(pioche)

	reussite = []

	while pioche:
		une_etape_reussite(reussite, pioche, affichage)


def reussite_mode_manuel(pioche, nb_tas_max=2):
	""" Fait jouer l'utilisateur avec la pioche donnée en affichant des menus. La partie est gagnée
			si le joueur termine avec un nombre de tas inférieur ou égal à nb_tas_max.
		
		pioche (list): La liste des cartes de la pioche
		nb_tas_max (int): Nombre de tas restant maximum pour gagner (2 par défaut) """
	
	reussite = []

	piocher(reussite, pioche)
	piocher(reussite, pioche)
	piocher(reussite, pioche)

	while pioche:
		faire_parler("Voici les tas visibles", config.NOM_ORDI)
		afficher_reussite(reussite)

		mode = demander_qcm(
			"Choisissez une action", 
			"Piocher une carte", 
			"Effectuer un saut", 
			"Réafficher le jeu", 
			"Quitter")

		if mode == 0:
			piocher(reussite, pioche)

		elif mode == 1:
			saut = demander_entier(
				f"Quel tas faire sauter ? (ne s'applique ni au 1er ni au dernier tas)",
				1, len(reussite) - 2)

			if saut_si_possible(reussite, saut):
				faire_parler("Un saut a été effectué !", config.NOM_ORDI)
			else:
				faire_parler("Impossible de faire sauter ce tas !", config.NOM_ORDI)

		elif mode == 3:
			faire_parler("Vous avez quitté la partie !", config.NOM_ORDI)
			return None

	faire_parler("Le jeu est terminé !", config.NOM_ORDI)
	faire_parler(f"Il vous reste {len(reussite)} tas", config.NOM_ORDI)

	if len(reussite) > nb_tas_max:
		faire_parler("Vous avez perdu !", config.NOM_ORDI)
	else:
		faire_parler("Vous avez gagné !", config.NOM_ORDI)


def lance_reussite(mode, nb_cartes=32, affiche=False, nb_tas_max=2):
	""" Lance une partie automatique ou manuelle avec un nombre de cartes fixé. Peut afficher ou
			non les changements. La partie est gagnée si elle se termine avec un nombre de tas
			inférieur ou égal à nb_tas_max.
		
		mode (str): Le mode de résolution du jeu ('auto' ou 'manuel')
		nb_cartes (int): Nombre de cartes du jeu (32 par défaut)
		affiche (bool): Si True, affiche la pioche et la réussite après chaque changement (False
			par défaut)
		nb_tas_max (int): Nombre de tas restant maximum pour gagner (2 par défaut) """
	
	depuis_fichier = bool(demander_qcm("Charger la pioche depuis un fichier ?", "Non", "Oui"))

	if depuis_fichier:
		pioche = init_pioche_fichier(demander_chaine("Entrez le chemin vers le fichier à charger"))
	else:
		pioche = init_pioche_alea(nb_cartes)

	pioche_copie = pioche[:]

	if mode:
		reussite_mode_auto(pioche, affiche)
	else:
		reussite_mode_manuel(pioche, nb_tas_max)

	if not depuis_fichier:
		sauve_pioche = bool(demander_qcm("Enregistrer la pioche ?", "Non", "Oui"))

		if sauve_pioche:
			ecrire_fichier_reussite(demander_chaine("Entrez le chemin vers le fichier à charger"), pioche_copie)


def lancer_reussite_gfx(fenetre, images, mode, nb_cartes=32, nb_tas_max=2):
	widgets = []

	def demander_pioche_from_fichier():
		widgets.clear()
		widgets.extend(creer_widgets_qcm("Voulez-vous charger la pioche depuis un fichier ?", "Oui", "Non"))

	def demander_pioche_to_fichier():
		widgets.clear()
		widgets.extend(creer_widgets_qcm("Voulez-vous sauvegarder la pioche ?", "Oui", "Non"))

	def handler(widget, evenement):
		pass

	demander_pioche_from_fichier(None, None)

	while True:
		redessiner_gfx(fenetre, widgets)


def preparer_reussite():
	""" Demande le mode de jeu, le nombre de carte et d'autres informations essentielles au
		démarrage du jeu.
		Ne prend aucun argument. """

	faire_parler("Bienvenu dans La réussite des alliances !", config.NOM_ORDI)
	mode = demander_qcm("Quel mode ?", "Manuel", "Automatique")
	jeu_type = 32 + 20 * demander_qcm("Quel jeu ?", "32 cartes", "52 cartes")

	if mode:
		faire_parler("Vous avez choisi le mode automatique", config.NOM_ORDI)
		affiche = bool(demander_qcm("Voulez-vous activer l'affichage ?", "Non", "Oui"))
		tas_max = 2
	else:
		faire_parler("Vous avez choisi le mode manuel", config.NOM_JOUEUR)
		tas_max = demander_entier("Nombre de tas maximum pour gagner", 2, 32)
		affiche = False

	lance_reussite(mode, jeu_type, affiche, tas_max)
	deboggue("Fin du jeu", config.NOM_ORDI)


def preparer_reussite_gfx(fenetre, images):
	""" Même chose que preparer_reussite mais en mode graphique.

		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire des images du jeu """

	widgets = []
	infos = {"mode": 0, "jeu": 32, "affiche": False, "etape": 0}

	def demander_mode():
		widgets.clear()
		widgets.extend(creer_widgets_qcm("Choisissez un mode", "Manuel", "Automatique"))

	def demander_jeu():
		widgets.clear()
		widgets.extend(creer_widgets_qcm("Choisissez un jeu", "32 cartes", "52 cartes"))

	def demander_tas_max():
		widgets.clear()

	def handler():
		if infos["etape"] == 0:
			demander_mode()
		elif infos["etape"] == 1:
			demander_jeu()
		elif infos["etape"] == 2:
			demander_tas_max()
		else:
			lancer_reussite_gfx(fenetre, images, infos["mode"], infos["jeu"], infos["nb_tas_max"])
		infos["etape"] += 1

	handler()

	while True:
		redessiner_gfx(fenetre, widgets)


def main():
	""" Fonction principale. Initialise l'interface et lance le jeu.
		Ne prend aucun argument. """
	
	if init_gfx() and not config.FORCE_CONSOLE:
		deboggue("Le jeu est en mode graphique")

		l, h = config.TAILLE_FENETRE
		fenetre = creer_fenetre("PolyAlliances (Chargement des ressources...)", l, h)

		deboggue("Chargement des images...")
		images = charger_images_jeu()
		deboggue("Chargement terminé")

		definir_titre("PolyAlliances")

		preparer_reussite_gfx(fenetre, images)
	else:
		deboggue("Le jeu est en mode console")
		preparer_reussite()


if __name__ == "__main__":
	main()