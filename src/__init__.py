import view as v
import controller as co
  
if __name__ == '__main__':  
    mapRad = 30
    alpha = 1
    beta = 0.3
    gamma = 0.01
    
    c = co.Controller(alpha, beta, gamma, mapRad)
    
    w = v.Window(c)