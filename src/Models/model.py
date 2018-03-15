import numpy as np

class Model:
    def __init__(self, hexaGrid, alpha, beta, gamma):
        """
        alpha : float (0 <= b <= 1) constante de diffusion
        beta : float (0 <= b <= 1) background vapor level
        gamma : float (0 <= b <= 1) Addition de vapeur
        Initialise le modèle
        """
        assert 0 <= beta and beta <= 1, "Le niveau de vapeur beta doit être compris entre 0 et 1"
        assert 0 <= gamma and gamma <= 1, "La constante d'addition de vapeur gamma doit être comprise entre 0 et 1"
        assert 0 <= alpha and alpha <= 1, "La constante de diffusion alpha doit être comprise entre 0 et 1"
        
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        self.hexaGrid = hexaGrid

        self.step = 0

    def InitHexaGrid(self):
        """
        void -> void
        Initialise la grille : toutes les cellules à beta sauf la cellule centrale à 1
        """
        I,J,K = self.hexaGrid.getSize()
        for i in range(I):
            for j in range(J):
                for k in range(K):
                    data = {}
                    if (i == 0 and j == 0 and k == 0):
                        data["state"] = 1
                        data["diff"] = 0
                        data["non_diff"] = 1
                    else :
                        data["state"] = self.beta
                        data["diff"] = self.beta
                        data["non_diff"] = 0
                    self.hexaGrid[i,j,k] = data

    def UpdateGrid(self):
        """
        void -> void
        Met à jour la grille
        """
        self.step += 1
        for cell in self.hexaGrid :
            if cell.edge :
                continue

            if self.__Receptive(cell) :
                cell.data["non_diff"] += self.gamma

            cell.data["diff"] += (self.alpha/2) * (self.__NeighborsAverage(cell) - cell.data["diff"])

    def __Receptive(self, hexaCell):
        """
        HexaCell -> bool
        Renvoie True si la cellule est glacée ou a un voisin glacé
        """
        if hexaCell.data["state"] >= 1:
            return True

        #neighborCell : HexaCell
        for neighborCell in self.hexaGrid.getNeighbors(hexaCell.ijk):
            if neighborCell.data["state"] >= 1 :
                return True

        return False

    def __NeighborsAverage(self, hexaCell):
        """
        HexaCell -> float
        Renvoit la moyenne des voisins
        """
        somme = 0.0
        for neighborCell in self.hexaGrid.getNeighbors(hexaCell.ijk) :
            somme += neighborCell.data["diff"]
        
        return somme/6

    
