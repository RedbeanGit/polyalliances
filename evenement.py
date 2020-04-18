#
# PolyAlliances
#
# Date de création: 17/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

""" Propose des fonctions liées à la gestion des interactions avec l'utilisateur """

try:
	import pygame
except ImportError:
	pass

from utile import *


def interagir(actions):
	""" Parcourt la liste des évenements ajoutés depuis le dernier appel de cette fonction et
			execute les actions associées. Ne fonctionne que si Pygame a été initialisé.

		actions (list): La liste des actions à executer """

	type_mouvement = {
		"survol": pygame.MOUSEMOTION,
		"clic": pygame.MOUSEBUTTONUP,
		"drop": pygame.DROPFILE,
		"appui": pygame.KEYDOWN,
		}

	for evenement in pygame.event.get():
		if evenement.type == pygame.QUIT:
			arreter()

		for action in actions:
			if evenement.type == type_mouvement[action["mouvement"]]:
				if action["widget"]:
					if action["mouvement"] in ("survol", "clic"):
						x, y = evenement.pos
					else:
						x, y = pygame.mouse.get_pos()

					widget = action["widget"]
					xw, yw = widget["position"]
					axw, ayw = widget["ancrage"]
					lw, hw = widget["image"].get_size()
					xw -= axw * lw
					yw -= ayw * hw

					if x >= xw and x < xw + lw and y >= yw and y < yw + hw:
						executer_action(action, evenement)
				else:
					executer_action(action, evenement)


def executer_action(action, evenement):
	""" Excecute une action.

		action (dict): L'action à executer
		evenement (pygame.event.Event): L'évenement à l'origine de cette action """

	action["fonction"](evenement, *action["args"], **action["kwargs"])


def creer_action(mouvement, fonction, *args, widget=None, **kwargs):
	""" Crée et renvoie une action associée à un type d'évenement donné.

		mouvement (str): L'action effectuée par l'utilisateur ('survol', 'clic', 'appui' ou 'drop')
		fonction (function, method): La fonction à executer lors du déclenchement de l'évenement
		args (*object): Les arguments à passer à 'fonction'
		widget (dict): Le widget sur lequel le curseur de la souris doit passer
		kwargs (**object): Les arguments optionels à passer à 'fonction' """

	action =  {
		"fonction": fonction, 
		"mouvement": mouvement,
		"widget": widget,
		"args": args, 
		"kwargs": kwargs
	}

	return action