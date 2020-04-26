import tkinter
 
# Définition du rectangle #
 
fenetre = tkinter.Tk()

def demander(canvas, texte):
	def quand_clic():
		attente[0] = False

	ensemble = tkinter.Frame(canvas)
	ensemble.pack()
	
	label = tkinter.Label(ensemble, text=texte)
	label.pack(side=tkinter.LEFT)

	saisie = tkinter.Entry(ensemble)
	saisie.pack(side=tkinter.LEFT)
	saisie.focus_set()

	bouton = tkinter.Button(ensemble, text="Valider", command=quand_clic)
	bouton.pack(side=tkinter.RIGHT)

	attente = [True]

	while attente[0]:
		canvas.update()

	return saisie.get()


print(demander(fenetre, "Test"))
