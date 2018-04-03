from hexagrid import HexaCell, HexaMap
import time
import multiprocessing as mp


def putcellWorker(cells, hm):
    task = 1
    for c in hm.values():
        cells.put( (task, c) )
    cells.join()
    
    task = 2
    hm_keys = tuple(hm.keys())
    for qr in hm_keys:
        cells.put( (task, qr) )
    cells.join()
    
    task = -1
    from controller import NUM_PROCS
    for i in range(NUM_PROCS):
        cells.put( (task, 0) )
    cells.join()
    print("worker "+(mp.current_process()).name+" has ended its tasks")


def Worker(cells, hm, rec, nonRec, gamma):
    name = (mp.current_process()).name
    
    def updatetask(log):
        if log:
            log.write("----------------------------------------------------------------------------------------------------------\n"
                 +"--  "+name+"\n"
                 +"-----------------------------------------------------\n")
        while True:
            #appel bloquant:
            task, obj = cells.get()
            if log:
                log.write("\ttask n°"+str(task)+";\t"+str(obj)+"\n")
            
            if task == 1:
                cell = obj
                
                receptive = False
                if cell.oldState >= 1 :
                    receptive = True
                else:
                    for qr2 in cell.GetFalseNeighbors():
                        try:
                            if hm[qr2].oldState >= 1:
                                receptive = True
                                break
                        except KeyError:
                            continue
                        
                if receptive:
                    recCell = HexaCell(cell.q, cell.r, cell.state, cell.isEdge)
                    nonRecCell = HexaCell(cell.q, cell.r, 0, cell.isEdge)
                
                else :
                    recCell = HexaCell(cell.q, cell.r, 0, cell.isEdge)
                    nonRecCell= HexaCell(cell.q, cell.r, cell.state, cell.isEdge)
                
                if recCell.state != 0:
                    recCell.state += gamma
                    
                qr = (cell.q, cell.r)
                rec[qr] = recCell
                nonRec[qr] = nonRecCell
                
                
                
            elif task == 2:
                qr = obj
    
                nonRecCell = nonRec[qr]
                cell = hm[qr]
                somme = 0
                cpt = 0
                for qr2 in nonRecCell.GetFalseNeighbors():
                    try:
                        somme += nonRecCell.oldState
                        cpt += 1
                    except KeyError:
                        continue
                cell.UpdateState()
                cell.state = nonRecCell.state/2 + somme/(cpt*2) + rec[qr].state
                hm[qr] = cell
                
            elif task == -1:
                cells.task_done()
                if log:
                    log.write("\tworker "+name+" has ended its tasks\n")
                break
                
            else:
                raise KeyError("invalid worker task:"+str(task))
            
            cells.task_done()
        if log:
            log.write("-----------------------------------------------------\n")
        return
    
    
    from controller import PROFILE_MODE, NUM_PROCS
    if PROFILE_MODE and NUM_PROCS > 1:
        import cProfile, pstats, io
        pr = cProfile.Profile()
        s = io.StringIO()
        pr.enable()

        updatetask(s)
        
        pr.disable()
        sortby = 'tottime'
        pstats.Stats(pr, stream=s).sort_stats(sortby).print_stats(20)
        sortby = 'cumtime'
        pstats.Stats(pr, stream=s).sort_stats(sortby).print_stats(20)
        #print(s.getvalue())
        with open(name+".log.txt", "w") as f:
            f.write(s.getvalue())
        
    else:
        updatetask(None)
        
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
        
        from controller import NUM_PROCS
        if NUM_PROCS > 1:
            local_hm = self.hexaMap.cells
            
            with mp.Manager() as mn:
                hm = mn.dict(local_hm)
                rec = mn.dict()
                nonRec = mn.dict()
                
                cells = mp.JoinableQueue(len(local_hm))
        
                #p_putcell = mp.Process(target=putcellWorker, args=(cells, hm), name="queue put")
                #p_putcell.start()
                
                my_procs = []
                for i in range(NUM_PROCS):
                    p = mp.Process(target=Worker, args=(cells, hm, rec, nonRec, self.gamma), name="receptive"+str(i))
                    p.start()
                    my_procs.append(p)
                    
                task = 1#calc receptive
                for c in local_hm.values():
                    cells.put( (task, c) )
                cells.join()
                
                print("len rec[]: "+str(len(rec)))
                print("len nonRec[]: "+str(len(nonRec)))
                
                task = 2#calc final sums
                for qr in tuple(local_hm.keys()):
                    cells.put( (task, qr) )
                cells.join()
                
                task = -1 #shutdown processes
                for p in my_procs:
                    cells.put( (task, 0) )
                cells.join()
                
                print("workers have ended their tasks")
                    
                #p_putcell.join()
                
                self.hexaMap.cells = dict(hm)
        
        
        else:
            rec = HexaMap(self.hexaMap.radius)
            nonRec = HexaMap(self.hexaMap.radius)
            
            for qr in self.hexaMap.keys():
                cell = self.hexaMap[qr]
                recCell = rec[qr]
                nonRecCell = nonRec[qr]
                  
                #plus rapide de l'intégrer que de faire un appel
                receptive = False
                if cell.oldState >= 1 :
                    receptive = True
                else:
                    for c in self.hexaMap.GetNeighbors(cell):
                            if c.oldState >= 1:
                                receptive = True
                                break
                  
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

    def _GetNeighborsAverage(self, hexaCell, hexMap):
        somme = 0
        cpt = 0
        for cell in hexMap.GetNeighbors(hexaCell):
                somme += cell.oldState
                cpt += 1

        return somme/cpt
