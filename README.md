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

  Nous utilisons le modèle de Clifford A. Reiter, mathématicien américain. C'est un modèle en deux dimensions qui ne nous permettra donc pas de représenter les formes tri-dimensionelles. Le modèle de Reiter est un automate représenté sur une grille hexagonale. Chaque cellule a donc 6 voisins.
  
  ![Image of Devine Hexagonal Grid] (https://www.google.fr/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=0ahUKEwjJhp2H8dzZAhUDRhQKHQm1AicQjRwIBg&url=http%3A%2F%2Fcatlikecoding.com%2Funity%2Ftutorials%2Fhex-map%2Fpart-1%2F&psig=AOvVaw2l-IYCiksGjbqjQTbQvAe8&ust=1520603886600685)
  
  Nous divisons les cellules de la grille en 2 types : les **cellules réceptives** et le **cellules non réceptives**.
  
