# PolyAlliances

## But du jeu

PolyAlliance est le nom donné à une version informatisé une réussite peu connue : La réussite des alliances. Ce jeu se joue avec 32 ou 52 cartes. Le but du jeu est de faire le moins de tas possibles à partir du paquet donné. La partie est gagnée si le nombre de tas est inférieur au seuil fixé au début.

## Préparation de l'environnement

Pour programmer ce jeu nous utiliserons les logiciels suivants:
- Python (téléchargeable [ici](https://www.python.org/downloads/)): Interprète le code
- Sublime Text 3 (c'est [ici](https://www.sublimetext.com/) que ça se passe): Un éditeur de code simple et léger
- Git (viens voir par [là](https://git-scm.com/downloads)): Permet la sauvegarde de différentes versions du projet en gardant une trace de tout ce qui a été fait
- Sublime Merge (regarde par [ici](https://www.sublimemerge.com/)): Intègre Git à Sublime Text pour simplifier ~~énormément~~ son utilisation
- Discord (pas besoin de te donner un lien): Pour parler devant un peuuutiii caféé laaaa

Pour travailler simultanément sur le même projet sans s'embêter à envoyer des mails à chaque fois, on va utiliser [Github](https://github.com/). Je t'invite à te créer un compte c'est gratuit ;)

Une fois les logiciels téléchargés, commence par installer Python en veillant à bien cocher la case *Add Python X.X to PATH*. Installe ensuite Sublime Text 3 puis Git et enfin Sublime Merge dans cet ordre en laissant les options d'installation par défaut.

Une fois les logiciels installés, il va falloir télécharger le projet:
1. Choisis un emplacement sur ton ordinateur (par exemple à l'aide de l'Explorateur de fichier Windows)
2. Copie le chemin vers cet emplacement (clique dans le chemin affiché dans l'explorateur pour afficher le chemin réel)
3. Ouvre une invite de commande (Windows + R > tape "cmd" > entrer)
4. Tape la commande suivante ```cd emplacementChoisi``` en remplaçant *emplacementChoisi* par l'emplacement... que tu as choisi
5. Tape la commande suivante ```git clone "https://github.com/RedbeanGit/polyalliance.git"```
6. Patiente le temps que le projet soit entièrement téléchargé.

Il ne reste plus qu'à ouvrir le projet dans Sublime Text 3 (File > Open Folder... > dossierContenantLeProjet).

## Utilisation de Git avec Sublime Merge

Avant chaque session de code, il est **important** de récupérer la dernière version du projet en ligne. Dans Sublime Text 3, le curseur doit se trouver dans un fichier du projet (si ce n'est pas le cas ouvre un fichier du projet, n'importe lequel). Clique ensuite sur **master** en bas à droite de l'éditeur. Sublime Merge apparait. Il suffit alors de cliquer sur la flêche dirigée vers le bas (en haut à droite de la fenêtre de Sublime Merge) pour importer les dernières modifications qui ont été faites. Une fois importé, tu peux programmer.

Après chaque session de code, il est **important** de sauvegarder et envoyer les modifications sur Github. Pour ça, il te suffit de cliquer sur **master** en bas à droite de l'éditeur de Sublime Text 3. Sublime Merge apparait. Si tu as ajouté de nouveaux fichiers pendant cette session, passe ta souris sur l'un d'eux (dans Sublime Merge) et clique sur **Stage All**. Ensuite, il suffit de donner une brève explication sur les modifs effectuées (exemple: *Optimisation de l'affichage*) et de cliquer sur **master** en haut de la fenêtre de Sublime Merge pour sauvegarder le projet. Il ne reste plus qu'à tout envoyer sur Github en cliquant sur la flêche dirigée vers le haut (en haut à droite de la fenêtre de Sublime Merge). Une fois envoyer tu peux tout fermer.