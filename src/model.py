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
        assert mapRadius >= 0, "Le rayon de la carte doit être positif"

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
                cell.SetState(1)
            else :
                cell.SetState(self.beta)
        self._CellsNewState()

    def UpdateGrid(self):
        old = time.time()
        self.step += 1

        rec = HexaMap(self.hexaMap.radius)
        nonRec = HexaMap(self.hexaMap.radius)

        for cell in self.hexaMap.cells.values():
            q,r,s = cell.GetCoords()
            receptive = self._Receptive(cell)
            #print(cell, receptive)
            if receptive:
                rec[(q,r)] = HexaCell(cell.q, cell.r, cell.state, cell.isEdge)
                nonRec[(q,r)] = HexaCell(cell.q, cell.r, 0, cell.isEdge)
            else :
                rec[(q,r)] = HexaCell(cell.q, cell.r, 0, cell.isEdge)
                nonRec[(q,r)] = HexaCell(cell.q, cell.r, cell.state, cell.isEdge)

        for cell in rec.cells.values():
            if cell.state != 0:
                cell.state += self.gamma

        for cell in nonRec.cells.values():
            cell.state = 1/2 * cell.state + 1/2 * self._GetNeighborsAverage(cell, nonRec)


        for qr in self.hexaMap.cells:
            recCell = rec[qr]
            nonRecCell = nonRec[qr]
            q,r = qr
            cell = HexaCell(q,r, nonRecCell.state + recCell.state, recCell.isEdge)
            self.hexaMap.cells[qr] = cell
            
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

    def _GetNeighborsAverage(self, hexaCell, hexMap):
        somme = 0
        cpt = 0
        for cell in hexMap.GetNeighbors(hexaCell):
                somme += cell.oldState
                cpt += 1

        return somme/cpt
