# Controllers

Le contrôleur est (pour l'instant) équivalent à la grille. Il stocke une grille encapsulée dans un objet HexaGrid.

HexaGrid possède les méthodes publiques suivantes :

+ update(ijk, data)
  + Mets à jour une case en (i,j,k) avec data
  + ijk : tuple des coordonnées hexagonales
  + data : dictionnaire de données
+ gridToHexa()
  + Renvoie la grille au format hexagonal pour les Models
+ gridToMatrix()
 + Renvoie la grille au format matriciel pour les Views

# Models

# Views
