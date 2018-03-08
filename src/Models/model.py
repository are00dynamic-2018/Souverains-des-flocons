#import numpy as np
from .Controllers.hexaGrid import *

class Model:
    def __init__(self, beta):
        """
        beta : float (0 <= b <= 1) background vapor level
        """
        assert 0 <= beta and beta <= 1, "Le niveau de vapeur beta doit être comprise entre 0 et 1"
        self.beta = beta

    def InitHexaGrid(self, hexaGrid):
        """
        HexaGrid -> void
        """
        I,J,K = hexaGrid.getSize()
        for i in range(I):
            for j in range(J):
                for k in range(K):
                    hexaGrid[i,j,k] = if (i == I//2 and j == J//2 and k == K//2) 1 else self.beta

    def UpdateGrid(self, hexaGrid):
        """
        HexaGrid -> void
        """
        pass

m = Model(0.2)