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

from console import *
from evenement import *
from gfx import *
from jeu import *


###################################################################################################
### Mode console ##################################################################################
###################################################################################################

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


###################################################################################################
### Mode graphique ################################################################################
###################################################################################################

def reussite_mode_auto_gfx(fenetre, images, pioche):
	""" Joue automatiquement la réussite en partant sur la pioche donnée.
		
		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire des images chargées
		pioche (list): La liste des cartes de la pioche """

	reussite = []
	
	piocher(reussite, pioche)
	piocher(reussite, pioche)
	piocher(reussite, pioche)

	while pioche:
		widgets, actions = creer_widgets_reussite(images, reussite)
		redessiner_gfx(fenetre, widgets)
		time.sleep(1)
		une_etape_reussite(reussite, pioche)

	widgets, actions = creer_widgets_reussite(images, reussite)
	redessiner_gfx(fenetre, widgets)
	time.sleep(4)


def reussite_mode_manuel_gfx(fenetre, images, pioche, nb_tas_max=2):
	""" Fait jouer l'utilisateur avec la pioche donnée. La partie est gagnée si le joueur termine
			avec un nombre de tas inférieur ou égal à nb_tas_max.
		
		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire des images chargées
		pioche (list): La liste des cartes de la pioche
		nb_tas_max (int): Nombre de tas restant maximum pour gagner (2 par défaut) """

	stats = {"widgets": [], "actions": [], "reussite": []}

	def handler(carte_id):
		if carte_id:
			saut_si_possible(stats["reussite"], carte_id)
		else:
			piocher(stats["reussite"], pioche)
		
		w, a = creer_widgets_reussite(images, stats["reussite"], handler)
		stats["widgets"] = w
		stats["actions"] = a

	piocher(stats["reussite"], pioche)
	piocher(stats["reussite"], pioche)
	handler(0)

	while pioche:
		redessiner_gfx(fenetre, stats["widgets"])
		interagir(stats["actions"])


def lancer_reussite_gfx(fenetre, images, mode, nb_cartes=32, nb_tas_max=2):
	""" Crée la pioche, lance une partie puis sauvegarde la pioche.

		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire des images chargées
		mode (int): Le mode de jeu (0=manuel, 1=auto)
		nb_cartes (int): Nombre de cartes du jeu (32 par défaut
		nb_tas_max (int): Nombre de tas maximum pour gagner """

	stats = {"widgets": [], "actions": [], "pioche": [], "etape": 0}

	def demander_fichier_charge():
		w, a = creer_widgets_qcm("Voulez-vous charger la pioche depuis un fichier ?", handler, "Oui", "Non")
		stats["widgets"] = w
		stats["actions"] = a

	def demander_chemin_charge(texte=""):
		titre = "Où se trouve ce fichier ? (Vous pouvez glisser déposer)"
		w, a = creer_widgets_input_fichier(titre, handler, demander_chemin_charge, texte)
		stats["widgets"] = w
		stats["actions"] = a

	def demander_fichier_sauve():
		w, a = creer_widgets_qcm("Voulez-vous sauvegarder la pioche dans un fichier ?", handler, "Oui", "Non")
		stats["widgets"] = w
		stats["actions"] = a

	def demander_chemin_sauve(texte=""):
		titre = "Ou sauvegarder la pioche ? (Vous pouvez glisser déposer)"
		w, a = creer_widgets_input_fichier(titre, handler, demander_chemin_sauve, texte, False)
		stats["widgets"] = w
		stats["actions"] = a

	def lancer_partie():
		if mode:
			reussite_mode_auto_gfx(fenetre, images, stats["pioche"])
		else:
			reussite_mode_manuel_gfx(fenetre, images, stats["pioche"], nb_tas_max)
		demander_fichier_sauve()

	def handler(choix):
		if stats["etape"] == 0:
			demander_fichier_charge()
		
		elif stats["etape"] == 1:
			if choix:
				stats["pioche"] = init_pioche_alea()
				stats["etape"] += 1
				lancer_partie()
			else:
				demander_chemin_charge()
		
		elif stats["etape"] == 2:
			stats["pioche"] = init_pioche_fichier(choix)
			lancer_partie()

		elif stats["etape"] == 3:
			if choix:
				stats["etape"] += 1
			else:
				demander_chemin_sauve()
		else:
			ecrire_fichier_reussite(choix, stats["pioche"])

		stats["etape"] += 1

	handler(0)

	while stats["etape"] < 5:
		redessiner_gfx(fenetre, stats["widgets"])
		interagir(stats["actions"])


def preparer_reussite_gfx(fenetre, images):
	""" Même chose que preparer_reussite mais en mode graphique.

		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire des images du jeu """

	stats = {"widgets": [], "actions": [], "mode": 0, "jeu": 32, "etape": 0}

	def demander_mode():
		w, a = creer_widgets_qcm("Choisissez un mode", handler, "Manuel", "Automatique")
		stats["widgets"] = w
		stats["actions"] = a

	def demander_jeu():
		w, a = creer_widgets_qcm("Choisissez un jeu", handler, "32 cartes", "52 cartes")
		stats["widgets"] = w
		stats["actions"] = a

	def demander_tas_max(texte=""):
		w, a = creer_widgets_input("Nombre de tas maximum ? (chiffres seulement)", handler, demander_tas_max, int, texte)
		stats["widgets"] = w
		stats["actions"] = a

	def handler(choix):
		if stats["etape"] == 0:
			demander_mode()

		elif stats["etape"] == 1:
			stats["mode"] = choix
			demander_jeu()
		
		elif stats["etape"] == 2:
			stats["jeu"] = 32 + 20 * choix
			demander_tas_max()
		
		else:
			stats["nb_tas_max"] = choix
			lancer_reussite_gfx(fenetre, images, stats["mode"], stats["jeu"], stats["nb_tas_max"])

		stats["etape"] += 1

	handler(0)

	while stats["etape"] < 4:
		redessiner_gfx(fenetre, stats["widgets"])
		interagir(stats["actions"])


###################################################################################################
### Demarrage du jeu ##############################################################################
###################################################################################################

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