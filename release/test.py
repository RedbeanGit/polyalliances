
from student import *

pioche = init_pioche_fichier("data_init.txt")
pioche[12] = {"valeur": 8, "couleur": "T"}
afficher_reussite(pioche)
print(verifier_pioche(pioche))