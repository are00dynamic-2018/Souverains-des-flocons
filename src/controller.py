from model import Model

PROFILE_MODE = False
NUM_PROCS = 1 #1 and 6 are good

class Controller:
    def __init__(self, alpha, beta, gamma, mapRadius):
        self.ResetGrid(alpha, beta, gamma, mapRadius)
        
    def ResetGrid(self, alpha, beta, gamma, mapRadius):
        self.model = Model(alpha, beta, gamma, mapRadius)
        self.nbCellsWidth = self.model.hexaMap.nbCellsWidth
        self.model.InitGrid()
    
    def NextStep(self):
        if PROFILE_MODE and not NUM_PROCS > 1:
            import cProfile, pstats, io
            pr = cProfile.Profile()
            pr.enable()
            
            self.model.UpdateGrid()
            
            pr.disable()
            s = io.StringIO()
            sortby = 'tottime'
            pstats.Stats(pr, stream=s).sort_stats(sortby).print_stats(20)
            sortby = 'cumtime'
            pstats.Stats(pr, stream=s).sort_stats(sortby).print_stats(20)
            
            print(s.getvalue())
        else:
            self.model.UpdateGrid()