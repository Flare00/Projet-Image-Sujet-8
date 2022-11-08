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
class Select:
    def __init__(self, min : tuple, max : tuple, element):
        self.min = min
        self.max = max
        self.element = element
        self.filter = None

    def setFiler(self, filter) :
        self.filter = filter

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
        self.selfirstPos = (0,0)
        self.selections = []
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
       

        self.canvas = Canvas(self.root, bg='blue')
        self.canvas.bind_all("<MouseWheel>", self.canvasZoom)

        self.canvas.bind_all("<B3-Motion>", self.canvasPan)
        self.canvas.bind_all("<Button-3>", self.canvasPanStart)
        self.canvas.bind_all("<ButtonRelease-3>", self.canvasPanStop)

        self.canvas.bind_all("<Button-1>", self.selectionStart)
        self.canvas.bind_all("<B1-Motion>", self.selectionMotion)
        self.canvas.bind_all("<ButtonRelease-1>", self.selectionEnd)

        #Zone Bouttons
        self.zoneButtons = Frame(self.root, width=200)
        butOpen = Button(self.zoneButtons, text="Open Image", justify="center", command=self.openImage)
        #selections Filtres
        self.filtrageValue = StringVar()
        self.filtrageValue.set("pixel")
        self.rPixel = Radiobutton(self.zoneButtons, text="Pixelization", variable=self.filtrageValue, value="pixel", command=self.radioButtonChanged)
        self.rGauss = Radiobutton(self.zoneButtons, text="Gaussian Blur", variable=self.filtrageValue, value="gauss", command=self.radioButtonChanged)
        self.rPNoise = Radiobutton(self.zoneButtons, text="Partial Destructive Noise", variable=self.filtrageValue, value="partnoise", command=self.radioButtonChanged)
        self.rBitNoise = Radiobutton(self.zoneButtons, text="Full Bit Noise", variable=self.filtrageValue, value="bitnoise", command=self.radioButtonChanged)

        butApplyFilter = Button(self.zoneButtons, text="Apply Filter", justify="center", command=self.applyFilter)

        #Liste Selections
        self.listSelectionTk = Listbox(self.zoneButtons)
        
        self.listSelectionTk.bind('<<ListboxSelect>>', self.listChangeSelected)
        butDelete = Button(self.zoneButtons, text="Delete Selection", justify="center", command=self.deleteSelection)

        #Buttons CNN
        self.zoneCNN = Frame(self.zoneButtons)
        butDetection= Button(self.zoneCNN, text="Detection", justify="center", command=self.askCNN)
        butEvaluation= Button(self.zoneCNN, text="Evaluation", justify="center", command=self.askCNN)

#----


        #elements Placement
        labelHelper.pack( fill=X, side=TOP)
        self.labelZoom.pack( fill=X, side=BOTTOM)
        self.canvas.pack( expand=True,fill=BOTH, side=LEFT)

        self.zoneButtons.pack(expand=False, side=RIGHT, fill=Y)
        self.zoneButtons.pack_propagate(0)
        #zoneButtons
        butOpen.pack(side=TOP, fill=X)
        self.rPixel.pack(side=TOP, fill=X)
        self.rGauss.pack(side=TOP, fill=X)
        self.rPNoise.pack(side=TOP, fill=X)
        self.rBitNoise.pack(side=TOP, fill=X)
        butApplyFilter.pack(side=TOP, fill=X)

        self.listSelectionTk.pack(side=TOP, fill=X)
        butDelete.pack(side=TOP, fill=X)

        self.zoneCNN.pack(side=BOTTOM, fill=X)
        #zone CNN
        butDetection.pack(side=LEFT, fill=X)
        butEvaluation.pack(side=RIGHT, fill=X)

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
                for e in self.selections:  
                    self.canvas.delete(e.element)
                self.selections.clear()
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
            self.updateAllSelectionsZoom()

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
                
                w2 = self.display.width()/2
                h2 = self.display.height()/2
                
                if (coords[0] + w2 > self.panBorderLimit) and (coords[0] - w2 < self.canvas.winfo_width()-self.panBorderLimit) and (coords[1] + h2 > self.panBorderLimit) and (coords[1] - h2 < self.canvas.winfo_height()-self.panBorderLimit) :
                    self.canvas.move(self.canImg, delta[0]*self.panSpeed, delta[1]*self.panSpeed)
                    for sel in self.selections:
                        self.canvas.move(sel.element, delta[0]*self.panSpeed, delta[1]*self.panSpeed)

    def selectionStart(self, event):
        self.selfirstPos = (event.x, event.y)

    def selectionMotion(self, event):
        if event.x != self.selfirstPos[0] and event.y != self.selfirstPos[1]:
            if hasattr(self, 'selectHelper'):
                self.canvas.delete(self.selectHelper)

            self.selectHelper = self.canvas.create_rectangle(event.x, event.y, self.selfirstPos[0], self.selfirstPos[1], outline="#f00")

    def selectionEnd(self, event):
        if event.x != self.selfirstPos[0] and event.y != self.selfirstPos[1]:
            min = [0,0]
            max = [0,0]
            if(event.x < self.selfirstPos[0]):
                min[0] = event.x
                max[0] = self.selfirstPos[0]
            else :
                min[0] = self.selfirstPos[0]
                max[0] = event.x

            if(event.y < self.selfirstPos[1]):
                min[1] = event.y
                max[1] = self.selfirstPos[1]
            else :
                min[1] = self.selfirstPos[1]
                max[1] = event.y

            if hasattr(self, 'canImg'):
                sel = self.computeImageSelection(min, max)
                if sel is not None :
                    self.selections.append(sel)
                    self.listSelectionTk.insert(0, f"[{sel.min[0]}, {sel.max[0]}] | [{sel.min[1]}, {sel.max[1]}] | {sel.filter}")
            self.canvas.delete(self.selectHelper)

    def computeImageSelection(self, min, max):
        coords = self.canvas.coords(self.canImg)
        w2 = self.display.width()/2
        h2 = self.display.height()/2
        
        minSelCan = (coords[0] - w2 , coords[1] - h2)
        maxSelCan = (coords[0] + w2 , coords[1] + h2)

        if(max[0] <= minSelCan[0] or max[1] <= minSelCan[1] or min[0] >= maxSelCan[0] or min[1] >= maxSelCan[1]):
            return None

        for i in range(2):
            if min[i] < minSelCan[i]:
                min[i] = minSelCan[i]
            if max[i] > maxSelCan[i]:
                max[i] = maxSelCan[i]

        wRatio =  self.display.width() / self.img.width()
        hRatio =  self.display.width() / self.img.width()

        imgSelMin = [0,0]
        imgSelMax = [0,0]
        
        imgSelMin[0] = int((min[0] - minSelCan[0])/wRatio)
        imgSelMax[0] = int((max[0] - minSelCan[0])/wRatio)
        
        imgSelMin[1] = int((min[1] - minSelCan[1])/hRatio)
        imgSelMax[1] = int((max[1] - minSelCan[1])/hRatio)
        
        if(imgSelMin[0] == imgSelMax[0] or imgSelMin[1] == imgSelMax[1]):
            return None

        exist = False

        for s in self.selections:
            if(s.filter == None and s.min == imgSelMin and s.max == imgSelMax ):
                exist = True
        if(exist):
            return None

        element = self.canvas.create_rectangle(min[0], min[1], max[0], max[1], outline="#0f0")
        res = Select(imgSelMin, imgSelMax, element)
        self.updateSelectionZoom(res, minSelCan, wRatio, hRatio)

        return Select(imgSelMin, imgSelMax, element)

    def updateSelectionZoom(self, sel : Select,posMin : tuple, wRatio, hRatio):
        imgSelMin = (((sel.min[0])*wRatio) + posMin[0], ((sel.min[1])*hRatio) + posMin[1])
        imgSelMax = (((sel.max[0])*wRatio) + posMin[0], ((sel.max[1])*hRatio) + posMin[1])
        self.canvas.coords(sel.element, imgSelMin[0], imgSelMin[1], imgSelMax[0], imgSelMax[1])
    
    def updateAllSelectionsZoom(self):
        coords = self.canvas.coords(self.canImg)
        w2 = self.display.width()/2
        h2 = self.display.height()/2
        minSelCan = (coords[0] - w2 , coords[1] - h2)

        wRatio =  self.display.width() / self.img.width()
        hRatio =  self.display.width() / self.img.width()

        for e in self.selections:   
            self.updateSelectionZoom(e, minSelCan, wRatio, hRatio)

    def radioButtonChanged(self):
        print(self.filtrageValue.get())

    def applyFilter(self):
        print("Apply")

    def askCNN(self):
        print("CNN")
    
    def listChangeSelected(self, event):
        index = int(self.listSelectionTk.size() - self.listSelectionTk.curselection()[0] -1)
        for i in range(len(self.selections)):
            if i == index:
                self.canvas.itemconfig(self.selections[i].element, outline="#ff0")
            else :
                self.canvas.itemconfig(self.selections[i].element, outline="#0f0")

    def deleteSelection(self):
        index = int(self.listSelectionTk.size() - self.listSelectionTk.curselection()[0] -1)
        self.listSelectionTk.delete(index)
        self.canvas.delete(self.selections[index].element)
        self.selections.remove(self.selections[index])