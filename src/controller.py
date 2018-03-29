from hexagrid import *
from model import *

class Controller:
    def __init__(self, beta, gamma, mapRadius):
        self.model = Model(beta, gamma, mapRadius)
        self.nbCellsWidth = self.model.hexaMap.nbCellsWidth
        self.ResetGrid()
        
    def ResetGrid(self):
        self.model.InitGrid()
    
    def NextStep(self):
        self.model.UpdateGrid()
