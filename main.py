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
import time

from console import *
from gui import *
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

	lancer_reussite(mode, jeu_type, affiche, tas_max)


###################################################################################################
### Mode graphique ################################################################################
###################################################################################################

def reussite_mode_auto_gui(fenetre, images, pioche, affichage=False):
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

	if affichage:
		canvas = creer_zone_jeu(fenetre)
		dessiner_reussite_gui(canvas, images, pioche)
		fenetre.after(500, tick)

		while pioche:
			redessiner_fenetre(fenetre)
		canvas.destroy()
	else:
		while pioche:
			une_etape_reussite(liste_tas, pioche)


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

	dessiner_reussite_gui(canvas, images, liste_tas, quand_clic)

	while pioche:
		redessiner_fenetre(fenetre)

	canvas.destroy()


def lance_reussite_gui(fenetre, images, mode, nb_cartes=32, affiche=False, nb_tas_max=2):
	""" Crée la pioche, lance une partie puis sauvegarde la pioche.

		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire des images chargées
		mode (int): Le mode de jeu (0=manuel, 1=auto)
		nb_cartes (int): Nombre de cartes du jeu (32 par défaut
		nb_tas_max (int): Nombre de tas maximum pour gagner """

	nom_fichier = demander_charger_pioche(fenetre)

	if nom_fichier:
		pioche = init_pioche_fichier(creer_chemin("ressources", "pioches", nom_fichier))
	else:
		pioche = init_pioche_alea(nb_cartes)

	pioche_copie = pioche[:]

	if mode:
		reussite_mode_auto_gui(fenetre, images, pioche, affiche)
	else:
		reussite_mode_manuel_gui(fenetre, images, pioche, nb_tas_max)

	nom_fichier = demander_sauver_pioche(fenetre)

	if nom_fichier:
		ecrire_fichier_reussite(creer_chemin("ressources", "pioches", nom_fichier), pioche_copie)


def preparer_reussite_gui(fenetre, images):
	""" Même chose que preparer_reussite mais en mode graphique.

		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire des images du jeu """

	def quand_valide():
		info_boucle["attente"] = False

	def quand_tape(texte):
		if texte:
			if texte.isdigit():
				return int(texte) >= 2
		return False

	def quand_mode_change(*args):
		if var_mod.get():
			desactiver_categorie(saisi_tas)
			activer_categorie(qcm_aff)
		else:
			desactiver_categorie(qcm_aff)
			activer_categorie(saisi_tas)
			var_aff.set(1)

	cadre = creer_categorie(fenetre, "Réglages", "n")
	qcm_mod, var_mod = creer_qcm_simple(cadre, "Mode de jeu", "Manuel", "Automatique")
	qcm_jeu, var_jeu = creer_qcm_simple(cadre, "Nombre de cartes", "32 cartes", "52 cartes")
	qcm_aff, var_aff = creer_qcm_simple(cadre, "Activer l'affichage", "Non", "Oui")
	saisi_tas, var_tas = creer_champs_saisi(cadre, "Nombre de tas maxi pour gagner", quand_tape, "Entier supérieur à 2")
	bouton_valide = creer_bouton(cadre, "Continuer", quand_valide)

	info_boucle = {"attente": True}

	var_mod.trace("w", quand_mode_change)
	var_tas.set("2")

	quand_mode_change()

	while info_boucle["attente"]:
		redessiner_fenetre(fenetre)

	cadre.destroy()
	lance_reussite_gui(fenetre, images, var_mod.get(), 32+20*var_jeu.get(), bool(var_aff.get()), int(var_tas.get()))


###################################################################################################
### Demarrage du jeu ##############################################################################
###################################################################################################

def main():
	""" Fonction principale. Initialise l'interface et lance le jeu.
		Ne prend aucun argument. """
	
	if config.FORCE_CONSOLE:
		deboggue("Le jeu est en mode graphique")
		fenetre = creer_fenetre()
		images = charge_images()
		preparer_reussite_gui(fenetre, images)
	else:
		deboggue("Le jeu est en mode console")
		preparer_reussite()


if __name__ == "__main__":
	main()