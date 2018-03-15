from tkinter import *

class Window :
    def __init__(self):
        self._InitUI()

    def _InitUI(self):
        self.window = Tk()
        self.canvas = Canvas(self.window)

        btn1 = Button(self.window, text="Next Step")
        btn2 = Button(self.window, text="Reset")

        self.buttons = dict(nextStep=btn1, reset=btn2)

        self.label = 