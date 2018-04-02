from hexagrid import *
from model import *

PROFILE_MODE = False

class Controller:
    def __init__(self, alpha, beta, gamma, mapRadius):
        self.model = Model(alpha, beta, gamma, mapRadius)
        self.nbCellsWidth = self.model.hexaMap.nbCellsWidth
        self.ResetGrid()
        
    def ResetGrid(self):
        self.model.InitGrid()
    
    def NextStep(self):
        if PROFILE_MODE:
            import cProfile, pstats, io
            pr = cProfile.Profile()
            pr.enable()
            
            self.model.UpdateGrid()
            
            pr.disable()
            s = io.StringIO()
            sortby = 'tottime'
            pstats.Stats(pr, stream=s).sort_stats(sortby).print_stats()
            sortby = 'cumtime'
            pstats.Stats(pr, stream=s).sort_stats(sortby).print_stats(15)
            
            print(s.getvalue())
        else:
            self.model.UpdateGrid()
