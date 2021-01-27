#
# PolyAlliances
#
# Date de création: 27/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

""" Contient des fonctions de simulations et de créations de graphiques """

import matplotlib.pyplot as plt

from jeu import *
from console import *
from utile import deboggue


def res_multi_simulation(nb_sim, nb_cartes=32):
	""" Réalise nb_sim simulations et renvoie la liste du nombre de tas restants après chaque
			simulation.

		nb_sim (int): Le nombre de simulation à effectuer
		nb_cartes (int): Le nombre de cartes de chaque jeu (32 par défaut) """

	resultats = []

	for sim in range(nb_sim):
		deboggue("Simulation n" + str(sim))
		pioche = init_pioche_alea(nb_cartes)
		liste_tas = []
		
		while pioche:
			une_etape_reussite(liste_tas, pioche)

		resultats.append(len(liste_tas))
	return resultats


def statistiques_nb_tas(nb_sim, nb_cartes=32):
	""" Calcule et affiche la moyenne, le minimum et le maximum de tas restants après nb_sim
			simulations. Affiche également le nombre de tas > et < à la moyenne.

		nb_sim (int): Le nombre de simulation à effectuer
		nb_cartes (int): Le nombre de cartes de chaque jeu (32 par défaut) """

	resultats = res_multi_simulation(nb_sim, nb_cartes)
	mini = nb_cartes
	maxi = 2
	total = 0

	for resultat in resultats:
		if resultat > maxi:
			maxi = resultat
		if resultat < mini:
			mini = resultat
		total += resultat

	moyenne = total / len(resultats)
	inf_m = 0
	sup_m = 0

	for resultat in resultats:
		if resultat < moyenne:
			inf_m += 1
		elif resultat > moyenne:
			sup_m += 1

	dire("Après {} simulation(s) avec des jeux de {} cartes :".format(nb_sim, nb_cartes))
	dire("Moyenne: {}\tMinimum: {}\tMaximum: {}".format(moyenne, mini, maxi))
	dire("Tas inférieurs à {m}: {}\tTas supérieurs à {m}: {}".format(inf_m, sup_m, m=moyenne))


def probabilite_victoire(nb_sim, nb_cartes=32):
	""" Détermine les chances de gagner en fonction du nombre de tas maximum autorisés.

		nb_sim (int): Le nombre de simulations à chaque test
		nb_cartes (int): Le nombre de carte du jeu (32 par défaut) """

	victoires = []

	for nb_tas_max in range(nb_cartes):
		deboggue("Calcul du taux de victoire pour {} tas max".format(nb_tas_max))
		resultats = res_multi_simulation(nb_sim, nb_cartes)
		nb_victoires = sum(resultat <= nb_tas_max for resultat in resultats)
		victoires.append(nb_victoires / len(resultats))

	return victoires


def creer_graphique(nb_sim, nb_cartes=32):
	""" Crée un graphique établi à partir d'un nombre de simulations données.

		nb_sim (int): Le nombre de simulations
		nb_cartes (int): Le nombre de cartes du jeu (32 par défaut) """

	figure = plt.figure()
	figure.canvas.set_window_title("PolyAlliances statistiques")

	plt.plot(probabilite_victoire(nb_sim, nb_cartes))
	plt.title("Probabilité de gagner en fonction du nombre de tas maximum")
	plt.xlabel("Nombre de tas maximum")
	plt.ylabel("Probabilité de gagner")
	plt.show()


if __name__ == "__main__":
	creer_graphique(30) # ceci est un exemple