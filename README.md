# Souverains des flocons
**Nous étudions la formation des flocons de neige.**

![Image of Devine Snowflake](https://bridoz.com/wp-content/uploads/2014/05/neige11.jpg)

###### Membres
MANSOUR Mélissa 

MERLE-REMOND Julian 

RUCHE Nicolas 

TRAZIE Océane 


## Vous avez dit flocons ?

  Les cristaux de neige naissent et se développent au sein des nuages à température nettement négative. Sous l'action de mouvements ascendants au sein de l'atmosphère, de la vapeur d'eau provenant des couches basses de l'atmosphère remonte vers des couches atmosphériques d'altitude plus élevée. Elle s'y condense alors sur les microscopiques poussières en suspension dans l'air, soit sous la forme de micro-gouttelettes d'eau en surfusion soit sous celle d'un microscopique germe de glace : c'est la naissance du cristal. Débute ensuite sa phase de croissance : de la vapeur d'eau continue à se condenser sur le germe de glace initial, en provenance des micro-gouttelettes d'eau liquide surfondue également présentes dans le nuage, par effet Bergeron. La taille du cristal passe ainsi de quelques micromètres à quelques millimètres. Sa forme dépend principalement de la température à laquelle il se développe. On observe trois formes types : les étoiles, les plaquettes, les aiguilles et colonnes.
  *(source : meteofrance.fr)*

## L'affichage

Nous choisissons d'afficher les flocons que nous génèrerons sur une grille hexagonale. Cette dernière nous permet d'obtenir plus aisément les 6 voisisns de chaque cellulle (voir ci-dessous). De plus, cette affichage correspond au modèle physique : les molécules d'eau lorsqu'elles se solidifient adoptent un arrangement hexagonal. La grille hexagonale représente un espace vectoriel de dimension 4 : {(x, y, z, a) ∈ ℝ² | x + y + z = 0} avec (x, y, z) les coordonnées de chaque cellulle et a le data.

![Image of Devine Hexagonal Grid](https://github.com/are00dynamic-2018/Souverains-des-flocons/blob/master/Docs/hexa.png)
            
## Le modèle 


### Présentation
  
  Pour générer nos flocons, nous nous basons sur le modèle de Clifford A. Reiter, mathématicien américain. C'est un modèle en deux dimensions qui ne nous permettra donc pas de représenter les formes tri-dimensionelles. Le modèle de Reiter est un automate dont chaque cellule a donc 6 voisins.
  
  ![Image of Devine Hexagonal Grid](http://catlikecoding.com/unity/tutorials/hex-map/part-1/about-hexagons/hexagon-grid.png)
  
  Pour gérer la grille hexagonale, nous suivrons le procédé suivant : [HexagonalGrid](https://www.redblobgames.com/grids/hexagons/implementation.html)
  

  Notre modèle se base sur l'article suivant : [Article de Jessica Li](https://github.com/are00dynamic-2018/Souverains-des-flocons/blob/master/Docs/JessicaLiModelREITER.pdf)

On appelle **C**, l'ensemble des cellules. Chaque cellule prend une valeur réelle positive indiquant l'état de l'eau dans cette cellule. On note s<sub>t</sub>(x) l'état d'une cellule x à un instant t.

On considère deux ensembles : 

+ 
  
  Nous divisons les cellules de la grille en 2 types : les **cellules réceptives** et les **cellules non réceptives**. Les sites réceptifs sont définis comme les sites étant "glacés" ou ayant un voisin glacé; autrement dit. 
  Les valeurs affectées aux cellules à chaque étape se font en additionant la valeur de la cellule à l'étape précédente, une quantité d'eau provenant d'autres cellules et une terme de diffusion.
  
  state(t, x) = state(t-1, x) + γ + α ∇²(state(t-1, x))
  
  Le modèle prend en compte trois paramètres: 
  
  + α : constante de diffusion 
  + β : teneur en vapeur d'eau de l'environnement
  + γ : quantité d'eau provenant d'en dehors de la cellule
  
 ### Initialisation et fonctionnement
 
 Pour l'initialisation, on commence avec une cellule centrale de la grille, dite cellule-germe, qui prend la valeur de 1. Toutes les autres cellules de la grille prennent la valeur de β.
 
 Lors de l'exécution, les cellules limitrophes gardent toujours la valeur de β. 
 
 ![Image Of Divine Cells](https://github.com/are00dynamic-2018/Souverains-des-flocons/blob/master/Docs/hexagrid.png)
 
 
 
 
  
