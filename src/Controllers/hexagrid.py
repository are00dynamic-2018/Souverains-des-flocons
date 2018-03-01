# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 15:48:38 2018

@author: 3700191
"""
import numpy as np

class HexaCell(object):
    def __init__(self, ijk):
        #initialisation de HexaCell, lancé quand on fait:
        #var = HexaCell(ijk)
        self.data = {}
        self.ijk = ijk #ijk est un tuple
    
    def __eq__(self, other):
        #vérifie si cell1 == cell2 (comparaison data et coordonnées)
        #ce qui eqivalent à cell1.__eq__(cell2)
        #il doit retourner True ou False
        pass
    
    def __contains__(self, element):
        #vérifie si cell.data[element] existe
        pass
    
    def update(self, **data):
         #stocke data dans la cellule
        pass
    
    def __len__(self):
        #len(cell) retourne la longeur de data
        return len(self.data)

class HexaGrid(object):
    __slots__ = (grid,)
    
    def __init__(self, t_ijk):
        #a = HexaGrid(t_ijk)
        #self.grid = np.
        
    def __getitem__(self, ijk):
        #data = grid[ijk]
        pass
    
    def __setitem__(self, ijk, data):
        #grid[ijk] = data
        pass
    
    def __delitem__(self, ijk):
        #del grid[ijk]
        pass
        
    def __iter__(self):
        #for data in grid:
        pass
    
    def __next__(self):
        pass
        
    def __len__(self):
        #len(grid)
        pass
        
    def __eq__(self, other):
        pass
        
    def __contains__(self, element):
        pass
        
    def clear(self):
        pass        
        
    
    def keys(self):
        pass
    
    def update(self, ijk, **data):
        pass
    
    def getNeighbors(self, ijk):
        yield (ni, nj, nk)
        
    def gridToHexa(self):
        return hexa
        
    def gridToMatrix(self):
        return matrix
        
    def display(self):
        pass
