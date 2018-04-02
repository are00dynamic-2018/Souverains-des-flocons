from hexagrid import *
import time
from multiprocessing import Pool

def updateWorker(qr, gamma, hm, rec, nonRec):
    cell = hm[qr]
    recCell = rec[qr]
    nonRecCell = nonRec[qr]
    
    receptive = False
    if cell.oldState >= 1 :
        receptive = True
    else:
        for c in hm.GetNeighbors(cell):
                if c.oldState >= 1:
                    receptive = True
    
    if receptive:
        recCell.state = cell.state
        nonRecCell.state = 0
            
    else :
        recCell.state = 0
        nonRecCell.state = cell.state
        
    recCell.UpdateState()
    nonRecCell.UpdateState()

    if recCell.state != 0:
            recCell.state += gamma

class Model():
    def __init__(self, alpha, beta, gamma, mapRadius):
        """
        alpha : float (0 <= b <= 1) constante de diffusion
        beta : float (0 <= b <= 1) background vapor level
        gamma : float (0 <= b <= 1) Addition de vapeur
        Initialise le modèle
        """
        assert 0 <= beta and beta <= 1, "Le niveau de vapeur beta doit être compris entre 0 et 1"
        assert 0 <= gamma and gamma <= 1, "La constante d'addition de vapeur gamma doit être comprise entre 0 et 1"
        assert 0 <= alpha and alpha <= 1, "La constante de diffusion alpha doit être comprise entre 0 et 1"
        assert mapRadius >= 0, "Le rayon de la carte doit être positif"

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        print("Model", alpha, beta, gamma)

        self.hexaMap = HexaMap(mapRadius)

        self.step = 0

    def InitGrid(self):
        for cell in self.hexaMap:
            q,r,s = cell.GetCoords()
            if q == r and r == 0:
                cell.SetState(1)
            else :
                cell.SetState(self.beta)
            cell.UpdateState()

    def UpdateGrid(self):
        old = time.time()
        self.step += 1

        rec = HexaMap(self.hexaMap.radius)
        nonRec = HexaMap(self.hexaMap.radius)
        
        my_queue = []
        for qr in self.hexaMap.keys():
            my_queue.append([qr, self.gamma, self.hexaMap, rec, nonRec])
        
        with Pool(processes=4) as pp: 
            #pp.starmap(updateWorker, my_queue)
            for qr in self.hexaMap.keys():
                cell = self.hexaMap[qr]
                recCell = rec[qr]
                nonRecCell = nonRec[qr]
                receptive = self._Receptive(qr)
                 
                if receptive:
                    recCell.state = cell.state
                    nonRecCell.state = 0
                         
                else :
                    recCell.state = 0
                    nonRecCell.state = cell.state
                     
                recCell.UpdateState()
                nonRecCell.UpdateState()
     
                if recCell.state != 0:
                        recCell.state += self.gamma


        for qr in self.hexaMap.keys():
            cell = self.hexaMap[qr]
            nonRecCell = nonRec[qr]
            cell.UpdateState()
            cell.state = nonRecCell.state/2 + self._GetNeighborsAverage(nonRecCell, nonRec)/2 + rec[qr].state
            
        print(self.step, ":", time.time() - old, "s")


    def _Receptive(self, qr):
        hc = self.hexaMap[qr]
        if hc.oldState >= 1 :
            return True
        
        for cell in self.hexaMap.GetNeighbors(hc):
                if cell.oldState >= 1:
                    return True

        return False

    def _GetNeighborsAverage(self, hexaCell, hexMap):
        somme = 0
        cpt = 0
        for cell in hexMap.GetNeighbors(hexaCell):
                somme += cell.oldState
                cpt += 1

        return somme/cpt
