from tkinter import *

class Window :
    def __init__(self):
        self._InitUI()

    def _InitUI(self):
        """
        Creates the windows and displays it
        """
        self.window = Tk()
        self.canvas = Canvas(self.window)
        
        self.window.title('fenetre')

        btn1 = Button(self.window, text="Next Step", command=self.NextStep)
        btn2 = Button(self.window, text="Reset", command=self.ResetGrid)

        self.buttons = dict(nextStep=btn1, reset=btn2)
        
        text = StringVar()
        text.set("t = 0")

        self.timeLabel= Label(self.window, textvariable=text)
        
        alpha = Scale(self.window, orient='horizontal', from_=0, to=1, resolution=0.1, tickinterval=2, length=350, label='Alpha')
        beta = Scale(self.window, orient='horizontal', from_=0, to=1, resolution=0.1, tickinterval=2, length=350, label='Beta')
        gamma = Scale(self.window, orient='horizontal', from_=0, to=1, resolution=0.1, tickinterval=2, length=350, label='Gamma')
      
        self.sliders = dict(alpha=alpha, beta=beta, gamma=gamma)

    def ResetGrid(self):
        pass

    def NextStep(self):
        pass
      