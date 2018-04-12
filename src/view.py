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
        self.auto_has_to_stop = False
        
        self.controller = c

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
        
    def _InitUI(self):
        self.window = Tk()
        self.window.resizable(False, False)
        self.canvas = Canvas(self.window, width=self.canvasWidth, height=self.canvasHeight, bg="black")
        self.window.title('Les souverains des flocons')

        #top level menu
        top = self.window.winfo_toplevel()
        self.menuBar = Menu(top)
        top['menu'] = self.menuBar
    
        self.subMenu = Menu(self.menuBar)
        self.menuBar.add_cascade(label='Export', menu=self.subMenu)
        self.subMenu.add_command(label='PostScript illisible', command=self._ExportImg)

        #création widgets
        controls = LabelFrame(self.window, labelanchor='nw', padx=5, pady=5, width=self.canvasWidth, text='Controls', relief=RIDGE)
        btn1 = Button(controls, text="Next Step [Enter key]", command=self._NextStep)
        
        radius_box = Frame(controls)
        btn2 = Button(radius_box, text="Reset", command=self._ResetGrid)
        radius_lbl = Label(radius_box, text='Radius: ')
        radius = Spinbox(radius_box, from_=3, to=400, increment =1, exportselection=True, width=5, command=self._needReset)
        
        step_box = Frame(controls)
        btn3 = Button(step_box, text="Auto", command=self._Autoplay)
        steps_lbl = Label(step_box, text='Steps forward: ')
        steps = Spinbox(step_box, from_=1, to=2000, increment =1, exportselection=True, width=5)
        


        mdl = LabelFrame(self.window, labelanchor='nw', padx=5, pady=5, width=self.canvasWidth, text='Modèle', relief=RIDGE)

        alpha = Scale(mdl, orient='horizontal', from_=0, to=3, resolution=0.1, tickinterval=2, label='Alpha', command=self._needReset)
        beta = Scale(mdl, orient='horizontal', from_=0, to=1, resolution=0.1, tickinterval=2, label='Beta', command=self._needReset)
        gamma = Scale(mdl, orient='horizontal', from_=0, to=1, resolution=0.0001, tickinterval=2, label='Gamma', command=self._needReset)
        
        #init values:
        cm = self.controller.model
        alpha.set(cm.alpha)
        beta.set(cm.beta)
        gamma.set(cm.gamma)
        steps.delete(0,"end")
        steps.insert(0,100)
        radius.delete(0,"end")
        radius.insert(0,cm.hexaMap.radius)
        
        #register widgets:
        self.buttons = dict(
            nextStep=btn1, 
            reset=btn2, 
            auto=btn3)
        self.sliders = dict(
            alpha=alpha, 
            beta=beta, 
            gamma=gamma, 
            steps=steps, 
            radius=radius)
        
        # Positionnement
        #dans la fenetre
        self.canvas.pack(fill=X)
        controls.pack(fill=X)
        mdl.pack(fill=X)
        
        #dans controls
        btn1.grid(row=0, column=0, sticky=N+W+S+E)
        radius_box.grid(row=0, column=1)
        step_box.grid(row=0, column=2)
        
        #dans radius_box
        btn2.grid(row=0, column=0, sticky=E, columnspan=2)
        radius_lbl.grid(row=1, column=0)
        radius.grid(row=1, column=1)
        
        #dans step_box
        btn3.grid(row=0, column=0, sticky=E, columnspan=2)
        steps_lbl.grid(row=1, column=0)
        steps.grid(row=1, column=1)
        
        #dans mdl
        alpha.pack(fill=X)
        beta.pack(fill=X)
        gamma.pack(fill=X)
        
        
        #bindings de touches
        self.window.bind("<Return>", lambda event: self._NextStep())
        
        #démarage loop d'affichage tcl
        self.window.mainloop()

    def _needReset(self, event=None):
        cm = self.controller.model
        if not (
            cm.alpha == self.sliders["alpha"].get() and
            cm.beta == self.sliders["beta"].get() and
            cm.gamma == self.sliders["gamma"].get() and
            cm.hexaMap.radius == int(self.sliders["radius"].get())
            ):
            self.buttons["reset"].config(bg="orange")


    def _ResetGrid(self):
        if not self.task_running.locked():
            alpha = self.sliders["alpha"].get()
            beta = self.sliders["beta"].get()
            gamma = self.sliders["gamma"].get()
            self.mapRadius = int(self.sliders["radius"].get())
            
            self.controller.ResetGrid(alpha, beta, gamma, self.mapRadius)
            
            hexaWidth = self.canvasWidth/self.controller.nbCellsWidth
            hexaRadius = hexaWidth/2
            self.layout = Layout.PointyLayout(Point(self.canvasWidth/2,self.canvasHeight/2), hexaRadius)
            
            self.buttons["reset"].config(bg=self.window.cget("bg"))
            self.redraw = True

    def _Autoplay(self):
        if self.ns_auto and self.ns_auto.is_alive():
            self.auto_has_to_stop = True
            
        if not self.task_running.locked():
            steps = int(self.sliders["steps"].get())
            if not self.ns_auto or not self.ns_auto.is_alive():
                self.buttons["auto"].config(bg="yellow", text="Stop")
                
                def threaded_auto():
                    for i in range(steps):
                        self._NextStep(auto=True)
                        self.ns_thr.join()
                        sleep(0.01)
                        if self.auto_has_to_stop:
                            self.auto_has_to_stop = False
                            break
                    self.redraw = True
                
                self.ns_auto = th.Thread(target=threaded_auto)
                self.ns_auto.start()
    
    def _NextStep(self, auto=False):
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
            working = True
            while True:
                if self.redraw or working:
                    self.redraw = False
                    working = True
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
                            self.canvas_cells.clear()
                            
                        for cell in hexa_values:
                            if cell.state != cell.oldState or step == 0:
                                self._DrawHexa(cell)
                                
                        #add text for step:
                        try:
                            self.canvas.itemconfig(self.canvas_cells["txt"], text="t = {}\nbeta = {}\ngamma = {}".format(step, cm.beta, cm.gamma))
                        except KeyError:
                            self.canvas_cells["txt"] = self.canvas.create_text(1, 1, anchor=NW, text="t = 0\nbeta = {}\ngamma = {}".format(cm.beta, cm.gamma), fill="white")
                                
                        self.canvas.update()
                        working = False
                        
                    if not (self.ns_auto and self.ns_auto.is_alive()):
                        self.buttons["auto"].config(bg=self.window.cget("bg"), text="Auto")
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
    
    def _ExportImg(self):
        self.canvas.update()
        self.canvas.postscript(file=r"../flocon_{}.ps".format(self.controller.model.step), colormode='color')

 
