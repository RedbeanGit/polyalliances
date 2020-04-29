#!/usr/bin/env python3

#
# PolyAlliances
#
# Date de création: 08/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

###################################################################################################
### Explication ###################################################################################
###################################################################################################

""" 
	Le code du jeu est réparti en 8 parties
		- Explication: commentaires sur l'organisation du programme
		- Constantes: constantes du jeu
		- Mode console: fonctions liées à l'affichage en console
		- Mode graphique: fonctions liées à l'affichage graphique
		- Utile jeu: fonctions centrales du jeu utilisées par l'ensemble du programme
		- Statistique: fonctions liées aux simulations et statistiques
		- Fichier: fonctions liées aux fichiers et à l'execution du script
		- Principal: fonctions principales du jeu (lancent toutes les autres)
	
	Les fonctions non-obligatoires comportent les commentaires suivants:
		- (fonction extension) = Cette fonction est demandée pour une extension
		- (fonction auxilière) = Cette fonction simplifie le code global

	Pour activer le mode graphique, définissez FORCE_CONSOLE à False
"""

try:
	import matplotlib.pyplot as plt
except ImportError:
	print("Matplotlib n'est pas installé ! Le mode statistique ne fonctionnera pas")

import os
import random
import sys
import tkinter


###################################################################################################
### Constantes ####################################################################################
###################################################################################################

DEBUG=False
FORCE_CONSOLE=False
VALEURS=("A", "R", "D", "V", "10", "9", "8", "7", "6", "5", "4", "3", "2")
COULEURS={"P": "♠", "K": "♦", "C": "♥", "T": "♣"}
COULEUR_DOS=("bleu", "gris", "jaune", "rouge", "vert", "violet")
COULEUR_FOND="#004B14"
TAILLE_FENETRE=(1024, 576)
TAILLE_CARTE=(88, 128)
POS_DEPART=(45, 20)
MAX_CARTE_LIGNE=10
MARGE=5
NOM_ORDI="JEU"
NOM_JOUEUR="VOUS"


###################################################################################################
### Mode console ##################################################################################
###################################################################################################

def afficher_reussite(reussite):
	""" Affiche les cartes de la réussite les unes à côté des autres.
		
		reussite (list): Liste contenant les cartes à afficher """

	# map permet "d'appliquer" une fonction sur chaque objet d'un iterable
	# on l'utilise ici pour obtenir une "jolie" chaine pour représenter chaque carte
	print(*map(carte_to_chaine, reussite))
	print()


def afficher_menu_qcm(titre, *options):
	""" Affiche un menu avec un titre personnalisé et retourne le numéro associé au choix du joueur.
		(fonction auxilière)

		titre (str): Le titre à afficher
		options (*str): Les options proposées au joueur """

	dire(titre)
	
	# On affiche un menu
	for i, option in enumerate(options):
		print("\t{}. {}".format(i, option))
	print()

	return demander_entier(0, len(options)-1)


def afficher_menu_entier(titre, mini, maxi):
	""" Demande un entier à l'utilisateur compris entre min et max.
		(fonction auxilière)

		titre (str): Le titre à afficher
		min (int): Valeur minimale acceptée
		max (int): Valeur maximale accepté """

	# on affiche un joli titre
	dire(titre)
	print("\tEntrez un entier compris entre {} et {}".format(mini, maxi))
	print()

	return demander_entier(mini, maxi)


def afficher_menu_chaine(titre):
	""" Demande une chaine de caractère à l'utilisateur.
		(fonction auxilière)

		titre (str): Le titre à afficher """

	dire(titre)
	return demander()


def afficher_menu_fichier(titre, existe=True):
	""" Demande le chemin vers un fichier. Il est possible de forcer le joueur à entrer un chemin
			existant.
		(fonction auxilière)

		titre (str): Le chemin
		existe (bool): Si True, accepte uniquement les chemins menant à des fichiers existants
			(True par défaut) """

	dire(titre)
	chemin = demander()

	if existe:
		# tant que le chemin donné ne pointe pas vers un fichier existant
		# on redemande un chemin
		while not fichier_existe(chemin):
			dire("Le fichier spécifié n'existe pas !")
			chemin = demander()
	else:
		# tant que le chemin donné n'est pas accessible (caractères interdits, droits, etc)
		# on redemande un chemin
		while not chemin_valide(chemin):
			dire("Le chemin spécifié est invalide !")
			chemin = demander()

	return chemin


def dire(msg):
	""" Affiche un message avec son auteur.
		(fonction auxilière)

		msg (str): Le message à afficher """

	print(NOM_ORDI + " > " + msg)


def demander():
	""" Demande au joueur d'entrer quelque chose. Arrête proprement le jeu en cas de Ctrl+C.
		(fonction auxilière) """

	# try/except permet d'attraper un arrêt forcé lors d'un appui sur CTRL+C
	try:
		return input(NOM_JOUEUR + " > ")
	except KeyboardInterrupt:
		deboggue("Arrêt par Ctrl+C du jeu")
		arreter()


def demander_entier(mini, maxi):
	""" Demande et redemande un entier tant que l'entrée utilisateur n'est pas un entier compris
			entre mini et maxi.
		(fonction auxilière)

		mini (int): Le minimal autorisé
		maxi (int): Entier maximal """

	entree = demander()

	# tant qu'on a pas obtenu d'entier compris entre mini et maxi on redemande
	while not nombre_valide(entree, mini, maxi):
		if mini == -float("inf") and maxi == float("inf"):
			dire("Vous devez entrer un entier")
		elif mini == -float("inf"):
			dire("Vous devez entrer un entier inférieur à {}".format(maxi))
		elif maxi == float("inf"):
			dire("Vous devez entrer un entier supérieur à {}".format(mini))
		else:
			dire("Vous devez entrer un entier compris entre {} et {}.".format(mini, maxi))
		entree = demander()

	return int(entree)


def deboggue(msg):
	""" Affiche un message précédé de 'DEBUG' pour aider au développement du jeu. Cette fonction
			peut être désactivée en passant DEBUG à False.

		msg (str): Le message à afficher """

	if DEBUG:
		print("DEBUG > {}".format(msg))


###################################################################################################
### Mode graphique ################################################################################
###################################################################################################

def creer_fenetre():
	""" Crée une fenêtre de taille définie.
		(fonction auxilière) """

	fenetre = tkinter.Tk()
	fenetre.resizable(False, False)
	fenetre.minsize(300, 0)
	fenetre.title("PolyAlliances")

	return fenetre


def redessiner_fenetre(fenetre):
	""" Tente de redessiner l'affichage. Si cette opération échoue le jeu s'arrête.
		(fonction auxilière) """

	# try/except permet de détecter si la fenêtre a été fermée
	# si c'est le cas, fenetre.update() génère une erreur que nous capturons
	# on peut ensuite arreter proprement le programme
	try:
		fenetre.update()
	except tkinter.TclError:
		arreter()


def charge_images():
	""" Charge les images du jeu dans la mémoire et renvoie le chemin des images
		(fonction auxilière) """

	chemin_images = "images"
	images = {}

	# on charge chaque image au format GIF
	for nom_image in obtenir_liste_fichiers(chemin_images, "gif"):
		chemin_image = creer_chemin(chemin_images, nom_image)
		images[nom_image] = tkinter.PhotoImage(file=chemin_image)

	return images


def effacer_zone_jeu(canvas):
	""" Efface la zone de jeu.
		(fonction auxilière)

		canvas (tkinter.Canvas): La zone de jeu """

	canvas.delete(tkinter.ALL)


def dessiner_texte(canvas, texte):
	""" Affiche un message dans la zone de jeu.
		(fonction auxilière)

		canvas (tkinter.Canvas): La zone de jeu
		texte (str): La zone à afficher """

	l, h = TAILLE_FENETRE
	canvas.create_text(int(l*0.5), int(h*0.9), text=texte, fill="white", font=("Arial", 18))


def dessiner_carte(canvas, images, carte, x, y):
	""" Dessine une carte aux coordonnées données. Renvoie l'identifiant de l'image dessinée sur le
			canvas.
		(fonction auxilière)

		canvas (tkinter.Canvas): La zone de jeu
		images (dict): Le dictionnaire référençant les images chargées
		carte (dict): La carte à afficher
		x (int): La position horizontale de la carte
		y (int): Sa positon verticale """

	v, c = carte["valeur"], carte["couleur"]
	nom_image = str(v) + "-" + c + ".gif"
	item = canvas.create_image(x, y, image=images[nom_image], anchor=tkinter.NW)

	return item


def dessiner_reussite(canvas, images, reussite, interact=lambda x: None):
	""" Affiche les cartes de la réussite dans la zone de jeu. Lie une fonction au clic sur chaque
			image dessinée.
		(fonction auxilière)
		
		canvas (tkinter.Canvas): La zone de jeu
		images (dict): Le dictionnaire référençant les images chargées
		reussite (list): Liste des cartes à afficher
		interact (function, method): Une fonction à appeler lors du clic sur une carte (lambda x:
			None par défaut). Le numéro du tas cliqué sera passé en paramètre (-1 pour la pioche) """

	# cette fonction est appelée par canvas.after après un certain délai
	def quand_dessine(carte, x, y, num_tas):
		item = dessiner_carte(canvas, images, carte, x, y)
		# l'argument x de cette fonction lambda reçoit l'évènement tkinter déclenché
		# mais nous n'en avons pas besoin
		canvas.tag_bind(item, "<ButtonPress-1>", lambda x: interact(num_tas))

	x, y = POS_DEPART

	for i, carte in enumerate(reussite):
		# On utilise after pour créer une légère animation sans bloquer l'execution du code
		canvas.after(i*10, quand_dessine, carte, x, y, i)

		# On revient à la ligne lorsque le nombre de carte maximal par ligne est atteint
		if (i+1) % MAX_CARTE_LIGNE:
			x += TAILLE_CARTE[0] + MARGE
		else:
			y += TAILLE_CARTE[1] + MARGE
			x = POS_DEPART[0]

	# On dessine la pioche en dernier
	carte = {"valeur": "dos", "couleur": random.choice(COULEUR_DOS)}
	quand_dessine(carte, x, y, -1)


def creer_zone_jeu(parent):
	""" Crée et renvoie la zone de jeu.
		(fonction auxilière)

		parent (tkinter.Wodget): Le widget parent de la zone de jeu """

	# pour éviter d'écrire toutes les options sur une seule ligne (trop long)
	# on les note toutes dans un dictionnaire qui sera passé en paramètre
	options = {
		"width": TAILLE_FENETRE[0],
		"height": TAILLE_FENETRE[1],
		"highlightthickness": 0,
		"bg": COULEUR_FOND
	}
	canvas = tkinter.Canvas(parent, **options)
	canvas.pack()

	return canvas


def creer_categorie(parent, nom, ancrage="nw"):
	""" Crée un LabelFrame afin de regrouper de futurs widgets.
		(fonction auxilière)

		parent (tkinter.Widget): Le widget parent
		nom (str): Le nom de la catégorie
		ancrage (str): Le point d'ancrage du titre de la catégorie ('nw' par défaut) """

	cadre = tkinter.LabelFrame(parent, text=nom, labelanchor=ancrage)
	cadre.pack(fill=tkinter.BOTH)

	return cadre


def creer_qcm_simple(parent, titre, *options):
	""" Crée un questionnaire à réponse unique avec un titre défini. Renvoie le widget englobant le
			questionnaire et une StringVar associée.
		(fonction auxilière)

		parent (tkinter.Widget): Le widget parent
		titre (str): Le titre du QCM
		options (*str): Les options du QCM """

	cadre = creer_categorie(parent, titre)
	
	# cette variable stock un entier correspondant à l'option choisie
	# on défini sa valeur par défaut sur 0 pour cocher dès le départ la première option
	qcm_var = tkinter.IntVar()
	qcm_var.set(0)

	for i, option in enumerate(options):
		bouton = tkinter.Radiobutton(cadre, text=option, value=i, variable=qcm_var)
		bouton.pack(anchor=tkinter.W)

	return cadre, qcm_var


def creer_qcm_liste(parent, titre, *options):
	""" Crée une liste d'éléments textuels. Renvoie le widget englobant la liste et une StringVar
			associée.
		(fonction auxilière)

		parent (tkinter.Widget): Le widget parent du QCM
		titre (str): Le titre du QCM
		options (*str): Les options du QCM """

	cadre = creer_categorie(parent, titre)

	liste = tkinter.Listbox(cadre, selectmode="single")
	liste.pack(fill=tkinter.BOTH)

	# on ajoute chaque option à la fin de la liste
	for option in options:
		liste.insert(tkinter.END, option)

	return cadre, liste


def creer_champs_saisi(parent, titre, fct_verif=lambda: True, desc=""):
	""" Crée un champs de saisie de texte avec un titre défini. Renvoie le widget englobant le
			champs et une StringVar associée.
		(fonction auxilière)

		parent (tkinter.Widget): Le widget parent du champs de saisi
		titre (str): Le titre du champs de saisi
		fct_verify (function, method): La fonction à appeler à chaque modification du champs
			(renvoie toujours True par défaut). Cette fonction doit renvoyer un booléen et est
			appelée juste avant chaque changement du champ de saisi avec le texte du champ en
			paramètre
		desc (str): Un texte de description ('' par défaut) """

	cadre = creer_categorie(parent, titre)

	if desc:
		label = creer_texte(cadre, desc)

	saisi_var = tkinter.StringVar()
	# on demande au champ de nous donner le texte en cours lors de l'appel de fct_verif
	commande = (parent.register(fct_verif), "%P") # %P renvoie au texte du champ de saisi
	saisi = tkinter.Entry(cadre, textvariable=saisi_var, validate="key", validatecommand=commande)
	saisi.pack(fill=tkinter.BOTH)

	return cadre, saisi_var


def creer_texte(parent, texte):
	""" Crée un texte.
		(fonction auxilière)

		parent (tkinter.Widget): Le widget parent du texte
		texte (str): Le texte à afficher """

	label = tkinter.Label(parent, text=texte)
	label.pack()

	return label


def creer_bouton(parent, texte, fct_clic):
	""" Crée un bouton avec un texte donné. Appelle fct_clic lors du clic sur celui-ci.
		(fonction auxilière)

		parent (tkinter.Widget): Le widget parent de ce bouton
		texte (str): Le texte à afficher sur le bouton
		fct_clic (function, method): La fonction à appeler lors du clic """

	bouton = tkinter.Button(parent, text=texte, command=fct_clic)
	bouton.pack()

	return bouton


def creer_checkbouton(parent, texte):
	""" Crée un bouton cochable avec un texte donné. Renvoie le bouton créé et la variable
			associée (vaut 1 si coché sinon 0).
		(fonction auxilière)

		parent (tkinter.Widget): Le widget parent de ce bouton
		texte (str): Le texte à afficher à coté du bouton """

	var = tkinter.IntVar()
	bouton = tkinter.Checkbutton(parent, text=texte, variable=var)
	bouton.pack(anchor=tkinter.W)

	return bouton, var


def creer_menu(fenetre, parent):
	""" Ajoute un bouton 'Continuer' et attend que l'utilisateur clic dessus pour continuer.
		(fonction auxilière)

		fenetre (tkinter.Tk): La fenêtre de jeu
		parent (tkinter.Widget): Le widget parent du menu """

	def quand_valide():
		boucle_info["attente"] = False

	boucle_info = {"attente": True}
	bouton_valide = creer_bouton(parent, "Continuer", quand_valide)

	while boucle_info["attente"]:
		redessiner_fenetre(fenetre)


def desactiver_categorie(cadre):
	""" Désactive tous les widgets enfants du cadre donné.
		(fonction auxilière)

		cadre (tkinter.Widget): Le cadre parent """

	for widget in cadre.winfo_children():
		widget.config(state=tkinter.DISABLED)


def activer_categorie(cadre):
	""" Active tous les widgets enfants du cadre donné.
		(fonction auxilière)

		cadre (tkinter.Widget): Le cadre parent """

	for widget in cadre.winfo_children():
		widget.config(state=tkinter.NORMAL)


def afficher_popup(fenetre, *messages):
	""" Affiche une fenêtre popup pour avertir le joueur.
		(fonction auxilière)

		fenetre (tkinter.Tk): La fenêtre de jeu
		messages (*str): Les messages à afficher """

	popup = tkinter.Toplevel()
	popup.title("Informations")
	popup.minsize(250, 50)
	popup.resizable(False, False)
	popup.grab_set()

	# on ajoute chaque message à la fenêtre popup
	for message in messages:
		label = tkinter.Label(popup, text=message)
		label.pack()

	bouton = tkinter.Button(popup, text="D'accord", command=popup.destroy)
	bouton.pack()

	fenetre.wait_window(popup) # on met en pose la fenêtre principale


def afficher_menu_programme(fenetre):
	""" Crée un menu proposant au joueur de choisir un programme.
		(fonction auxilière)

		fenetre (tkinter.Tk): La fenêtre de jeu """

	cadre = creer_categorie(fenetre, "Programme", "n")
	qcm_pro, var_pro = creer_qcm_simple(cadre, "Que voulez-vous faire ?", "Jouer", "Statistiques")
	creer_menu(fenetre, cadre)
	cadre.destroy()

	return var_pro.get()


def afficher_menu_jouer(fenetre):
	""" Crée un menu proposant au joueur de changer les réglages initiaux du jeu.
		(fonction auxilière)

		fenetre (tkinter.Tk): La fenêtre de jeu """

	# Cette fonction renvoie True si le nombre de tas entré est un entier supérieur à 2
	# utilisé par le champs de saisi pour savoir si la valeur entrée est correcte
	def quand_tape(texte):
		if texte:
			if texte.isdigit():
				return int(texte) >= 2
		return False

	# quand le mode change on active et désactive des sections devenues inutiles
	# mode manuel=affichage obligatoire
	# mode auto=pas de tas max pour gagner
	def quand_mode_change(*args):
		if var_mod.get():
			desactiver_categorie(saisi_tas)
			activer_categorie(qcm_aff)
			var_aff.set(0)
		else:
			desactiver_categorie(qcm_aff)
			activer_categorie(saisi_tas)
			var_aff.set(1)

	cadre = creer_categorie(fenetre, "Jouer", "n")
	qcm_mod, var_mod = creer_qcm_simple(cadre, "Mode de jeu", "Manuel", "Automatique")
	qcm_jeu, var_jeu = creer_qcm_simple(cadre, "Nombre de cartes", "32 cartes", "52 cartes")
	qcm_aff, var_aff = creer_qcm_simple(cadre, "Activer l'affichage", "Non", "Oui")
	saisi_tas, var_tas = creer_champs_saisi(cadre, "Nombre de tas maxi pour gagner", quand_tape, "Entier supérieur à 2")

	# on lance quand_mode_change à chaque fois que var_mod change
	var_mod.trace("w", quand_mode_change)
	quand_mode_change() # on l'appelle une première fois
	var_tas.set("2") # on défini le nombre de tas max par défaut à 2

	creer_menu(fenetre, cadre)
	cadre.destroy()

	# les variables correspondantes au mode, nb_carte, affiche et nb_tas_max sont renvoyées
	# attention les valeurs renvoyées sont brutes (elles doivent être traitées après)
	return var_mod.get(), var_jeu.get(), var_aff.get(), var_tas.get()


def afficher_menu_stats(fenetre):
	""" Affiche un menu proposant au joueur de régler la simulation.
		(fonction auxilière)

		fenetre (tkinter.Tk): La fenêtre de jeu """

	# Cette fonction renvoie True si le nombre de simulation est strictement positif
	# utilisé par le champs de saisi pour savoir si la valeur entrée est correcte
	def quand_tape(texte):
		if texte:
			if texte.isdigit():
				return int(texte) > 0
		return False

	cadre = creer_categorie(fenetre, "Statistiques", "n")
	qcm_jeu, var_jeu = creer_qcm_simple(cadre, "Nombre de cartes", "32 cartes", "52 cartes")
	qcm_ame, var_ame = creer_qcm_simple(cadre, "Pioches améliorées ?", "Non", "Oui")
	saisi_sim, var_sim = creer_champs_saisi(cadre, "Nombre de simulation par tas max", quand_tape, "Entier positif")

	var_sim.set("1") # nombre de simulations par défaut

	creer_menu(fenetre, cadre)
	cadre.destroy()

	# données brutes renvoyées (var_jeu.get() est une str)
	return var_sim.get(), var_jeu.get(), var_ame.get()


def afficher_menu_charge_pioche(fenetre):
	""" Affiche un menu proposant au joueur de choisir une pioche.
		(fonction auxilière)

		fenetre (tkinter.Tk): La fenêtre de jeu """

	# Active ou désactive la liste des pioches trouvées
	def quand_qcm_change(*args):
		if var_fic.get():
			activer_categorie(liste_pio)
		else:
			desactiver_categorie(liste_pio)

	pioches = obtenir_liste_pioche()

	cadre = creer_categorie(fenetre, "Pioche", "n")
	qcm_fic, var_fic = creer_qcm_simple(cadre, "Depuis un fichier ?", "Non", "Oui")
	liste_pio, var_pio = creer_qcm_liste(cadre, "Quelle pioche ?", *pioches)
	bouton_tri, var_tri = creer_checkbouton(liste_pio, "Autoriser les pioches truquées")

	# quand_qcm_change est appelée à chaque fois que var_fic change
	var_fic.trace("w", quand_qcm_change)
	quand_qcm_change() # on l'appelle une première fois

	creer_menu(fenetre, cadre)
	sel = var_pio.curselection()
	canvas.destroy()

	# si le joueur a selectionné une pioche dans la liste
	if sel:
		pioche = pioches[sel[0]]
	# sinon on choisi un pioche par défaut (dans le cas ou il existe des fichiers pioches)
	elif pioches:
		deboggue("Aucune pioche sélectionnée ! Utilisation de la première pioche")
		pioche = pioches[0]
	else:
		deboggue("Aucune pioche ne peut être chargée ! Passage en mode aléatoire")
		var_fic.set(0)

	if var_fic.get():
		return pioche, bool(var_tri.get())
	# dans le cas ou on ne charge pas la pioche depuis un fichier
	# on renvoie None et False (pas de triche)
	return None, False


def afficher_menu_sauve_pioche(fenetre):
	""" Affiche un menu proposant au joueur de sauvegarder une pioche.
		(fonction auxilière)

		fenetre (tkinter.Tk): La fenêtre de jeu """

	# Active ou désactive le champ de saisi du nom de la pioche
	def quand_qcm_change(*args):
		if var_fic.get():
			activer_categorie(saisi_pio)
		else:
			desactiver_categorie(saisi_pio)

	cadre = creer_categorie(fenetre, "Sauvegarde", "n")
	qcm_fic, var_fic = creer_qcm_simple(cadre, "Sauvegarder ?", "Non", "Oui")
	saisi_pio, var_pio = creer_champs_saisi(cadre, "Nom de la pioche")

	# lance quand_qcm_change quand var_fic change
	var_fic.trace("w", quand_qcm_change)
	quand_qcm_change() # on l'appelle une première fois

	creer_menu(fenetre, cadre)

	cadre.destroy()

	if var_fic.get():
		return var_pio.get()
	# Si le joueur ne veut pas sauvegarder la pioche on renvoie None
	return None


###################################################################################################
### Utile jeu #####################################################################################
###################################################################################################

def carte_to_chaine(carte):
	""" Renvoie une chaine de caractère représentant une carte donnée.
		
		carte (dict): La carte à représenter """
	
	# rjust(2) permet d'ajouter des "0" à gauche si la chaine fait moins de 2 caractères
	return str(carte["valeur"]).rjust(2) + COULEURS[carte["couleur"]]


def carte_from_chaine(chaine):
	""" Renvoie une nouvelle carte à partir d'une chaine de caractère.
		(fonction auxilière)

		chaine (str): La chaine à partir de laquelle créer une carte """

	valeur, couleur = chaine.split("-")

	# on converti la valeur en un entier si c'est ni un As, ni un Roi, ni une Dame, ni un Valet
	# ni le dos d'une carte (nécessaire pour l'extension graphique)
	if valeur not in ("V", "D", "R", "A", "dos"):
		valeur = int(valeur)

	return {"valeur": valeur, "couleur": couleur}


def genere_jeu(nb_cartes=32):
	""" Génère un jeu de cartes renvoyé sous forme d'une liste. Le jeu est trié.
		(fonction auxilière)

		nb_cartes (int): Le nombre de cartes du jeu (32 par défaut) """

	cartes = []

	for valeur in VALEURS:
		# on converti la valeur en un entier si c'est ni un As, ni un Roi, ni une Dame, ni un Valet
		if valeur not in ("V", "D", "R", "A"):
			valeur = int(valeur)

		for couleur in COULEURS:
			cartes.append({"valeur": valeur, "couleur": couleur})

			# si on a suffisamment de cartes, on s'arrête en les renvoyant
			if len(cartes) == nb_cartes:
				return cartes


def init_pioche_alea(nb_cartes=32):
	""" Renvoie une liste mélangée de toutes les cartes du jeu. 
		
		nb_cartes (int): Nombre de cartes du jeu (32 par défaut) """
	
	jeu = genere_jeu(nb_cartes)
	random.shuffle(jeu) # mélange la liste des cartes
	return jeu


def alliance(carte1, carte2):
	""" Renvoie True si les deux cartes sont de même valeur ou de même couleur (sinon False).
		
		carte1 (dict): La première carte à comparer
		carte2 (dict): La deuxième carte à comparer """

	return carte1["valeur"] == carte2["valeur"] or carte1["couleur"] == carte2["couleur"]


def saut_si_possible(liste_tas, num_tas):
	""" Si possible effectue le saut d'un tas donné et renvoie True sinon renvoie False.
		
		liste_tas (list): Liste des cartes visibles de la réussite
		num_tas (int): Numéro du tas à faire sauter (de gauche à droite en partant de 0) """
	
	# si le tas demandé n'est pas valide on renvoie False
	if num_tas > 0 and num_tas < len(liste_tas) - 1:
		# sinon on tente de faire un saut
		if alliance(liste_tas[num_tas-1], liste_tas[num_tas+1]):
			liste_tas.pop(num_tas-1)
		
			return True
	return False


def piocher(liste_tas, pioche):
	""" Pioche une carte et ajoute cette carte à la réussite.
		(fonction auxilière)

		liste_tas (list): Liste des cartes visibles de la réussite
		pioche (list): Liste des cartes de la pioche """

	# on ne pioche uniquement s'il reste des cartes dans la pioche
	if pioche:
		liste_tas.append(pioche.pop())


def une_etape_reussite(liste_tas, pioche, affiche=False):
	""" Place la première carte de la pioche à la suite de la réussite et effectue les sauts
			nécessaires (la réussite peut être affichée à chaque étape).
		
		liste_tas (list): Liste des cartes visibles de la réussite
		pioche (list): Liste des cartes de la pioche
		affiche (bool): Si True, affiche la réussite après chaque changement (False par défaut) """
	
	piocher(liste_tas, pioche)

	# on affiche une première fois les cartes
	if affiche:
		afficher_reussite(liste_tas)

	# numéro du tas à faire sauter
	num_tas = 1

	while num_tas < len(liste_tas) - 1:
		if saut_si_possible(liste_tas, num_tas):
			if affiche:
				afficher_reussite(liste_tas)
	
			# si un saut est fait on recommence depuis le début à faire sauter des tas
			num_tas = 0
		num_tas += 1


def verifier_pioche(pioche, nb_cartes=32):
	""" Vérifie si une pioche n'est pas truquée (pas de cartes en double et nombre de cartes
			correct).
		(fonction extension)

		pioche (list): La liste des cartes de la pioche
		nb_cartes (int): Le nombre de cartes du jeu (32 par défaut) """

	# s'il n'y a pas le bon nombre de carte on peut déjà retourner False
	if len(pioche) != nb_cartes:
		return False

	# on fait une copie de la pioche avant de la vérifier
	pioche = pioche[:]
	testees = []

	# tant qu'il reste des cartes
	while pioche:
		# on pioche une carte
		carte = pioche.pop()

		# si la carte en cours a déjà été retournée alors on s'arrête
		if carte in testees:
			break

		# sinon on l'ajoute à la liste des cartes testées
		testees.append(carte)

	# renvoie True si toutes les cartes ont pu être testées
	return len(testees) == nb_cartes


def chaine_est_pioche(chaine):
	""" Renvoie True si chaine représente une pioche sinon False.
		(fonction auxilière)

		chaine (str): La chaine à tester """
		
	for carte in chaine.split():
		# les chaines vides sont acceptées (exemple à la fin du fichier)
		if carte:
			attr = carte.split("-")

			# carte ne représente pas une carte...
			# s'il n'y a pas 2 attributs
			if len(attr) != 2:
				return False
			# ou si le premier attribut n'est pas une valeur valide
			elif attr[0] not in VALEURS:
				return False
			# ou si le deuxième n'est pas une couleur valide
			elif attr[1] not in COULEURS:
				return False
	return True


def nombre_valide(nombre, mini, maxi):
	""" Renvoie un entier compris entre mini et maxi demandé au joueur.
		(fonction auxilière)

		nombre (object): Un objet représentant un entier
		mini (int): Entier minimal accepté
		maxi (int): Entier maximal """

	try:
		nombre = int(nombre)
	except ValueError:
		return False

	if nombre >= mini and nombre <= maxi:
		return True
	return False


def obtenir_liste_pioche():
	""" Recherche tous les fichiers susceptible de d'être une pioche dans le répertoire courant.
		(fonction auxilière) """

	nom_fichiers = obtenir_liste_fichiers(".", "txt")
	fichiers_valides = []

	for nom_fichier in nom_fichiers:
		if fichier_pioche_valide(nom_fichier):
			fichiers_valides.append(nom_fichier)

	return fichiers_valides


###################################################################################################
### Statistiques ##################################################################################
###################################################################################################

def res_multi_simulation(nb_sim, nb_cartes=32, pioche_amelioree=False):
	""" Réalise nb_sim simulations et renvoie la liste du nombre de tas restants après chaque
			simulation.

		nb_sim (int): Le nombre de simulation à effectuer
		nb_cartes (int): Le nombre de cartes de chaque jeu (32 par défaut) """

	resultats = []

	for sim in range(nb_sim):
		deboggue("Simulation n" + str(sim))
		pioche = init_pioche_alea(nb_cartes)
		liste_tas = []

		if pioche_amelioree:
			pioche, amel = meilleur_echange_consecutif(pioche)
			deboggue("Il est possible d'améliorer la pioche pour gagner {} tas".format(amel))
		
		while pioche:
			une_etape_reussite(liste_tas, pioche)

		resultats.append(len(liste_tas))
	return resultats


def statistiques_nb_tas(nb_sim, nb_cartes=32, pioche_amelioree=False):
	""" Calcule et affiche la moyenne, le minimum et le maximum de tas restants après nb_sim
			simulations. Affiche également le nombre de tas > et < à la moyenne.

		nb_sim (int): Le nombre de simulation à effectuer
		nb_cartes (int): Le nombre de cartes de chaque jeu (32 par défaut) """

	resultats = res_multi_simulation(nb_sim, nb_cartes, pioche_amelioree)
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


def probabilite_victoire(nb_sim, nb_cartes=32, pioche_amelioree=False):
	""" Détermine les chances de gagner en fonction du nombre de tas maximum autorisés.

		nb_sim (int): Le nombre de simulations à chaque test
		nb_cartes (int): Le nombre de carte du jeu (32 par défaut) """

	victoires = []

	for nb_tas_max in range(nb_cartes):
		deboggue("Calcul du taux de victoire pour {} tas max".format(nb_tas_max))
		resultats = res_multi_simulation(nb_sim, nb_cartes, pioche_amelioree)
		nb_victoires = sum(resultat <= nb_tas_max for resultat in resultats)
		victoires.append(nb_victoires / len(resultats))

	return victoires


def meilleur_echange_consecutif(pioche):
	""" """

	nb_tas_depart = len(reussite_mode_auto(pioche))

	meilleur_pioche = pioche
	meilleur_tas = nb_tas_depart

	for echange in range(len(pioche)-1):
		pioche2 = pioche[:]
		pioche2[echange], pioche2[echange+1] = pioche2[echange+1], pioche2[echange]
		nb_tas = len(reussite_mode_auto(pioche))

		if nb_tas < meilleur_tas:
			meilleur_tas = nb_tas
			meilleur_pioche = pioche2

	return meilleur_pioche, nb_tas_depart - nb_tas


def creer_graphique(nb_sim, nb_cartes=32, pioche_amelioree=False):
	""" Crée un graphique établi à partir d'un nombre de simulations données.
		(fonction auxilière)

		nb_sim (int): Le nombre de simulations
		nb_cartes (int): Le nombre de cartes du jeu (32 par défaut)
		pioche_amelioree (bool): Si True, modifie légèrement la pioche pour augmenter les chances
			de gagner """

	figure = plt.figure()
	figure.canvas.set_window_title("PolyAlliances statistiques")

	plt.plot(probabilite_victoire(nb_sim, nb_cartes, pioche_amelioree))
	plt.title("Probabilité de gagner en fonction du nombre de tas maximum")
	plt.xlabel("Nombre de tas maximum")
	plt.ylabel("Probabilité de gagner")
	plt.show()


###################################################################################################
### Fichiers ######################################################################################
###################################################################################################

def obtenir_liste_fichiers(chemin_dossier, *extensions):
	""" Renvoie la liste des fichiers contenu dans un dossier donné. Il est possible de spécifier
		l' / les extension(s) voulue(s).

		chemin_dossier (str): Le chemin vers un dossier
		extensions (*str): Les extensions autorisées (ne rien préciser pour tout autoriser) """

	if fichier_existe(chemin_dossier):
		fichiers = os.listdir(chemin_dossier)

		if extensions:
			return [fichier for fichier in fichiers if os.path.splitext(fichier)[-1][1:] in extensions]
		return fichiers
	else:
		deboggue("Le dossier '{}' n'existe pas".format(chemin_dossier))
		return []


def fichier_existe(chemin_fichier):
	""" Renvoie True si le fichier existe (sinon False).

		chemin_fichier (str): Le chemin vers le fichier à tester """

	return os.path.exists(chemin_fichier)


def creer_chemin(dossier, *sous_dossiers):
	""" Créer une chaine représentant le chemin vers un fichier (ou dossier) à partir du nom des
		dossier, sous_dossiers et fichier donnés.

		dossier (str): Le dossier parent
		sous_dossiers (*str): Les sous-dossiers ou fichier """

	return os.path.join(dossier, *sous_dossiers)


def obtenir_nom_reel(nom_fichier):
	""" Renvoie le nom du fichier sans extension.

		nom_fichier (str): Le nom du fichier """
		
	return os.path.splitext(nom_fichier)[0]


def arreter():
	""" Arrête le jeu sans attendre. """

	deboggue("Fin du jeu")
	sys.exit()


def chemin_valide(chemin):
	""" Renvoie True si le chemin donné est accessible.
		(fonction auxiliaire)

		chemin (str): Le chemin à tester """

	chemin = os.path.abspath(chemin)
	return os.path.exists(chemin) or os.access(os.path.dirname(chemin), os.W_OK)


def init_pioche_fichier(chemin_fichier):
	""" Renvoie la liste des cartes écrites dans un fichier.
		
		chemin_fichier (str): Chemin vers le fichier contenant la liste des cartes """

	deboggue("Chargement de la pioche depuis '" + chemin_fichier + "'")
	with open(chemin_fichier, "r") as fichier:
		# pour chaque ensemble "v-c" chargé depuis le fichier on crée une carte
		# "if chaine" empêche de charger une chaine vide
		cartes = [carte_from_chaine(chaine) for chaine in fichier.read().split() if chaine]
	return cartes


def ecrire_fichier_reussite(nom_fichier, pioche):
	""" Ecrit la pioche dans un fichier. 
		
		nom_fichier (str): Nom du fichier dans lequel écrire la pioche
		pioche (list): Liste des cartes de la pioche """

	deboggue("Sauvegarde de la pioche dans '" + nom_fichier + "'")
	with open(nom_fichier, "w") as fichier:
		for carte in pioche:
			fichier.write(str(carte['valeur'])+"-"+carte['couleur']+" ")


def fichier_pioche_valide(nom_fichier):
	""" Renvoie True si le fichier donné contient une pioche sinon False.
		(fonction auxilière)

		nom_fichier (str): Le nom du fichier à charger """

	# on charge son contenu
	with open(nom_fichier, "r") as file:
		contenu = file.read()

	# on regarde s'il est valide
	return chaine_est_pioche(contenu)


###################################################################################################
### Principales ###################################################################################
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

	# tant qu'il reste des cartes
	while pioche:
		une_etape_reussite(liste_tas, pioche, affichage)

	return liste_tas


def reussite_mode_manuel(pioche, nb_tas_max=2):
	""" Fait jouer l'utilisateur avec la pioche donnée en affichant des menus. La partie est gagnée
			si le joueur termine avec un nombre de tas inférieur ou égal à nb_tas_max.
		
		pioche (list): La liste des cartes de la pioche
		nb_tas_max (int): Nombre de tas restant maximum pour gagner (2 par défaut) """
	
	liste_tas = []
	pioche = pioche[:]
	menu = ("Choisissez une action", "Piocher une carte", "Effectuer un saut", "Quitter")

	piocher(liste_tas, pioche)
	piocher(liste_tas, pioche)
	piocher(liste_tas, pioche)

	while pioche:
		# à chaque tour de boucle on affiche les tas visibles
		dire("Voici les tas visibles")
		afficher_reussite(liste_tas)

		# on demande une action au joueur
		mode = afficher_menu_qcm(*menu)

		# mode 0 = piocher
		if mode == 0:
			piocher(liste_tas, pioche)

		# mode 1 = faire sauter
		elif mode == 1:
			texte = "Quel tas faire sauter ? (ne s'applique ni au 1er ni au dernier tas)"
			saut = afficher_menu_entier(texte, 1, len(liste_tas) - 2)

			if saut_si_possible(liste_tas, saut):
				dire("Un saut a été effectué !")
			else:
				dire("Impossible de faire sauter ce tas !")

		# mode 2 = quitter
		elif mode == 2:
			dire("Vous avez quitté la partie !")
			dire("Voici les cartes qu'il restait dans la pioche")
			afficher_reussite(pioche)
			return liste_tas

	# on affiche un message différent si le joueur a gagné
	if len(liste_tas) > nb_tas_max:
		dire("Vous avez perdu(e) !")
	else:
		dire("Vous avez gagné(e) !")
	dire("Il reste {} tas.".format(len(liste_tas)))

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

	choix_pioche = True

	# on demande l'origine de la pioche tant que celle-ci n'est pas valide
	while choix_pioche:
		depuis_fichier = afficher_menu_qcm("Charger la pioche depuis un fichier ?", "Non", "Oui")

		# si on charge la pioche depuis un fichier
		if depuis_fichier:
			nom_fichier = afficher_menu_fichier("Entrez le nom du fichier à charger")
			# si ce fichier contient une pioche on le charge
			if fichier_pioche_valide(nom_fichier):
				pioche = init_pioche_fichier(nom_fichier)

				# si cette pioche est truquée on avertit le joueur
				if not verifier_pioche(pioche, nb_cartes):
					dire("Triche détectée ! La pioche est truquée !")
					pioche_acceptee = afficher_menu_qcm("Voulez-vous continuer avec cette pioche ?", "Non", "Oui")

					if pioche_acceptee:
						choix_pioche = False
				else:
					choix_pioche = False
			else:
				dire("Ce fichier ne contient pas de pioche valide !")
		else:
			# sinon on génère une pioche aléatoire
			pioche = init_pioche_alea(nb_cartes)
			choix_pioche = False

	# le jeu commence véritablement ici
	liste_tas = []

	if mode == "auto":
		liste_tas = reussite_mode_auto(pioche, affiche)
		dire("La jeu est terminé !")
		dire("Il reste {} tas.".format(len(liste_tas)))
	elif mode == "manuel":
		liste_tas = reussite_mode_manuel(pioche, nb_tas_max)
	else:
		deboggue("Mode non reconnu !")

	# enfin on demande de sauvegarder la pioche
	if not depuis_fichier:
		sauve_pioche = afficher_menu_qcm("Enregistrer la pioche ?", "Non", "Oui")

		if sauve_pioche:
			nom_fichier = afficher_menu_fichier("Entrez le nom du fichier où enregistrer la pioche", False)
			ecrire_fichier_reussite(nom_fichier, pioche)

	return liste_tas


def preparer_reussite():
	""" Demande le mode de jeu, le nombre de carte et d'autres informations essentielles au
		démarrage du jeu.
		Ne prend aucun argument.
		(fonction auxilière) """

	dire("Bienvenu dans La réussite des alliances !")
	# on demande le mode de jeu et le nombre de cartes
	mode = afficher_menu_qcm("Quel mode ?", "Manuel", "Automatique")
	nb_cartes = 32 + 20 * afficher_menu_qcm("Quel jeu ?", "32 cartes", "52 cartes")

	if mode:
		dire("Vous avez choisi le mode automatique")
		affiche = bool(afficher_menu_qcm("Voulez-vous activer l'affichage ?", "Non", "Oui"))
		tas_max = 2
		mode = "auto"
	else:
		dire("Vous avez choisi le mode manuel")
		tas_max = afficher_menu_entier("Nombre de tas maximum pour gagner", 2, nb_cartes)
		affiche = True
		mode = "manuel"

	liste_tas = lance_reussite(mode, nb_cartes, affiche, tas_max)
	dire("Cette partie s'est terminée avec {} tas".format(len(liste_tas)))


def preparer_statistiques():
	""" Propose au joueur de choisir le nombre de cartes et de simulations faites pour établir
			des statistiques.
		(fonction auxiliaire) """

	# on demande le nombre de cartes et de simulations
	nb_cartes = 32 + 20 * afficher_menu_qcm("Quel jeu ?", "32 cartes", "52 cartes")
	nb_sim = afficher_menu_entier("Nombre de simulation par tas max", 1, float("inf"))
	pioche_amelioree = afficher_menu_qcm("Utiliser des pioches améliorées ?", "Non", "Oui")

	statistiques_nb_tas(nb_sim, nb_cartes, pioche_amelioree)
	dire("Chargement du graphique...")
	creer_graphique(nb_sim, nb_cartes, pioche_amelioree)


def choisir_programme():
	""" Propose au joueur de choisir entre jouer une partie et simplement lancer le programme de
			statistiques.
		(fonction auxiliaire) """

	# on propose de lancer l'un des deux programmes
	prog = afficher_menu_qcm("Quel voulez-vous faire ?", "Jouer", "Statistiques")

	if prog:
		preparer_statistiques()
	else:
		preparer_reussite()

# Version graphique des fonctions précédentes

def reussite_mode_auto_gui(fenetre, images, pioche):
	""" Joue automatiquement la réussite en partant sur la pioche donnée.
		(fonction auxiliaire)

		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire des images chargées
		pioche (list): La liste des cartes de la pioche """

	def tick():
		# on efface les cartes, on effectue une étape puis on les redessine
		effacer_zone_jeu(canvas)
		une_etape_reussite(liste_tas, pioche)
		dessiner_reussite(canvas, images, liste_tas)

		# cette fonction s'appelle elle même toutes les 0.5s
		if pioche:
			fenetre.after(500, tick)

	liste_tas = []
	pioche = pioche[:]

	# on crée une zone de jeu et on dessine une première fois les cartes
	canvas = creer_zone_jeu(fenetre)
	dessiner_reussite(canvas, images, pioche)
	fenetre.after(500, tick)

	# on redessine la fenêtre tant qu'il reste des cartes
	while pioche:
		redessiner_fenetre(fenetre)

	# on affiche un message une fois la partie finie
	afficher_popup(fenetre, "Le jeu est terminé !", "Il reste {} tas.".format(len(liste_tas)))
	canvas.destroy()

	return liste_tas


def reussite_mode_manuel_gui(fenetre, images, pioche, nb_tas_max=2):
	""" Fait jouer l'utilisateur avec la pioche donnée. La partie est gagnée si le joueur termine
			avec un nombre de tas inférieur ou égal à nb_tas_max.
		(fonction auxiliaire)

		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire des images chargées
		pioche (list): La liste des cartes de la pioche
		nb_tas_max (int): Nombre de tas restant maximum pour gagner (2 par défaut) """

	# cette fonction est appelée à chaque clic sur une carte
	def quand_clic(num_tas):
		effacer_zone_jeu(canvas)

		# le tas numéro -1 correspond à la pioche
		if num_tas == -1:
			piocher(liste_tas, pioche)
		# on affiche un message en fonction de l'action effectuée (saut ou non)
		elif saut_si_possible(liste_tas, num_tas):
			dessiner_texte(canvas, "Un saut a été effectué")
		else:
			dessiner_texte(canvas, "Impossible de faire sauter cette carte")
		
		# on redessine les cartes
		dessiner_reussite(canvas, images, liste_tas, quand_clic)

	liste_tas = []
	pioche = pioche[:]

	piocher(liste_tas, pioche)
	piocher(liste_tas, pioche)
	piocher(liste_tas, pioche)

	# on crée une zone de jeu et on affiche une première fois les cartes
	canvas = creer_zone_jeu(fenetre)
	dessiner_reussite(canvas, images, liste_tas, quand_clic)

	# tant qu'il reste des cartes dans la pioche on redessine la fenêtre
	while pioche:
		redessiner_fenetre(fenetre)

	# on affiche un message une fois la partie finie
	if len(liste_tas) > nb_tas_max:
		message = "Vous avez perdu !"
	else:
		message = "Vous avez gagné !"
	afficher_popup(fenetre, message, "Il reste {} tas.".format(len(liste_tas)))

	canvas.destroy()


def lance_reussite_gui(fenetre, images, mode, nb_cartes=32, affiche=False, nb_tas_max=2):
	""" Crée la pioche, lance une partie puis sauvegarde la pioche en mode graphique.
		(fonction auxiliaire)

		fenetre (pygame.surface.Surface): La fenêtre de jeu
		images (dict): Le dictionnaire des images chargées
		mode (str): Le mode de jeu
		nb_cartes (int): Nombre de cartes du jeu (32 par défaut)
		affiche (bool): Si True en mode automatique, affiche la partie (False par défaut)
		nb_tas_max (int): Nombre de tas maximum pour gagner """

	choix_pioche = True

	while choix_pioche:
		nom_fichier, truquee = afficher_menu_charge_pioche(fenetre)

		if nom_fichier:
			pioche = init_pioche_fichier(nom_fichier)
		else:
			pioche = init_pioche_alea(nb_cartes)

		# si la triche est autorisée pas besoin de vérifier
		if truquee:
			choix_pioche = False
		# sinon on verifie qu'elle ne soit pas truquée
		elif verifier_pioche(pioche, nb_cartes):
			choix_pioche = False
		# dans le cas contraire on averti le joueur
		else:
			afficher_popup(fenetre, "La pioche choisie est truquée !")

	# le jeu commence véritablement ici
	liste_tas = []

	if mode == "auto":
		if affiche:
			liste_tas = reussite_mode_auto_gui(fenetre, images, pioche)
		else:
			liste_tas = reussite_mode_auto(pioche)
			# même sans affichage on aimerait connaitre le résultat de la partie
			afficher_popup(fenetre, "Le jeu est terminé !", "Il reste {} tas.".format(len(liste_tas)))
	elif mode == "manuel":
		liste_tas = reussite_mode_manuel_gui(fenetre, images, pioche, nb_tas_max)
	else:
		deboggue("Mode non reconnu !")

	# on propose d'enregistrer la pioche
	nom_fichier = afficher_menu_sauve_pioche(fenetre)

	if nom_fichier:
		ecrire_fichier_reussite(nom_fichier, pioche)

	return liste_tas


def preparer_reussite_gui(fenetre, images):
	""" Même chose que preparer_reussite mais en mode graphique.
		(fonction auxiliaire)

		fenetre (tkinter.Tk): La fenêtre de jeu
		images (dict): Le dictionnaire des images du jeu """

	modes = ("manuel", "auto")
	# on récupère les données brutes de afficher_menu_jouer
	mode, nb_cartes, affiche, nb_tas_max = afficher_menu_jouer(fenetre)
	
	# et on les convertit
	mode = modes[mode]
	nb_cartes = 32 + 20 * nb_cartes
	affiche = bool(affiche)
	nb_tas_max = int(nb_tas_max)

	lance_reussite_gui(fenetre, images, mode, nb_cartes, affiche, nb_tas_max)


def preparer_statistiques_gui(fenetre):
	""" Même chose que preparer_statistiques mais en mode graphique.
		(fonction auxiliaire)

		fenetre (tkinter.Tk): La fenêtre de jeu """

	# on récupère les données brutes de afficher_menu_stats
	nb_sim, nb_cartes, pioche_amelioree = afficher_menu_stats(fenetre)

	# et on les convertit
	nb_sim = int(nb_sim)
	nb_cartes = 32+20*nb_cartes
	pioche_amelioree = bool(pioche_amelioree)

	# on détruit la fenêtre avant de lancer le programme de statistiques
	fenetre.destroy()
	statistiques_nb_tas(nb_sim, nb_cartes, pioche_amelioree)
	dire("Chargement du graphique...")
	creer_graphique(nb_sim, nb_cartes, pioche_amelioree)


def choisir_programme_gui(fenetre, images):
	""" Même chose que choisir_programme mais en mode graphique.
		(fonction auxiliaire)

		fenetre (tkinter.Tk): La fenêtre de jeu
		images (dict): Le dictionnaire des images du jeu """

	# on propose de choisir le programme
	prog = afficher_menu_programme(fenetre)

	if prog:
		preparer_statistiques_gui(fenetre)
	else:
		preparer_reussite_gui(fenetre, images)


def main():
	""" Fonction principale. Initialise l'interface et lance le jeu.
		Ne prend aucun argument.
		(fonction auxiliaire) """
	
	if FORCE_CONSOLE:
		deboggue("Le jeu est en mode console")
		choisir_programme()
	else:
		deboggue("Le jeu est en mode graphique")
		fenetre = creer_fenetre()
		images = charge_images()
		choisir_programme_gui(fenetre, images)

	deboggue("Arrêt normal")


if __name__ == "__main__":
	# le programme commence véritablement ici
	main()