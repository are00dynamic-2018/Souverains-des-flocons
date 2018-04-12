import view as v
import controller as co
import random
  

#additional modules needed: WCK

PROFILE_MODE = False
  
if __name__ == '__main__':  
    mapRad = 41
    alpha = 1
    beta = round(random.uniform(0, 0.95), 2)
    gamma = random.uniform(0, 1)
    
    c = co.Controller(alpha, beta, gamma, mapRad)
    
    if PROFILE_MODE:
        import cProfile as cp
        cp.run('v.Window(c)', 'snow_stats')
        
        import pstats
        p = pstats.Stats('snow_stats')
        p.strip_dirs().sort_stats("pcalls").print_stats()
        p.sort_stats('tottime').print_stats(0.5)
    else:
        w = v.Window(c)