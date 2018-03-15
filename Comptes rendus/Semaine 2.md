#Semaine 2 

+ **changement et optimisation du traitement de la grille hexagonale**: La grille hexagonale représente maintenant un espace vectoriel de dimension 4 : {(x, y, z, a) ∈ ℝ² | x + y + z = 0} avec (x, y, z) les coordonnées de chaque cellulle et a le data. Ceci nous permet d'éviter des calculs longs et inutiles (en transformant la grille hexagonale en matrice carrée).

+ **étude du modèle, partie mathématique**: Documentation approfondie sur le modèle, formules mathématiques utilisées pour mettre à jour chaque cellule ainsi que sur la bibliothèque python "numpy".

+ **avancement du code**:
  - élaboration du squelette des 2 classes hexacell et hexagrid (cellule et grille), utilisation de la bibliothèque numpy.
  - début de la programmation du modèle (initiation de la grille, mise à jours de chaque état, etc.)
