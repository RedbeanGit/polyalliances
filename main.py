#
# PolyAlliances
#
# Date de création: 08/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

""" Script principal du jeu """

from fonction import *


def main():
	""" Fonction principale du jeu. Ne prend aucun argument """
	
	print("Bienvenu dans La réussite des alliances !")
	mode = afficher_menu("Choisissez un mode de jeu", "Manuel", "Automatique", "Quitter")

	if mode != 3:
		lance_reussite(mode)
	print("Fin du jeu")


def reussite_mode_auto(pioche, affichage=False):
	""" Joue automatiquement la réussite en partant sur la pioche donnée (peut afficher ou non les
			étapes).
		
		pioche (list): La liste des cartes de la pioche
		affichage (bool): Si True, affiche la pioche et la réussite après chaque changement (False
			par défaut) """

	if affichage:
		afficher_reussite(pioche)
		print()

	reussite = []

	while pioche:
		une_etape_reussite(reussite, pioche, affichage)


def reussite_mode_manuel(pioche, nb_tas_max=2):
	""" Fait jouer l'utilisateur avec la pioche donnée en affichant des menus. La partie est gagnée
			si le joueur termine avec un nombre de tas inférieur ou égal à nb_tas_max.
		
		pioche (list): La liste des cartes de la pioche
		nb_tas_max (int): Nombre de tas restant maximum pour gagner (2 par défaut) """
	
	reussite = []

	while pioche:
		mode = afficher_menu(
			"Choisissez une action", 
			"Piocher une carte", 
			"Effectuer un saut", 
			"Réafficher le jeu", 
			"Quitter")

		if mode == 1:
			piocher(reussite, pioche)
		elif mode == 2:
			if len(reussite) >= 3:
				print(f"Entrez le numéro du tas à faire sauter (compris entre 1 et {len(reussite)-2})")
				saut = choisir_numero(1, len(reussite)-2)

				if saut_si_possible(reussite, saut):
					print("Un saut a été effectué !")
				else:
					print("Impossible de faire sauter ce tas")
			else:
				print("Il n'y a pas assez de cartes pour tenter un saut !")
		elif mode == 4:
			print("Fin de partie !")
			return None

		print("\nTas visibles: ", end="")
		afficher_reussite(reussite)
		print()

	print("Le jeu est terminé !")
	print(f"Il vous reste {len(reussite)} tas")

	if len(reussite) > nb_tas_max:
		print(f"Vous avez perdu !")
	else:
		print(f"Vous avez gagné !")


def lance_reussite(mode, nb_cartes=32, affiche=False, nb_tas_max=2):
	""" Lance une partie automatique ou manuelle avec un nombre de cartes fixé. Peut afficher ou
			non les changements. La partie est gagnée si elle se termine avec un nombre de tas
			inférieur ou égal à nb_tas_max.
		
		mode (str): Le mode de résolution du jeu ('auto' ou 'manuel')
		nb_cartes (int): Nombre de cartes du jeu (32 par défaut)
		affiche (bool): Si True, affiche la pioche et la réussite après chaque changement (False
			par défaut)
		nb_tas_max (int): Nombre de tas restant maximum pour gagner (2 par défaut) """
	
	depuis_fichier = afficher_menu("Charger la pioche depuis un fichier ?", "Oui", "Non")

	if depuis_fichier == 1:
		pioche = init_pioche_fichier(input("Chemin du fichier> "))
	else:
		pioche = init_pioche_alea(nb_cartes)
	print(pioche)

	if mode == 1:
		reussite_mode_manuel(pioche, nb_tas_max)
	else:
		reussite_mode_auto(pioche, affiche)


if __name__ == "__main__":
	main()