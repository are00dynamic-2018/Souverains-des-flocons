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
        q,r = qr
        radius = self.radius
        if -radius <= q <= radius:
            if max(-radius, -q - radius) <= r <= min(radius, -q + radius):
                return True
        return False

    def __getitem__(self, qr):
        if self._ValidateCoords(qr):
            return self.cells[qr]
        else:
            raise LookupError

    def __setitem__(self, qr, value):
        if self._ValidateCoords(qr):
            assert type(value) is HexaCell, "Pas une hexacell"
            self.cells[qr] = value
        else:
            raise LookupError

    def __iter__(self):
        """for data in grid:"""
        for qr in self.keys():
            yield self[qr]
            
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

    def GetNeighbors(self, hexaCell):
        for qr in hexaCell.GetFalseNeighbors():
            if self._ValidateCoords(qr):
                yield self[qr]

    def GetAllNeighbors(self, hexaCell):
        neighbors = []
        for qr in hexaCell.GetFalseNeighbors():
            if self._ValidateCoords(qr):
                neighbors.append(self[qr])
        return neighbors

    def NeighborsCount(self, hexaCell):
        return len(self.GetAllNeighbors(hexaCell))


    def _InitMap(self):
        for q in range(-self.radius, self.radius + 1):
            r1 = max(-self.radius, - q - self.radius)
            r2 = min(self.radius, - q + self.radius)
            for r in range(r1, r2 + 1):
                self.cells[(q,r)] = HexaCell(q,r)

        for cell in self.cells.values():
            cell.isEdge = self.NeighborsCount(cell) != 6
       
