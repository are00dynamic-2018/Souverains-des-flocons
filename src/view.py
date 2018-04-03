import threading as th
from time import sleep
from tkinter import *
from math import sqrt, pi, cos, sin

DEBUG_VALS = False

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
        self.task_running = th.Lock()
        self.ns_thr = None
        self.ns_auto = None
        
        self.controller = c
        self.mapRadius = self.controller.model.hexaMap.radius

        size = 500
        self.canvasWidth = size
        self.canvasHeight = size

        hexaWidth = size/self.controller.nbCellsWidth
        hexaRadius = hexaWidth/2
        self.layout = Layout.PointyLayout(Point(self.canvasWidth/2,self.canvasHeight/2), hexaRadius)
        
        self.display_thr = None
        self.canvas_cells = dict()
        self.redraw = True
        self._DisplayLoop()
        
        self._InitUI()
        
    def lockbutton(mybutton):
        def wrap(f):
            def new_f(*args, **kwargs):
                args[0].buttons[mybutton].config(state=DISABLED)
                ret = f(*args, **kwargs)
                args[0].buttons[mybutton].config(state=NORMAL)
            new_f.__name__ = f.__name__
            return new_f
        return wrap
    
    def activebutton(mybutton):
        def wrap(f):
            def new_f(*args, **kwargs):
                args[0].buttons[mybutton].config(state=ACTIVE)
                ret = f(*args, **kwargs)
                args[0].buttons[mybutton].config(state=NORMAL)
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
        gamma = Scale(self.window, orient='horizontal', from_=0, to=0.05, resolution=-1, tickinterval=2, length=self.canvasWidth, label='Gamma')

        steps = Scale(self.window, orient="horizontal", from_=1, to=2000, resolution=1, tickinterval=200, length=self.canvasWidth, label='Steps forward')
        
        cm = self.controller.model
        alpha.set(cm.alpha)
        beta.set(cm.beta)
        gamma.set(cm.gamma)
        steps.set(100)
        
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
        
        self.window.bind("<Return>", lambda event: self._NextStep())
        
        self.window.mainloop()


    def _ResetGrid(self):
        if not self.task_running.locked():
            alpha = self.sliders["alpha"].get()
            beta = self.sliders["beta"].get()
            gamma = self.sliders["gamma"].get()
            self.controller = Controller(alpha, beta, gamma, self.mapRadius)
            self.controller.ResetGrid()
            self.redraw = True

    def _Autoplay(self):
        if not self.task_running.locked():
            steps = self.sliders["steps"].get()
            if not self.ns_auto or not self.ns_auto.is_alive():
                
                def threaded_auto():
                    self.buttons["auto"].config(state=ACTIVE)
                    for i in range(steps):
                        self._NextStep(auto=True)
                        self.ns_thr.join()
                        sleep(0.01)
                    self.redraw = True
                    self.buttons["auto"].config(state=NORMAL)
                
                self.ns_auto = th.Thread(target=threaded_auto)
                self.ns_auto.start()
    
    def _NextStep(self, auto=False):
        assert self.controller, "La grille n'est pas initialisée : appuyer sur Reset"
        
        if auto or not self.task_running.locked():
            if not self.ns_thr or not self.ns_thr.is_alive():

                def threaded_step():
                    with self.task_running:
                        self.controller.NextStep()
                    self.redraw = True
                
                self.ns_thr = th.Thread(target=threaded_step)
                self.ns_thr.start()
                if not auto:
                    self.ns_thr.join()

    def _DisplayLoop(self):
        def threaded_DisplayLoop():
            print("display loop thread started")
            self.redraw = True
            started = False
            hexa_values = ()
            while True:
                if self.redraw:
                    if not started:
                        try:
                            self.canvas
                            started = True
                        except AttributeError:
                            sleep(0)
                            continue
                    
                    if not self.task_running.locked():
                        #with self.task_running:
                        cm = self.controller.model
                        hexa_values = tuple(cm.hexaMap)
                        step = cm.step
                    
                        #empeche les fuites de mémoire liées au grand nombre d'éléments
                        if step == 0:
                            self.canvas.delete("all")
                            
                        for cell in hexa_values:
                            if cell.state != cell.oldState or step == 0:
                                self._DrawHexa(cell)
                                
                        self.canvas.update()
                        self.redraw = False
                    print("hex drawn!")
                sleep(0)
        
        self.display_thr = th.Thread(target=threaded_DisplayLoop, daemon=True)
        self.display_thr.start()
    
    def _DrawHexa(self, cell):
        coords = self.layout.Corners(cell)
        coords = tuple(map(lambda x : (x.x, x.y), coords))

        state = min(1, cell.state)
        color = self._LerpColor(state)

        #print(color)
        if DEBUG_VALS:
            if cell.isEdge:
                self.canvas.create_polygon(coords, fill="white")
            else:
                self.canvas.create_polygon(coords, outline="white")
                center = self.layout.HexToPixel(cell)
                text = str(round(cell.state, 5)) + "\n" + str(cell.q) + " " + str(cell.r)
                self.canvas.create_text(center.x, center.y, text=text, fill="white")
        else:
            #dessin rapide car pas de nouvelles instances
            try:
                self.canvas.itemconfig(self.canvas_cells[coords], fill=color)
            except KeyError:
                self.canvas_cells[coords] = self.canvas.create_polygon(coords, fill=color)
        

    def _LerpColor(self, t):
        r,g,b = (66, 134, 244)
        R,G,B = (255, 255, 255)

        nR = int(r * (1-t) + R * t)
        nG = int(g * (1-t) + G * t)
        nB = int(b * (1-t) + B * t)

        return "#" + str(hex(nR).split("x")[-1]) + str(hex(nG).split("x")[-1]) + str(hex(nB).split("x")[-1])

 
