# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 15:48:38 2018
@author: 3700191
"""
import numpy as np
from math import floor



HEXACELL_TYPE = np.dtype([
    #("ijk", np.int16 , (3,)), 
    ("data", np.float32, 1),
    ])
NEUTRAL_DATA = 0





def cube_to_axial(ijk):
    return np.array((ijk[0], ijk[2]))

def axial_to_cube(ik):
    return np.array((ik[0], -ik[0] - ik[1], ik[1]))



class HexaCell(object):
    __slots__ = ("ijk", "data", "edge", "mygrid")
    
    def __init__(self, mygrid, ijk, data):
        """initialisation de HexaCell, lancé quand on fait:
        var = HexaCell(ijk)"""
        self.mygrid = mygrid
        self.data = data[0]
        self.ijk = ijk #ijk est un tuple
        self.edge = tuple(ijk) in mygrid.edges
    
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
    
    def update(self, data):
        """stocke data dans la cellule"""
        self.data = data
        self.mygrid[self.ijk] = (data,)
        
    
    def __len__(self):
        """len(cell) retourne la longeur de data"""
        return len(self.data)

class HexaGrid(object):
    __slots__ = ("grid", "radius", "centre", "ordre_parcours",
                 "edges")
    
    def __init__(self, radius):
        """a = HexaGrid(t)"""
        self.radius = radius
        self.ordre_parcours = np.array([ (+1, -1, 0), (+1,0,-1), (0,+1,-1), 
                                (-1,+1,0), (-1,0,+1), (0,-1,+1) ])
        self.clear()
        self.centre = np.array(tuple(radius for i in range(3)))
        self.getEdges()
        
    def __getitem__(self, ijk):
        """data = grid[ijk]"""
        if not self.validateCoords(ijk):
            raise IndexError
            
        i, j = cube_to_axial(self.absoluteCoords(ijk))
        return HexaCell(self, ijk, self.grid[i][j])
    
    def __setitem__(self, ijk, data):
        """grid[ijk] = data <=> grid.__setitem__(ijk, data)"""
        if not self.validateCoords(ijk):
            raise IndexError
            
        i, j = cube_to_axial(self.absoluteCoords(ijk))
        self.grid[i][j] = (data,)
    
    def __delitem__(self, ijk):
        """del grid[ijk]"""
        if not self.validateCoords(ijk):
            raise IndexError
            
        i, j = cube_to_axial(self.absoluteCoords(ijk))
        self.grid[i][j] = (NEUTRAL_DATA,)
        
    def __iter__(self):
        """for data in grid:"""
        for ijk in self.keys():
            yield self[ijk]
    
    #défini par __iter__(self) qui retourne un générateur qui fournit __next__
    #def __next__(self):
    #    """appeller nativement par next(grid)"""
    #    pass
        
    def __len__(self):
        """len(grid)"""
        return len(self.grid)
        
    def __eq__(self, other):
        """permet de comparer des grilles
        grid1 == grid2"""
        return self.grid == other
        
    def __contains__(self, element):
        """vérifie si element est une cellule de grid"""
        return element in self.grid
        
    def clear(self):
        """nettoie grid.data de toutes les celulles"""
        self.grid = np.full((self.radius*2,self.radius*2), 
                            (NEUTRAL_DATA,), 
                            dtype=HEXACELL_TYPE)
    

    def keys(self):
        """itere sur les coordonnées des cellules"""
        already_done = set()
        radius = self.radius
        for i in range(-radius, radius):
            for j in range(max(-i, -i-radius), min(radius, -i+radius)):
                ijk = (i,j,-j-i)
                if ijk not in already_done:
                    already_done.add(ijk)
                    yield ijk
    
    def validateCoords(self, ijk):
        r = self.radius
        if sum(ijk) == 0:
            if -r < ijk[0] < r:
                if -r < ijk[1] < r:
                    if-r < ijk[2] < r:
                        return True
        return False
    
    def userCoords(self, ijk):
        return ijk-self.centre
        
    def absoluteCoords(self, ijk):
        return ijk+self.centre
    
    
    def gridSize(self):
        """renvoie la taille de grid"""
        return self.t*2
    
    #utiliser update de l'hexacell!!
    #def update(self, ijk, **data):
    #    """met à jour la cellule ijk avec les données data"""
    #    if not self.validateCoords((i,j,k)):
    #        raise LookupError
    
    def getNeighbors(self, ijk):
        """retourne itérativement les voisins de la case
        ijk"""
        if not self.validateCoords(ijk):
            raise LookupError
            
        for coords in self.ordre_parcours:
            c = coords + ijk
            yield self[c]
        
    def getEdges(self):
        """retourne un set des coordonnées des cellules sur 
        les bords de la grille"""
        self.edges = []
        r = self.radius-1
        ijk = (-r, 0, r) 
        for goSide in self.ordre_parcours:
            for x in range(r):
               self.edges.append(tuple(ijk))
               ijk += goSide
        
    #def gridToHexa(self):
    #    """retourne l'Hexagrid"""
    #    return hexa
        
    def gridToMatrix(self):
        """transforme une hexagrid en matrice"""
        return self.grid
        
    #def display(self):
    #    """retourne une forme prete à la representation pour l'hexagrid"""
    #    pass

#tests:
    """
hg = HexaGrid(6)

print("keys")
for x in hg.keys():
    print(x)
    
print("iter")
for x in hg:
    print(x.ijk)
    
print("edges")
for x in hg.edges:
    print(hg[x].ijk)
"""