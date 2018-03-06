#réaliser une fonction : centrale, edge. la fonction centrale remplace le bool en argument (a supprimer) teste si une cellule est la cellule centrale, idem pour edge.
#Neighbors : determine les voisisns d'une celleule (prend un tuple de coordonnees en argument)

def Init(beta, mat): #beta : background vapor level
    """float*array*bool->None
    Initialise toutes les cellules"""
    for i in mat[i, j]:
        for j in mat[i, j]:
            if Centrale(mat[i,j]):
                mat[i, j]=beta
            else:
                mat[i, j]=1


def Receptive(cell, mat): #mat sera definit avant
    """cell(tuple)*array->Bool
    Renvcoie True si la cellule est receptive, false sinon"""
    i, j = cell
    if mat[i, j]>=1:
        return True
    else:
        for k in Neighbors(k, l=cell):
            for l in Neighbors(k, l):
                if Neighbors(k, l)>=1:
                    return True
    return False

def NeighborsAverage(cell, mat):
    """cell*array-> float
    Retourne la moyenne des 6 voisins d'une cellule passee en argument"""
    S=0 #somme
    for k in Neighbors(k, l=cell):
        for l in Neighbors(k, l):
            S+=Neighbors(k, l)
    return S/6
            
def UpdateState(mat, alpha, beta, gamma): #alpha : constante de diffusion, gamma : constante ajoutee (eau provenant d'autres cellules)
    """array*float*float-> None
    Met a jour l'etat et la valeur de chaque cellule"""
    for i in mat[i, j]:
        for j in mat[i, j]:
            if Edge(mat[i, j], mat):
                mat[i, j]=beta
            elif Receptive(mat[i, j], mat):
                mat[i, j]=(NeighborsAverage(mat[i,j])+alpha/12*NeighborsAverage(mat[i,j]))+(mat[i, j]+gamma) #on factorisera plus tard
                #on additionne partie participant a la diffusion + partie non diffusion
            else :
                mat[i, j]=(NeighborsAverage(mat[i,j])+alpha/12*NeighborsAverage(mat[i,j])-mat[i, j])

