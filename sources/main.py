#!/usr/bin/env python3

#
# PolyAlliances
#
# Date de création: 08/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

""" Script principal du jeu """

import config
import tkinter

from console import *
from gui import *
from jeu import *
from stats import *

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

	liste_tas = []
	pioche = pioche[:]

	if affichage:
		dire("Voici la pioche")
		afficher_reussite(pioche)

	while pioche:
		une_etape_reussite(liste_tas, pioche, affichage)

	if affichage:
		dire("La jeu est terminé !")
		dire("Il reste {} tas.".format(len(liste_tas)))

	return liste_tas


def reussite_mode_manuel(pioche, nb_tas_max=2):
	""" Fait jouer l'utilisateur avec la pioche donnée en affichant des menus. La partie est gagnée
			si le joueur termine avec un nombre de tas inférieur ou égal à nb_tas_max.
		
		pioche (list): La liste des cartes de la pioche
		nb_tas_max (int): Nombre de tas restant maximum pour gagner (2 par défaut) """
	
	liste_tas = []
	pioche = pioche[:]

	piocher(liste_tas, pioche)
	piocher(liste_tas, pioche)
	piocher(liste_tas, pioche)

	while pioche:
		dire("Voici les tas visibles")
		afficher_reussite(liste_tas)

		mode = demander_qcm(
			"Choisissez une action", 
			"Piocher une carte", 
			"Effectuer un saut", 
			"Réafficher le jeu", 
			"Quitter")

		if mode == 0:
			piocher(liste_tas, pioche)

		elif mode == 1:
			saut = demander_entier(
				"Quel tas faire sauter ? (ne s'applique ni au 1er ni au dernier tas)",
				1, len(liste_tas) - 2)

			if saut_si_possible(liste_tas, saut):
				dire("Un saut a été effectué !")
			else:
				dire("Impossible de faire sauter ce tas !")

		elif mode == 3:
			dire("Vous avez quitté la partie !")
			dire("Voici les cartes qu'il restait dans la pioche")
			afficher_reussite(pioche)
			return liste_tas

	dire("Le jeu est terminé !")

	return liste_tas


def lance_reussite(mode, nb_cartes=32, affiche=False, nb_tas_max=2):
	""" Lance une partie automatique ou manuelle avec un nombre de cartes fixé. Peut afficher ou
			non les changements. La partie est gagnée si elle se termine avec un nombre de tas
			inférieur ou égal à nb_tas_max.
		
		mode (str): Le mode de résolution du jeu ('auto' ou 'manuel')
		nb_cartes (int): Nombre de cartes du jeu (32 par défaut)
		affiche (bool): Si True, affiche la pioche et la réussite après chaque changement (False
			par défaut)
		nb_tas_max (int): Nombre de tas restant maximum pour gagner (2 par défaut) """

	while True:	
		depuis_fichier = demander_qcm("Charger la pioche depuis un fichier ?", "Non", "Oui")

		if depuis_fichier:
			pioche = init_pioche_fichier(demander_fichier("Entrez le chemin vers le fichier à charger"))
		else:
			pioche = init_pioche_alea(nb_cartes)

		if not verifier_pioche(pioche, nb_cartes):
			dire("Triche détectée ! La pioche est invalide !")
			pioche_acceptee = demander_qcm("Voulez-vous continuer avec cette pioche ?", "Non", "Oui")

			if pioche_acceptee:
				break
		else:
			break

	liste_tas = []

	if mode == "auto":
		liste_tas = reussite_mode_auto(pioche, affiche)
		dire("Il reste {} tas".format(len(liste_tas)))

	elif mode == "manuel":
		liste_tas = reussite_mode_manuel(pioche, nb_tas_max)
		dire("Il reste {} tas".format(len(liste_tas)))

		if len(liste_tas) > nb_tas_max:
			dire("Vous avez perdu !")
		else:
			dire("Vous avez gagné !")
	else:
		deboggue("Mode non reconnu !")

	if not depuis_fichier:
		sauve_pioche = demander_qcm("Enregistrer la pioche ?", "Non", "Oui")

		if sauve_pioche:
			ecrire_fichier_reussite(demander_fichier("Entrez le chemin vers le fichier à charger", False), pioche)

	return liste_tas


def preparer_reussite():
	""" Demande le mode de jeu, le nombre de carte et d'autres informations essentielles au
		démarrage du jeu.
		Ne prend aucun argument. """

	dire("Bienvenu dans La réussite des alliances !")
	mode = demander_qcm("Quel mode ?", "Manuel", "Automatique")
	nb_cartes = 32 + 20 * demander_qcm("Quel jeu ?", "32 cartes", "52 cartes")

	if mode:
		dire("Vous avez choisi le mode automatique")
		affiche = bool(demander_qcm("Voulez-vous activer l'affichage ?", "Non", "Oui"))
		tas_max = 2
		mode = "auto"
	else:
		dire("Vous avez choisi le mode manuel")
		tas_max = demander_entier("Nombre de tas maximum pour gagner", 2, 32)
		affiche = False
		mode = "manuel"

	lance_reussite(mode, nb_cartes, affiche, tas_max)


def preparer_statistiques():
	""" Propose au joueur de choisir le nombre de cartes et de simulations faites pour établir
			des statistiques. """

	nb_cartes = 32 + 20 * demander_qcm("Quel jeu ?", "32 cartes", "52 cartes")
	nb_sim = demander_entier("Nombre de simulation par tas max", 1, float("inf"))

	creer_graphique(nb_sim, nb_cartes)


def choisir_programme():
	""" Propose au joueur de choisir entre jouer une partie et simplement lancer le programme de
			statistiques. """

	prog = demander_qcm("Quel voulez-vous faire ?", "Jouer", "Statistiques")

	if prog:
		preparer_statistiques()
	else:
		preparer_reussite()


###################################################################################################
### Mode graphique ################################################################################
###################################################################################################

def reussite_mode_auto_gui(fenetre, images, pioche):
	""" Joue automatiquement la réussite en partant sur la pioche donnée.
		
		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire des images chargées
		pioche (list): La liste des cartes de la pioche """

	def tick():
		effacer_dessin(canvas)
		une_etape_reussite(liste_tas, pioche)
		dessiner_reussite_gui(canvas, images, liste_tas)

		if pioche:
			fenetre.after(500, tick)

	liste_tas = []
	pioche = pioche[:]

	canvas = creer_zone_jeu(fenetre)
	dessiner_reussite_gui(canvas, images, pioche)
	fenetre.after(500, tick)

	while pioche:
		redessiner_fenetre(fenetre)

	canvas.destroy()

	return liste_tas


def reussite_mode_manuel_gui(fenetre, images, pioche, nb_tas_max=2):
	""" Fait jouer l'utilisateur avec la pioche donnée. La partie est gagnée si le joueur termine
			avec un nombre de tas inférieur ou égal à nb_tas_max.
		
		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire des images chargées
		pioche (list): La liste des cartes de la pioche
		nb_tas_max (int): Nombre de tas restant maximum pour gagner (2 par défaut) """

	def quand_clic(num_tas):
		effacer_dessin(canvas)

		if num_tas == -1:
			piocher(liste_tas, pioche)
		elif saut_si_possible(liste_tas, num_tas):
			dessiner_texte(canvas, "Un saut a été effectué")
		else:
			dessiner_texte(canvas, "Impossible de faire sauter cette carte")
		
		dessiner_reussite_gui(canvas, images, liste_tas, quand_clic)

	canvas = creer_zone_jeu(fenetre)
	liste_tas = []
	pioche = pioche[:]

	dessiner_reussite_gui(canvas, images, liste_tas, quand_clic)

	while pioche:
		redessiner_fenetre(fenetre)

	canvas.destroy()
	return liste_tas


def lance_reussite_gui(fenetre, images, mode, nb_cartes=32, affiche=False, nb_tas_max=2):
	""" Crée la pioche, lance une partie puis sauvegarde la pioche.

		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire des images chargées
		mode (int): Le mode de jeu (0=manuel, 1=auto)
		nb_cartes (int): Nombre de cartes du jeu (32 par défaut
		nb_tas_max (int): Nombre de tas maximum pour gagner """

	while True:
		nom_fichier, truquee = demander_charger_pioche(fenetre)

		if nom_fichier:
			pioche = init_pioche_fichier(creer_chemin("ressources", "pioches", nom_fichier))
		else:
			pioche = init_pioche_alea(nb_cartes)

		if truquee:
			break
		elif verifier_pioche(pioche, nb_cartes):
			break
		else:
			afficher_popup(fenetre, "La pioche choisie est truquée !")

	liste_tas = []
	message1 = "Le jeu est terminé !"
	message2 = "Il reste {} tas."

	if mode == "auto":
		if affiche:
			liste_tas = reussite_mode_auto_gui(fenetre, images, pioche)
		else:
			liste_tas = reussite_mode_auto(pioche)

		message2 = message2.format(len(liste_tas))
		afficher_popup(fenetre, message1, message2)

	elif mode == "manuel":
		liste_tas = reussite_mode_manuel_gui(fenetre, images, pioche, nb_tas_max)
	
		message2 = message2.format(len(liste_tas))

		if len(liste_tas) > nb_tas_max:
			message3 = "Vous avez perdu !"
		else:
			message3 = "Vous avez gagné !"
		afficher_popup(fenetre, message1, message2, message3)
	else:
		deboggue("Mode non reconnu !")

	nom_fichier = demander_sauver_pioche(fenetre)

	if nom_fichier:
		ecrire_fichier_reussite(creer_chemin("ressources", "pioches", nom_fichier), pioche)

	return liste_tas


def preparer_reussite_gui(fenetre, images):
	""" Même chose que preparer_reussite mais en mode graphique.

		fenetre (tkinter.Tk): La fenêtre de jeu
		images (dict): Le dictionnaire des images du jeu """

	modes = ("manuel", "auto")
	mode, nb_cartes, affiche, nb_tas_max = demander_reglages(fenetre)
	
	mode = modes[mode]
	nb_cartes = 32 + 20 * nb_cartes
	affiche = bool(affiche)
	nb_tas_max = int(nb_tas_max)

	lance_reussite_gui(fenetre, images, mode, nb_cartes, affiche, nb_tas_max)


def preparer_statistiques_gui(fenetre):
	""" Même chose que preparer_statistiques mais en mode graphique.

		fenetre (tkinter.Tk): La fenêtre de jeu """

	nb_sim, nb_cartes = demander_reglages_stats(fenetre)

	nb_sim = int(nb_sim)
	nb_cartes = 32+20*nb_cartes

	fenetre.destroy()
	creer_graphique(nb_sim, nb_cartes)


def choisir_programme_gui(fenetre, images):
	""" Même chose que choisir_programme mais en mode graphique.

		fenetre (tkinter.Tk): La fenêtre de jeu
		images (dict): Le dictionnaire des images du jeu """

	prog = demander_programme(fenetre)

	if prog:
		preparer_statistiques_gui(fenetre)
	else:
		preparer_reussite_gui(fenetre, images)


###################################################################################################
### Demarrage du jeu ##############################################################################
###################################################################################################

def main():
	""" Fonction principale. Initialise l'interface et lance le jeu.
		Ne prend aucun argument. """
	
	if config.FORCE_CONSOLE:
		deboggue("Le jeu est en mode console")
		choisir_programme()
	else:
		deboggue("Le jeu est en mode graphique")
		fenetre = creer_fenetre()
		images = charge_images()
		choisir_programme_gui(fenetre, images)

	deboggue("Arrêt normal")


if __name__ == "__main__":
	main()