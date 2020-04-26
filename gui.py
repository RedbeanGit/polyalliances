#
# PolyAlliances
#
# Date de création: 14/04/2020
# Binome: Julien Dubois, Philippe Guiraud (PA2-B09)
# Version Python: 3.8
#

""" Propose des fonctions liées à l'affichage. """

import tkinter

from config import *
from jeu import *
from utile import *


def creer_fenetre():
	""" Crée une fenêtre de taille définie. """

	fenetre = tkinter.Tk()
	fenetre.resizable(False, False)
	fenetre.minsize(300, 0)
	fenetre.title("PolyAlliances")

	return fenetre


def redessiner_fenetre(fenetre):
	""" Tente de redessiner l'affichage. Si cette opération échoue le jeu s'arrête. """

	try:
		fenetre.update()
	except tkinter.TclError:
		arreter()


def charge_images():
	""" Charge les images du jeu dans la mémoire et renvoie le chemin des images """

	chemin_images = creer_chemin("ressources", "images")
	images = {}

	for nom_image in obtenir_liste_fichiers(chemin_images, "gif"):
		chemin_image = creer_chemin(chemin_images, nom_image)
		images[nom_image] = tkinter.PhotoImage(file=chemin_image)

	return images


def effacer_dessin(canvas):
	""" Efface la zone de jeu.

		canvas (tkinter.Canvas): La zone de jeu """

	canvas.delete(tkinter.ALL)


def dessiner_texte(canvas, texte):
	""" Affiche un message dans la zone de jeu.

		canvas (tkinter.Canvas): La zone de jeu
		texte (str): La zone à afficher """

	l, h = config.TAILLE_FENETRE
	canvas.create_text(int(l*0.5), int(h*0.9), text=texte, fill="white", font=("Arial", 18))


def dessiner_carte(canvas, images, carte, x, y):
	""" Dessine une carte aux coordonnées données.

		canvas (tkinter.Canvas): La zone de jeu
		images (dict): Le dictionnaire référençant les images chargées
		carte (dict): La carte à afficher
		x (int): La position horizontale de la carte
		y (int): Sa positon verticale
		interact ("""

	v, c = carte["valeur"], carte["couleur"]
	nom_image = str(v) + "-" + c + ".gif"
	item = canvas.create_image(x, y, image=images[nom_image], anchor=tkinter.NW)

	return item


def dessiner_reussite_gui(canvas, images, reussite, interact=lambda x: None):
	""" Affiche les cartes de la réussite en grille et renvoie les identifiants des widgets créés.
		
		images (dict): Le dictionnaire des chemins vers les images chargées
		reussite (list): Liste contenant les cartes à afficher """

	def quand_dessine(carte, x, y, num_tas):
		item = dessiner_carte(canvas, images, carte, x, y)
		canvas.tag_bind(item, "<ButtonPress-1>", lambda x: interact(num_tas))

	x, y = POS_DEPART

	for i, carte in enumerate(reussite):
		canvas.after(i*10, quand_dessine, carte, x, y, i)

		if (i+1) % MAX_CARTE_LIGNE:
			x += TAILLE_CARTE[0] + MARGE
		else:
			y += TAILLE_CARTE[1] + MARGE
			x = POS_DEPART[0]

	carte = {"valeur": "dos", "couleur": "bleu"}
	quand_dessine(carte, x, y, -1)


def creer_zone_jeu(parent):
	""" Crée et renvoie la zone de jeu.

		parent (tkinter.Wodget): Le widget parent de la zone de jeu """

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

		parent (tkinter.Widget): Le widget parent
		nom (str): Le nom de la catégorie
		ancrage (str): Le point d'ancrage du titre de la catégorie ('nw' par défaut) """

	cadre = tkinter.LabelFrame(parent, text=nom, labelanchor=ancrage)
	cadre.pack(fill=tkinter.BOTH)

	return cadre


def creer_qcm_simple(parent, titre, *options):
	""" Crée un questionnaire à réponse unique avec un titre défini. Renvoie le widget englobant le
			questionnaire et une StringVar associée.

		parent (tkinter.Widget): Le widget parent
		titre (str): Le titre du QCM
		options (*str): Les options du QCM """

	cadre = creer_categorie(parent, titre)
	
	qcm_var = tkinter.IntVar()
	qcm_var.set(0)

	for i, option in enumerate(options):
		bouton = tkinter.Radiobutton(cadre, text=option, value=i, variable=qcm_var)
		bouton.pack(anchor=tkinter.W)

	return cadre, qcm_var


def creer_champs_saisi(parent, titre, fct_verif=lambda: True, desc=""):
	""" Crée un champs de saisie de texte avec un titre défini. Renvoie le widget englobant le
			champs et une StringVar associée.

		parent (tkinter.Widget): Le widget parent du champs de saisi
		titre (str): Le titre du champs de saisi
		fct_verify (function, method): La fonction à appeler à chaque modification du champs
			(renvoie toujours True par défaut)
		desc (str): Un texte de description ('' par défaut) """

	cadre = creer_categorie(parent, titre)

	if desc:
		label = creer_texte(cadre, desc)

	saisi_var = tkinter.StringVar()
	commande = (parent.register(fct_verif), '%P')
	saisi = tkinter.Entry(cadre, textvariable=saisi_var, validate="key", validatecommand=commande)
	saisi.pack(fill=tkinter.BOTH)

	return cadre, saisi_var


def creer_texte(parent, texte):
	""" Crée un texte.

		parent (tkinter.Widget): Le widget parent du texte
		texte (str): Le texte à afficher """

	label = tkinter.Label(parent, text=texte)
	label.pack()

	return label


def creer_bouton(parent, texte, fct_clic):
	bouton = tkinter.Button(parent, text=texte, command=fct_clic)
	bouton.pack()

	return bouton


def creer_qcm_liste(parent, titre, *options):
	""" Crée une liste d'éléments textuels. Renvoie le widget englobant la liste et une StringVar
			associée. """

	cadre = creer_categorie(parent, titre)
	qcm_var = tkinter.StringVar()

	if options:
		qcm_var.set(options[0])

	liste = tkinter.Listbox(cadre, selectmode="single")
	liste.pack(fill=tkinter.BOTH)

	for option in options:
		liste.insert(tkinter.END, option)

	return cadre, qcm_var


def desactiver_categorie(cadre):
	""" Désactive tous les widgets enfants du cadre donné.

		cadre (tkinter.Widget): Le cadre parent """

	for widget in cadre.winfo_children():
		widget.config(state=tkinter.DISABLED)


def activer_categorie(cadre):
	""" Active tous les widgets enfants du cadre donné.

		cadre (tkinter.Widget): Le cadre parent """

	for widget in cadre.winfo_children():
		widget.config(state=tkinter.NORMAL)


def demander_charger_pioche(fenetre):
	""" Affiche un menu qui demande au joueur de choisir une pioche.

		fenetre (tkinter.Tk): La fenêtre de jeu """

	def quand_valide():
		info_boucle["attente"] = False

	def quand_qcm_change(*args):
		if var_fic.get():
			activer_categorie(liste_pio)
		else:
			desactiver_categorie(liste_pio)

	pioches = obtenir_liste_pioche()

	cadre = creer_categorie(fenetre, "Pioche", "n")
	qcm_fic, var_fic = creer_qcm_simple(cadre, "Depuis un fichier ?", "Non", "Oui")
	liste_pio, var_pio = creer_qcm_liste(cadre, "Quelle pioche ?", *pioches)
	bouton_valide = creer_bouton(cadre, "Continuer", quand_valide)

	info_boucle = {"attente": True}

	var_fic.trace("w", quand_qcm_change)
	quand_qcm_change()

	while info_boucle["attente"]:
		redessiner_fenetre(fenetre)

	cadre.destroy()

	if var_fic.get():
		return var_pio.get()
	return None


def demander_sauver_pioche(fenetre):
	""" Affiche un menu qui demande au joueur de choisir une pioche.

		fenetre (tkinter.Tk): La fenêtre de jeu """

	def quand_valide():
		info_boucle["attente"] = False

	def quand_qcm_change(*args):
		if var_fic.get():
			activer_categorie(saisi_pio)
		else:
			desactiver_categorie(saisi_pio)

	cadre = creer_categorie(fenetre, "Sauvegarde", "n")
	qcm_fic, var_fic = creer_qcm_simple(cadre, "Sauvegarder ?", "Non", "Oui")
	saisi_pio, var_pio = creer_champs_saisi(cadre, "Nom de la pioche")
	bouton_valide = creer_bouton(cadre, "Continuer", quand_valide)

	info_boucle = {"attente": True}

	var_fic.trace("w", quand_qcm_change)
	quand_qcm_change()

	while info_boucle["attente"]:
		redessiner_fenetre(fenetre)

	cadre.destroy()

	if var_fic.get():
		return var_pio.get()
	return None