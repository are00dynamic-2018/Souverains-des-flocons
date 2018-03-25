from controller import *
from tkinter import *
from math import sqrt, pi, cos, sin


class Point:
    def __init__(self, x, y):
        """
        float, float
        """
        self.x = x
        self.y = y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

class Orientation:
    def __init__(self, mat, startAngle):
        """
        (float, float, float, float), float
        mat : Rotation Matrix
        startAngle : angle in degrees, for the corners
        """
        self.f0, self.f1, self.f2, self.f3 = mat
        self.startAngle = startAngle

    def FlatOrientation():
        return Orientation((3 / 2, 0, sqrt(3) / 2, sqrt(3)), 0)

    def PointyOrientation():
        return Orientation((sqrt(3), sqrt(3) / 2, 0, 3/2), 30)

class Layout:
    def __init__(self, orientation, origin, cellRadius):
        """
        Orientation, Point, int
        """
        self.cellRadius = cellRadius
        self.orientation = orientation
        self.origin = origin

    def HexToPixel(self, hexaCell):
        """
        HexaCell -> Center Point On Screen
        """
        o = self.orientation
        x = (o.f0 * hexaCell.q + o.f1 * hexaCell.r) * self.cellRadius
        y = (o.f2 * hexaCell.q + o.f3 * hexaCell.r) * self.cellRadius
        return Point(x + self.origin.x, y + self.origin.y)

    def _CornerOffset(self, corner):
        """
        int : the ith corner, must be an integer between 0 and 5
        """
        corner = int(corner)
        assert 0 <= corner and corner < 6, "Corner's number muste between 0 and 5"

        angle = pi/3 * (corner + self.orientation.startAngle * 1/60)
        return Point(self.cellRadius * cos(angle) , self.cellRadius * sin(angle))

    def Corners(self, hexaCell):
        center = self.HexToPixel(hexaCell)
        corners = []
        for i in range(0, 6):
            offset = self._CornerOffset(i)
            corners.append(Point(int(center.x + offset.x), int(center.y + offset.y)))
        return corners

    def FlatLayout(origin, cellRadius):
        return Layout(Orientation.FlatOrientation(), origin, cellRadius)

    def PointyLayout(origin, cellRadius):
        return Layout(Orientation.PointyOrientation(), origin, cellRadius)

class Window:
    
    def __init__(self, c):
        assert type(c) is Controller, "{} n'est pas un controller".format(type(c))
        self.controller = c
        self.mapRadius = self.controller.model.hexaMap.radius

        size = 500
        self.canvasWidth = size
        self.canvasHeight = size

        hexaWidth = size/self.controller.nbCellsWidth
        hexaRadius = hexaWidth/2
        self.layout = Layout.PointyLayout(Point(self.canvasWidth/2,self.canvasHeight/2), hexaRadius)

        self._InitUI()
        
    def lockbutton(self, mybutton):
        def wrap(f):
            def new_f(*args, **kwargs):
                self.buttons[mybutton].config(state=DISABLED)
                ret = f(*args, **kwargs)
                self.buttons[mybutton].config(state=DISABLED)
            new_f.__name__ = f.__name__
            return new_f
        return wrap
    
    def activebutton(self, mybutton):
        def wrap(f):
            def new_f(*args, **kwargs):
                self.buttons[mybutton].config(state=ACTIVE)
                ret = f(*args, **kwargs)
                self.buttons[mybutton].config(state=NORMAL)
            new_f.__name__ = f.__name__
            return new_f
        return wrap
        
    def _InitUI(self):
        self.window = Tk()
        self.canvas = Canvas(self.window, width=self.canvasWidth, height=self.canvasHeight, bg="black")
        self.window.title('Les souverains des flocons')

        btn1 = Button(self.window, text="Next Step", command=self._NextStep)
        btn2 = Button(self.window, text="Reset", command=self._ResetGrid)
        btn3 = Button(self.window, text="Auto", command=self._Autoplay)

        self.buttons = dict(nextStep=btn1, reset=btn2, auto=btn3)

        
        
        text = StringVar()
        text.set("t = 0")

        self.timeLabel= Label(self.window, textvariable=text)
        
        alpha = Scale(self.window, orient='horizontal', from_=0, to=1, resolution=0.1, tickinterval=2, length=self.canvasWidth, label='Alpha')
        beta = Scale(self.window, orient='horizontal', from_=0, to=1, resolution=0.1, tickinterval=2, length=self.canvasWidth, label='Beta')
        gamma = Scale(self.window, orient='horizontal', from_=0, to=0.05, resolution=0.00001, tickinterval=2, length=self.canvasWidth, label='Gamma')

        steps = Scale(self.window, orient="horizontal", from_=1, to=2000, resolution=1, tickinterval=2, length=self.canvasWidth, label='Steps forward')

        self.sliders = dict(alpha=alpha, beta=beta, gamma=gamma, steps=steps)
        
        # Positionnement

        self.canvas.grid(row=0, column=0, columnspan=3)
        
        btn1.grid(row=1, column=0)
        btn2.grid(row=1, column=1)
        btn3.grid(row=1, column=2)
        
        
        alpha.grid(row=2, column=0)
        beta.grid(row=3, column=0)
        gamma.grid(row=4, column=0)
        steps.grid(row=5, column=0)
        
        self._Display()
        self.window.mainloop()


    def _ResetGrid(self):
        alpha = self.sliders["alpha"].get()
        beta = self.sliders["beta"].get()
        gamma = self.sliders["gamma"].get()
        self.controller = Controller(alpha, beta, gamma, self.mapRadius)

        self.controller.ResetGrid()
        self._Display()

    #@activebutton(self, "auto")
    def _Autoplay(self):
        steps = self.sliders["steps"].get()
        for i in range(steps):
            self._NextStep()
            #sleep(0.2)

    def _NextStep(self):
        assert self.controller != None, "La grille n'est pas initialisée : appuyer sur Reset"
        self.controller.NextStep()
        self._Display()

    def _Display(self):
        for cell in self.controller.model.hexaMap.cells.values():
            self._DrawHexa(cell)

    def _DrawHexa(self, cell):
        coords = self.layout.Corners(cell)
        coords = list(map(lambda x : (x.x, x.y), coords))

        state = min(1, cell.state)
        color = self._LerpColor(state)

        #print(color)
        """
        if cell.isEdge:
            self.canvas.create_polygon(coords, fill="white")
        else:
            self.canvas.create_polygon(coords, outline="white")
            center = self.layout.HexToPixel(cell)
            text = str(round(cell.state, 5)) + "\n" + str(cell.q) + " " + str(cell.r)
            self.canvas.create_text(center.x, center.y, text=text, fill="white")
        """      
        

        self.canvas.create_polygon(coords, fill=color)

    def _LerpColor(self, t):
        r,g,b = (0, 0,0)
        R,G,B = (255, 255, 255)

        nR = int(r * (1-t) + R * t)
        nG = int(g * (1-t) + G * t)
        nB = int(b * (1-t) + B * t)

        return "#" + str(hex(nR).split("x")[-1]) + str(hex(nG).split("x")[-1]) + str(hex(nB).split("x")[-1])

 
