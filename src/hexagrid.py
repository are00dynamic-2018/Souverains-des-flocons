class HexaCell:
    def __init__(self, q, r, edge=False):
        self.q = q
        self.r = r
        self.s = -q - r
        self.state = 0
        self.diff = 0
        self.non_diff = 0
        self.oldDiff = 0
        self.oldNonDiff = 0

        self.isEdge = edge

    def GetCoords(self):
        return self.q, self.r, self.s
    
    def SetState(self, diff, non_diff):
        self.oldDiff = self.diff
        self.oldNonDiff = self.non_diff
        self.state = diff + non_diff
        self.diff = diff
        self.non_diff = non_diff

    def Distance(self, other):
        return len(self - other)

    def GetFalseNeighbors(self):
        offsets = [(1,0), (1,-1), (0,-1), (-1,0), (-1,1), (0,1)]
        for q, r in offsets:
            yield self + HexaCell(q, r)

    def __eq__(self, other):
        return self.q == other.q and self.r == other.r and self.s == other.s

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

    def __hash__(self):
        return hash(float(self.q + 0.3)) + hash(float(self.r + 0.2))

class HexaMap:
    def __init__(self, radius):
        self.radius = radius
        self.cells = dict()
        self.nbCellsWidth = 2 * self.radius + 1

        self._InitMap()

    def __getitem__(self, qr):
        q,r = qr
        cell = HexaCell(q,r)
        if cell in self.cells:
            return self.cells[cell]
        else:
            raise LookupError

    def GetNeighbors(self, hexaCell):
        for cell in hexaCell.GetFalseNeighbors():
            if cell in self.cells:
                yield self.cells[cell]

    def GetAllNeighbors(self, hexaCell):
        neighbors = []
        for cell in hexaCell.GetFalseNeighbors():
            if cell in self.cells:
                neighbors.append(self.cells[cell])
        return neighbors

    def NeighborsCount(self, hexaCell):
        return len(self.GetAllNeighbors(hexaCell))


    def _InitMap(self):
        for q in range(-self.radius, self.radius + 1):
            r1 = max(-self.radius, - q - self.radius)
            r2 = min(self.radius, - q + self.radius)
            for r in range(r1, r2 + 1):
                cell = HexaCell(q,r)
                self.cells[cell] = cell

        for cell in self.cells.values():
            cell.isEdge = self.NeighborsCount(cell) != 6
       

