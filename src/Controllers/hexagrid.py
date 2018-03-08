# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 15:48:38 2018

@author: 3700191
"""
import numpy as np


def validateCoords(ijk):
    return sum(ijk) == 0

class HexaCell(object):
    __slots__ = ("ijk", "data",)
    
    def __init__(self, ijk, data):
        """initialisation de HexaCell, lancé quand on fait:
        var = HexaCell(ijk)"""
        self.data = data
        self.ijk = ijk #ijk est un tuple
        self.edge = False
    
    def __eq__(self, other):
        """vérifie si cell1 == cell2 (comparaison data)
        ce qui eqivalent à cell1.__eq__(cell2)
        il doit retourner True ou False"""
        if type(self) is not type(other):
            return False
        
        return self.data == other.data and self.ijk == other.ijk
    
    def __contains__(self, element):
        """vérifie si cell.data[element] existe"""
        return element in self.data
    
    def update(self, **data):
        """stocke data dans la cellule"""
        pass
    
    def __len__(self):
        """len(cell) retourne la longeur de data"""
        return len(self.data)

class HexaGrid(object):
    __slots__ = ("grid", "t_ijk")
    
    def __init__(self, t_ijk):
        """a = HexaGrid(t_ijk)
        self.grid = np."""
        self.t_ijk = t_ijk
        self.grid
        
    def __cube_to_axial(self, ijk):
        return self.grid[ijk[0]][ijk[2]]
        
    def __getitem__(self, ijk):
        """data = grid[ijk]"""
        if not validateCoords(ijk):
            raise LookupError
            
        return grid[ijk[0]][ijk[2]]
    
    def __setitem__(self, ijk, data):
        """grid[ijk] = data <=> grid.__setitem__(ijk, data)"""
        if not validateCoords((i,j,k)):
            raise LookupError
           
        grid[ijk[0]][ijk[2]] = HexaCell(ijk, data)
    
    def __delitem__(self, ijk):
        """del grid[ijk]"""
        if not validateCoords((i,j,k)):
            raise LookupError
        grid[ijk[0]][ijk[2]] = None
        
    def __iter__(self):
        """for data in grid:"""
        pass
    
    def __next__(self):
        """appeller nativement par next(grid)"""
        pass
        
    def __len__(self):
        """len(grid)"""
        pass
        
    def __eq__(self, other):
        """permet de comparer des grilles
        grid1 == grid2"""
        pass
        
    def __contains__(self, element):
        """vérifie si element est une cellule de grid"""
        pass
        
    def clear(self):
        """nettoie grid.data de toutes les celulles"""
        self.grid.clear()
    
    
    def keys(self):
        """itere sur les coordonnées des cellules"""
        pass
    
    def gridSize(self):
        """renvoie la taille de grid"""
        return self.t_ijk
    
    def update(self, ijk, **data):
        """met à jour la cellule ijk avec les données data"""
        if not validateCoords((i,j,k)):
            raise LookupError
    
    def getNeighbors(self, ijk):
        """retourne itérativement les voisins de la case
        ijk"""
        if not validateCoords((i,j,k)):
            raise LookupError
            
        for i in range(ijk[0]-1, ijk[0]+2):
            for j in range(ijk[1]-1, ijk[1]+2):
                for k in range(ijk[2]-1, ijk[2]+2):
                    if ijk != (i,j,k):
                        yield self.grid[i][j]
        
    def gridToHexa(self):
        """retourne l'Hexagrid"""
        return hexa
        
    def gridToMatrix(self):
        """transforme une hexagrid en matrice"""
        return matrix
        
    def display(self):
        """retourne une forme prete à la representation pour l'hexagrid"""
        pass
    
    
