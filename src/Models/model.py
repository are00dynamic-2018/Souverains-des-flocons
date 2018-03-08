import numpy as np
from .Controllers.hexaGrid import *

class Model:
    def __init__(self, alpha, beta, gamma):
        """
        alpha : float (0 <= b <= 1) constante de diffusion
        beta : float (0 <= b <= 1) background vapor level
        gamma : float (0 <= b <= 1) 
        Initialise le modèle
        """
        assert 0 <= beta and beta <= 1, "Le niveau de vapeur beta doit être compris entre 0 et 1"
        assert 0 <= gamma and gamma <= 1, "la constante gamma doit être comprise entre 0 et 1"
        assert 0 <= alpha and alpha <= 1, "la constante de diffusion alpha doit être comprise entre 0 et 1"
        
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def InitHexaGrid(self, hexaGrid):
        """
        HexaGrid -> void
        Initialise la grille : toutes les cellules à beta sauf la cellule centrale à 1
        """
        I,J,K = hexaGrid.getSize()
        for i in range(I):
            for j in range(J):
                for k in range(K):
                    hexaGrid[i,j,k] = if (i == I//2 and j == J//2 and k == K//2) 1 else self.beta

    def UpdateGrid(self, hexaGrid):
        """
        HexaGrid -> void
        Met à jour la grille
        """
        pass

m = Model(0.2, 0.3)