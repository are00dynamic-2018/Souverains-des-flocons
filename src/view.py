from tkinter import *
from controller import *

class Window :
    def __init__(self, t_ijk):
        self.controller = None
        self._InitUI()

    def _InitUI(self):
        """
        Creates the windows and displays it
        """
        # Initialisation
        self.window = Tk()
        self.canvas = Canvas(self.window)
        
        self.window.title('fenetre')

        btn1 = Button(self.window, text="Next Step", command=self._NextStep)
        btn2 = Button(self.window, text="Reset", command=self._ResetGrid)

        self.buttons = dict(nextStep=btn1, reset=btn2)
        
        text = StringVar()
        text.set("t = 0")

        self.timeLabel= Label(self.window, textvariable=text)
        
        alpha = Scale(self.window, orient='horizontal', from_=0, to=1, resolution=0.1, tickinterval=2, length=350, label='Alpha')
        beta = Scale(self.window, orient='horizontal', from_=0, to=1, resolution=0.1, tickinterval=2, length=350, label='Beta')
        gamma = Scale(self.window, orient='horizontal', from_=0, to=1, resolution=0.1, tickinterval=2, length=350, label='Gamma')
      
        self.sliders = dict(alpha=alpha, beta=beta, gamma=gamma)
        
        # Positionnement
        self.ResetGrid()
        self.window.mainloop()

    def _ResetGrid(self):
        alpha = self.sliders.alpha.get()
        beta = self.sliders.beta.get()
        gamma = self.sliders.gamma.get()
        self.controller = Controller(self.t_ijk, alpha, beta, gamma)

        self.controller.ResetGrid()

    def _NextStep(self):
        assert self.controller != None, "La grille n'est pas initialisée : appuyer sur Reset"
      