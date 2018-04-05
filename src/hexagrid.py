class HexaCell:
    __slots__ = ("q", "r", "s", 
        "state", "oldState",
        "isEdge")
        
    def __init__(self, q, r, state=0, edge=False):
        self.q = q
        self.r = r
        self.s = -q - r
        self.state = state
        self.oldState = state

        self.isEdge = edge

    def GetCoords(self):
        return self.q, self.r, self.s
    
    def SetState(self, state):
        self.state = state

    def UpdateState(self):
        self.oldState = self.state

    def GetFalseNeighbors(self):
        offsets = [(1,0), (1,-1), (0,-1), (-1,0), (-1,1), (0,1)]
        for q, r in offsets:
            yield self.q + q, self.r + r
            
    def copy(self):
        c = HexaCell(self.q, self.r, self.state, self.isEdge)
        c.oldState = self.oldState
        return c

    def __eq__(self, other):
        return type(self) == type(other) and self.q == other.q and self.r == other.r and self.s == other.s

    def __add__(self, other):
        return HexaCell(self.q + other.q, self.r + other.r)

    def __neg__(self):
        return HexaCell(-self.q, -self.r)

    def __sub__(self, other):
        return HexaCell(self.q - other.q, self.r - other.r)

    def __mul__(self, other):
        return HexaCell(self.q * other.q, self.r * other.r)

    def __str__(self):
        return "({},{},{}) : {}".format(self.q, self.r, self.s, self.state)

    def __len__(self):
        return abs(self.s)

class HexaMap:
    __slots__ = ("radius", "cells", "nbCellsWidth")
    
    def __init__(self, radius):
        self.radius = radius
        self.cells = dict()
        self.nbCellsWidth = 2 * self.radius + 1

        self._InitMap()

    def _ValidateCoords(self, qr):
        """fontion très chère permettant de savoir si une cellule est dans
        la grille"""
        
        q,r = qr
        radius = self.radius
        return -radius <= q <= radius and max(-radius, -q - radius) <= r <= min(radius, -q + radius)

    def __getitem__(self, qr):
#c'était trop lent!!
#         if self._ValidateCoords(qr):
#             return self.cells[qr]
#         else:
#             raise LookupError
        try:
            return self.cells[qr]
        except KeyError as E:
            raise E

    def __setitem__(self, qr, value):
        if self._ValidateCoords(qr):
            assert type(value) is HexaCell, "Pas une hexacell"
            self.cells[qr] = value
        else:
            raise LookupError

    def __len__(self):
        return len(self.cells)

    def __iter__(self):
        """for data in grid:"""
        for qr in self.keys():
            yield self.cells[qr]
            
    def keys(self):
        """itere sur les coordonnées des cellules"""
        already_done = set()
        for q in range(-self.radius, self.radius + 1):
            r1 = max(-self.radius, - q - self.radius)
            r2 = min(self.radius, - q + self.radius)
            for r in range(r1, r2 + 1):
                already_done.add((q,r))
                yield (q,r)
    
    def values(self):
        return self.__iter__()

    def copy(self):
        hm = type(self)(self.radius)
        hm.cells = {k : self.cells[k].copy() for k in self.cells.keys()}
        return hm

    def GetNeighbors(self, hc):
        for qr in hc.GetFalseNeighbors():
            try:
                yield self.cells[qr]
            except KeyError:
                continue

    def GetAllNeighbors(self, hc):
        return [cell for cell in self.GetNeighbors(hc)]

    def NeighborsCount(self, hexaCell):
        return len(self.GetAllNeighbors(hexaCell))


    def _InitMap(self):
        for qr in self.keys():
            self.cells[qr] = HexaCell(*qr)

        for cell in self.cells.values():
            cell.isEdge = self.NeighborsCount(cell) != 6
       
