from hexagrid import *

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

    def UpdateGrid(self):
        self.step += 1
        for cell in self.hexaMap.cells.values():
            if cell.isEdge :
                continue
            diff = cell.oldDiff
            non_diff = cell.oldNonDiff
            if self._Receptive(cell):
                non_diff += self.gamma
            diff += (self.alpha/2) * (self._GetNeighborsAverage(cell) - diff)
            cell.SetState(diff, non_diff)

    def _Receptive(self, hexaCell):
        q,r,s = hexaCell.GetCoords()
        hexaCell = self.hexaMap[q,r]
        if hexaCell.state >= 1 :
            return True
        
        for cell in self.hexaMap.GetNeighbors(hexaCell):
            if cell.state >= 1:
                return True

        return False

    def _GetNeighborsAverage(self, hexaCell):
        somme = 0
        cpt = 0
        for cell in self.hexaMap.GetNeighbors(hexaCell):
            somme += cell.oldDiff
            cpt += 1

        return somme / cpt

