from hexagrid import *
import time

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

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        print("Model", alpha, beta, gamma)

        self.hexaMap = HexaMap(mapRadius)

        self.step = 0

    def InitGrid(self):
        for cell in self.hexaMap.cells.values():
            q,r,s = cell.GetCoords()
            if q == r and r == 0:
                cell.SetState(0, 1)
            else :
                cell.SetState(self.beta, 0)
        self._CellsNewState()

    def UpdateGrid(self):
        old = time.time()
        self.step += 1
        for cell in self.hexaMap.cells.values():
            if cell.isEdge :
                continue
            diff = 0
            non_diff = 0
            receptive = self._Receptive(cell)

            if receptive:
                non_diff = cell.oldState + self.gamma
            else :
                diff = cell.oldState
                diff = 1/2 * diff + 1/12 * self._GetNeighborsSum(cell)
            #print(diff, non_diff)
            cell.SetState(diff, non_diff)
        print(self.step, ":", time.time() - old, "s")
        self._CellsNewState()

    def _CellsNewState(self):
        for cell in self.hexaMap.cells.values():
            cell.UpdateState()

    def _Receptive(self, hexaCell):
        q,r,s = hexaCell.GetCoords()
        hexaCell = self.hexaMap[q,r]
        if hexaCell.oldState >= 1 :
            return True
        
        for cell in self.hexaMap.GetNeighbors(hexaCell):
            if cell.oldState >= 1:
                return True

        return False

    def _GetNeighborsSum(self, hexaCell):
        somme = 0
        for cell in self.hexaMap.GetNeighbors(hexaCell):
            somme += cell.oldState

        return somme
