# Souverains des flocons
**Nous étudions la formation des flocons de neige.**

![Image of Devine Snowflake](https://bridoz.com/wp-content/uploads/2014/05/neige11.jpg)

###### Membres
MANSOUR Mélissa <br>
MERLE-REMOND Julian <br>
RUCHE Nicolas <br>
TRAZIE Océane <br>

## Vous avez dit flocons ?

  Les cristaux de neige naissent et se développent au sein des nuages à température nettement négative. Sous l'action de mouvements ascendants au sein de l'atmosphère, de la vapeur d'eau provenant des couches basses de l'atmosphère remonte vers des couches atmosphériques d'altitude plus élevée. Elle s'y condense alors sur les microscopiques poussières en suspension dans l'air, soit sous la forme de micro-gouttelettes d'eau en surfusion soit sous celle d'un microscopique germe de glace : c'est la naissance du cristal. Débute ensuite sa phase de croissance : de la vapeur d'eau continue à se condenser sur le germe de glace initial, en provenance des micro-gouttelettes d'eau liquide surfondue également présentes dans le nuage, par effet Bergeron. La taille du cristal passe ainsi de quelques micromètres à quelques millimètres. Sa forme dépend principalement de la température à laquelle il se développe. On observe trois formes types : les étoiles, les plaquettes, les aiguilles et colonnes.
  *(source : meteofrance.fr)*

            
## Le modèle 


### Présentation

  Pour générer nos flocons, nous nous basons sur le modèle de Clifford A. Reiter, mathématicien américain. C'est un modèle en deux dimensions qui ne nous permettra donc pas de représenter les formes tri-dimensionelles. Le modèle de Reiter est un automate représenté sur une grille hexagonale. Chaque cellule a donc 6 voisins.
  
  ![Image of Devine Hexagonal Grid](http://catlikecoding.com/unity/tutorials/hex-map/part-1/about-hexagons/hexagon-grid.png)
  
  Chaque cellule prend une valeur indiquant l'état de l'eau dans la cellule. Lorsque l'état d'une cellule x à un temps t, state(t, x) > 1, on considère que l'eau est solide. 
  
  Nous divisons les cellules de la grille en 2 types : les **cellules réceptives** et les **cellules non réceptives**. Les sites réceptifs sont définis comme les sites étant "glacés" ou ayant un voisin glacé. 
  Les valeurs affectées aux cellules à chaque étape se font en additionant la valeur de la cellule à l'étape précédente, une quantité d'eau provenant d'autres cellules et une terme de diffusion.
  
  state(t, x) = state(t-1, x) + γ + α ∇²(state(t-1, x))
  
  Le modèle prend en compte trois paramètres: 
  
  + α : constante de diffusion 
  + β : teneur en vapeur d'eau de l'environnement
  + γ : quantité d'eau provenant d'en dehors de la cellule
  
 ### Initialisation et fonctionnement
 
 Pour l'initialisation, on commence avec une cellule centrale de la grille, dite cellule-germe, qui prend la valeur de 1. Toutes les autres cellules de la grille prennent la valeur de β.
 
 Lors de l'exécution, les cellules limitrophes gardent toujours la valeur de β.  
 
 
 
 
  
