from hexagrid import *
from Models.model import *

class Controller:
    def __init__(self, t_ijk, alpha, beta, gamma):
        self.hexagrid = HexaGrid(t_ijk)
        self.model = Model(self.hexagrid, alpha, beta, gamma)

