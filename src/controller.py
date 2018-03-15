from hexagrid import *
from Models.model import *

class Controller:
    def __init__(self, t_ijk, alpha, beta, gamma):
        self.model = Model(HexaGrid(t_ijk), alpha, beta, gamma)

        self.ResetGrid()

    def ResetGrid(self):
        self.model.InitHexaGrid()

    def NextStep(self):
        self.model.UpdateGrid()

    def getGrid(self):
        return self.model.hexaGrid.gridToMatrix()