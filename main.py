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

from activite import *
from console import *
from evenement import *
from gfx import *
from jeu import *

from utile import deboggue


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
		dire("Voici la pioche")
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
		dire("Voici les tas visibles")
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
				"Quel tas faire sauter ? (ne s'applique ni au 1er ni au dernier tas)",
				1, len(reussite) - 2)

			if saut_si_possible(reussite, saut):
				dire("Un saut a été effectué !")
			else:
				dire("Impossible de faire sauter ce tas !")

		elif mode == 3:
			dire("Vous avez quitté la partie !")
			dire("Voici les cartes qu'il restait dans la pioche")
			afficher_reussite(pioche)
			return None

	dire("Le jeu est terminé !")
	dire("Il vous reste {} tas".format(len(reussite)))

	if len(reussite) > nb_tas_max:
		dire("Vous avez perdu !")
	else:
		dire("Vous avez gagné !")


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
		pioche = init_pioche_fichier(demander_fichier("Entrez le chemin vers le fichier à charger"))
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
			ecrire_fichier_reussite(demander_fichier("Entrez le chemin vers le fichier à charger", False), pioche_copie)


def preparer_reussite():
	""" Demande le mode de jeu, le nombre de carte et d'autres informations essentielles au
		démarrage du jeu.
		Ne prend aucun argument. """

	dire("Bienvenu dans La réussite des alliances !")
	mode = demander_qcm("Quel mode ?", "Manuel", "Automatique")
	jeu_type = 32 + 20 * demander_qcm("Quel jeu ?", "32 cartes", "52 cartes")

	if mode:
		dire("Vous avez choisi le mode automatique")
		affiche = bool(demander_qcm("Voulez-vous activer l'affichage ?", "Non", "Oui"))
		tas_max = 2
	else:
		dire("Vous avez choisi le mode manuel")
		tas_max = demander_entier("Nombre de tas maximum pour gagner", 2, 32)
		affiche = False

	lance_reussite(mode, jeu_type, affiche, tas_max)


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
		activite = creer_menu_reussite(images, reussite)
		redessiner_gfx(fenetre, activite)
		time.sleep(1)
		une_etape_reussite(reussite, pioche)

	activite = creer_widgets_reussite(images, reussite)
	redessiner_gfx(fenetre, activite)
	time.sleep(4)


def reussite_mode_manuel_gfx(fenetre, images, pioche, nb_tas_max=2):
	""" Fait jouer l'utilisateur avec la pioche donnée. La partie est gagnée si le joueur termine
			avec un nombre de tas inférieur ou égal à nb_tas_max.
		
		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire des images chargées
		pioche (list): La liste des cartes de la pioche
		nb_tas_max (int): Nombre de tas restant maximum pour gagner (2 par défaut) """

	def quand_clic(num_tas):
		vider_activite(activite)

		if num_tas >= 0:
			if saut_si_possible(reussite, num_tas):
				ajouter_activite(activite, creer_activite_textinfo("Un saut a été effectué"))
			else:
				ajouter_activite(activite, creer_activite_textinfo("Impossible de faire sauter cette carte"))
		else:
			piocher(reussite, pioche)
		
		a = creer_menu_reussite(images, reussite, quand_clic)
		ajouter_activite(activite, a)

	reussite = []
	activite = creer_menu_reussite(images, reussite, quand_clic)

	piocher(reussite, pioche)
	piocher(reussite, pioche)
	quand_clic(-1)

	while pioche:
		redessiner_gfx(fenetre, activite)
		interagir(activite)


def lancer_reussite_gfx(fenetre, images, mode, nb_cartes=32, nb_tas_max=2):
	""" Crée la pioche, lance une partie puis sauvegarde la pioche.

		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire des images chargées
		mode (int): Le mode de jeu (0=manuel, 1=auto)
		nb_cartes (int): Nombre de cartes du jeu (32 par défaut
		nb_tas_max (int): Nombre de tas maximum pour gagner """

	def demander_fichier_charge():
		vider_activite(activite)
		a = creer_menu_qcm("Voulez-vous charger la pioche depuis un fichier ?", suivant, "Oui", "Non")
		ajouter_activite(activite, a)

	def demander_chemin_charge(texte=""):
		if texte == None:
			texte = ""
			erreur = "Chemin invalide"
		else:
			erreur = ""

		vider_activite(activite)
		a = creer_menu_fichier("Où se trouve le fichier à charger ?", suivant, demander_chemin_charge, texte, erreur)
		ajouter_activite(activite, a)

	def demander_fichier_sauve():
		vider_activite(activite)
		a = creer_menu_qcm("Voulez-vous sauvegarder la pioche dans un fichier ?", suivant, "Oui", "Non")
		ajouter_activite(activite, a)

	def demander_chemin_sauve(texte=""):
		if texte == None:
			texte = ""
			erreur = "Chemin invalide"
		else:
			erreur = ""

		vider_activite(activite)
		a = creer_menu_fichier("Où sauvegarder la pioche ?", suivant, demander_chemin_sauve, texte, erreur)
		ajouter_activite(activite, a)

	def lancer_partie():
		if mode:
			reussite_mode_auto_gfx(fenetre, images, stats["pioche"])
		else:
			reussite_mode_manuel_gfx(fenetre, images, stats["pioche"], nb_tas_max)
		demander_fichier_sauve()

	def suivant(retour):
		if stats["etape"] == 0:
			demander_fichier_charge()
		
		elif stats["etape"] == 1:
			if retour:
				stats["pioche"] = init_pioche_alea()
				stats["pioche_cp"] = stats["pioche"][:]
				stats["etape"] += 1
				lancer_partie()
			else:
				demander_chemin_charge()
		
		elif stats["etape"] == 2:
			stats["pioche"] = init_pioche_fichier(retour)
			stats["pioche_cp"] = stats["pioche"][:]
			lancer_partie()

		elif stats["etape"] == 3:
			if retour:
				stats["etape"] += 1
			else:
				demander_chemin_sauve()
		else:
			ecrire_fichier_reussite(retour, stats["pioche_cp"])

		stats["etape"] += 1

	stats = {"pioche": [], "etape": 0, "pioche_cp": []}
	activite = creer_activite([], [], [])

	suivant(0)

	while stats["etape"] < 5:
		redessiner_gfx(fenetre, activite)
		interagir(activite)


def preparer_reussite_gfx(fenetre, images):
	""" Même chose que preparer_reussite mais en mode graphique.

		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire des images du jeu """

	def demander_mode():
		vider_activite(activite)
		ajouter_activite(activite, creer_menu_qcm("Choisissez un mode", suivant, "Manuel", "Automatique"))

	def demander_jeu():
		vider_activite(activite)
		ajouter_activite(activite, creer_menu_qcm("Choisissez un jeu", suivant, "32 cartes", "52 cartes"))

	def demander_tas_max(texte=""):
		if texte == None:
			texte = ""
			erreur = "Vous devez entrer un entier compris entre 2 et {}".format(stats["jeu"])
		else:
			erreur = ""
		vider_activite(activite)
		a = creer_menu_entier("Nombre de tas maximum ?", suivant, demander_tas_max, 2, stats["jeu"], texte, erreur)
		ajouter_activite(activite, a)

	def suivant(retour):
		if stats["etape"] == 0:
			demander_mode()
		
		elif stats["etape"] == 1:
			stats["mode"] = retour
			demander_jeu()

		elif stats["etape"] == 2:
			stats["jeu"] = 32+20*retour
			demander_tas_max()

		else:
			lancer_reussite_gfx(fenetre, images, stats["mode"], stats["jeu"], retour)

		stats["etape"] += 1

	stats = {"mode": 0, "jeu": 32, "etape": 0}
	activite = creer_activite([], [], [])

	suivant(0)

	while stats["etape"] < 4:
		redessiner_gfx(fenetre, activite)
		interagir(activite)


###################################################################################################
### Demarrage du jeu ##############################################################################
###################################################################################################

def main():
	""" Fonction principale. Initialise l'interface et lance le jeu.
		Ne prend aucun argument. """
	
	if init_gfx() and not config.FORCE_CONSOLE:
		deboggue("Le jeu est en mode graphique")

		l, h = config.TAILLE_FENETRE
		fenetre = creer_fenetre("PolyAlliances (Chargement...)", l, h)

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