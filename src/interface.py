#!/usr/bin/env python3

from tkinter.filedialog import FileDialog

from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import ImageTk, Image
outputFolder = "output/"

def initInterface():
    global app
    app = Interface()

def startInterface():
    global app
    app.root.mainloop()

class Interface:
    def __init__(self):
        self.zoomMax = 10
        self.zoomMin = -10
        self.zoomPas = 1
        self.panSpeed = 1
        self.panBorderLimit = 10
        self.isPanning = False
        self.panLastPosition = (-1,-1)
        self.root = Tk()
        self.root.title = 'Safe-Eye'
        width = 800
        height = 600
        screenWidth = self.root.winfo_screenwidth()
        screenHeight= self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenWidth - width) / 2, (screenHeight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        #Create Elements
        labelHelper = Label(text="Left Click Drag : Create a selection | Scroll : Zoom | Right Click Drag : Pan")
        self.labelZoom = Label(text="Zoom = x1")
        butOpen = Button(self.root, text="Open Image", justify="center", command=self.openImage)

        self.canvas = Canvas(self.root, bg='blue')
        self.canvas.bind_all("<MouseWheel>", self.canvasZoom)
        self.canvas.bind_all("<B3-Motion>", self.canvasPan)
        self.canvas.bind_all("<Button-3>", self.canvasPanStart)
        self.canvas.bind_all("<ButtonRelease-3>", self.canvasPanStop)



        #elements Placement
        labelHelper.pack( fill=X, side=TOP)
        self.labelZoom.pack( fill=X, side=BOTTOM)
        self.canvas.pack( expand=True,fill=BOTH, side=LEFT)
        butOpen.pack(side=RIGHT)

    def openImage(self):
        f_types = [('Png Files', '*.png'),('Jpg Files', '*.jpg')]
        filename = filedialog.askopenfile(filetypes=f_types, initialdir = "./")
        if filename is not None:
            self.img = PhotoImage(file =filename.name)
            self.display = self.img.copy()
            self.zoom = 0

            self.labelZoom.config(text = f"Zoom = x{self.zoomDisplayNumber()}")
            if hasattr(self, 'canImg'):
                self.canvas.itemconfig(self.canImg, image = self.display, anchor=CENTER)
                self.canvas.moveto(self.canImg, (self.canvas.winfo_width()/2) - (self.display.width()/2), (self.canvas.winfo_height()/2) - (self.display.height()/2))
            else :
                self.canImg = self.canvas.create_image(self.canvas.winfo_width()/2,self.canvas.winfo_height()/2.0, anchor=CENTER, image = self.display)

    def zoomDisplayNumber(self):
        result = 1
        if self.zoom > 0:
            result = 1 + self.zoom 
        elif self.zoom < 0:
            result = 1.0 / (1 -self.zoom)
        return round(result,2)

    def canvasZoom(self, event):
        if hasattr(self, 'canImg'):
            if event.delta > 0.1 and ((self.zoom + self.zoomPas) < self.zoomMax):
                self.zoom = self.zoom + self.zoomPas
            elif event.delta < -0.1 and ((self.zoom - self.zoomPas) > self.zoomMin):
                self.zoom = self.zoom-self.zoomPas
            
            if(self.zoom > 0):
                self.display = self.img.zoom(1 + self.zoom)
            elif self.zoom < 0:
                self.display = self.img.subsample( 1 - self.zoom)
            else :
                self.display = self.img.copy()
            
            self.labelZoom.config(text = f"Zoom = x{self.zoomDisplayNumber()}")
            self.canvas.itemconfig(self.canImg, image = self.display)

    def canvasPanStart(self, event):
        self.isPanning = True

    def canvasPanStop(self, event):
        self.panLastPosition = (-1,-1)
        self.isPanning = False

    def canvasPan(self, event):
        if self.isPanning is True and hasattr(self, 'canImg'):
            if(self.panLastPosition[0] < 0 or self.panLastPosition[1] < 0):
                self.panLastPosition = (event.x, event.y)
            else :
                delta = (event.x - self.panLastPosition[0], event.y - self.panLastPosition[1])
                self.panLastPosition = (event.x, event.y)

                
                coords = self.canvas.coords(self.canImg)
                coords[0] = coords[0] + delta[0]*self.panSpeed
                coords[1] = coords[1] + delta[1]*self.panSpeed
                
                bounds = self.canvas.bbox(self.canImg)
                w2 = self.display.width()/2
                h2 = self.display.height()/2
                
                if (coords[0] + w2 > self.panBorderLimit) and (coords[0] - w2 < self.canvas.winfo_width()-self.panBorderLimit) and (coords[1] + h2 > self.panBorderLimit) and (coords[1] - h2 < self.canvas.winfo_height()-self.panBorderLimit) :
                    self.canvas.move(self.canImg, delta[0]*self.panSpeed, delta[1]*self.panSpeed)
