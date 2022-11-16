#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

import src.metric as metric

import src.filter as filter
import src.yoloDetection as Yolo
outputFolder = "output/"
tmpFileSave = "tmp.png"
pathModel = "./model/"

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
        self.parameters = []

    def setFilter(self, filter, parameters) :
        self.filter = filter
        self.parameters = parameters

class Interface:

    def __init__(self):
        self.canSelect = True
        self.zoomMax = 10
        self.zoomMin = -10
        self.zoomPas = 1
        self.panSpeed = 1
        self.panBorderLimit = 10
        self.isPanning = False
        self.panLastPosition = (-1,-1)
        self.root = Tk()
        self.root.title('Safe-Eye')
        self.selfirstPos = (0,0)
        self.selections = []
        width = 1000
        height = 800
        screenWidth = self.root.winfo_screenwidth()
        screenHeight= self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenWidth - width) / 2, (screenHeight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=True, height=True)

        #Create Elements
        labelHelper = Label(text="Left Click Drag : Create a selection | Scroll : Zoom | Right Click Drag : Pan")
        self.labelZoom = Label(text="Zoom = x1")
        self.labelMetrics= Label(text="Metrics")
       

        self.canvas = Canvas(self.root, bg='blue')
        self.canvas.bind_all("<Button-4>", self.canvasZoom)
        self.canvas.bind_all("<Button-5>", self.canvasZoom)

        self.canvas.bind_all("<B3-Motion>", self.canvasPan)
        self.canvas.bind_all("<Button-3>", self.canvasPanStart)
        self.canvas.bind_all("<ButtonRelease-3>", self.canvasPanStop)

        self.canvas.bind_all("<Button-1>", self.selectionStart)
        self.canvas.bind_all("<B1-Motion>", self.selectionMotion)
        self.canvas.bind_all("<ButtonRelease-1>", self.selectionEnd)

        #Zone Bouttons
        self.zoneButtons = Frame(self.root, width=200)
        
        self.butOpenFrame = Frame(self.zoneButtons)
        butOpen = Button(self.butOpenFrame, text="Open Image", justify="center", command=self.openImage)
        butSave = Button(self.butOpenFrame, text="Save Image", justify="center", command=self.saveImage)
        #selections Filtres
        self.filtrageValue = StringVar()
        self.filtrageValue.set("pixel")

        #zone radio
        
        self.radioFilter = Frame(self.zoneButtons)
        self.rPixel = Radiobutton(self.radioFilter, text="Pixelization", variable=self.filtrageValue, value="pixel", command=self.radioButtonChanged)
        self.rGauss = Radiobutton(self.radioFilter, text="Gaussian Blur", variable=self.filtrageValue, value="gauss", command=self.radioButtonChanged)
        self.rPNoise = Radiobutton(self.radioFilter, text="Partial Destructive Noise", variable=self.filtrageValue, value="partnoise", command=self.radioButtonChanged)
        self.rBitNoise = Radiobutton(self.radioFilter, text="Full Bit Noise", variable=self.filtrageValue, value="bitnoise", command=self.radioButtonChanged)
        self.rShuffle = Radiobutton(self.radioFilter, text="Shuffle", variable=self.filtrageValue, value="shuffle", command=self.radioButtonChanged)

        butApplyFilter = Button(self.radioFilter, text="Apply Filter", justify="center", command=self.applyFilter)

        #Liste Selections
        self.listWidget = Frame(self.zoneButtons)
        butListUp = Button(self.listWidget, text="▲", justify="center", command=self.listMoveUp)
        butListDown = Button(self.listWidget, text="▼", justify="center", command=self.listMoveDown)
        self.listSelectionTk = Listbox(self.listWidget, selectmode = "multiple")
        self.listSelectionTk.bind('<<ListboxSelect>>', self.listChangeSelected)
        butDelete = Button(self.listWidget, text="Delete Selection", justify="center", command=self.deleteSelection)

        #Buttons CNN
        self.zoneCNN = Frame(self.zoneButtons)
        butDetection= Button(self.zoneCNN, text="Detection", justify="center", command=self.askDetectionCNN)
        butEvaluation= Button(self.zoneCNN, text="Evaluation", justify="center", command=self.askEvalCNN)

#----
        #elements Placement
        labelHelper.pack( fill=X, side=TOP)
        self.labelMetrics.pack( fill=X, side=BOTTOM)
        self.labelZoom.pack( fill=X, side=BOTTOM)
        self.canvas.pack( expand=True,fill=BOTH, side=LEFT)

        self.zoneButtons.pack(expand=False, side=RIGHT, fill=Y)
        self.zoneButtons.pack_propagate(0)
        #zoneButtons
        self.butOpenFrame.pack(side=TOP, fill=BOTH, expand=True)
        butOpen.pack(side=TOP, fill=X)
        butSave.pack(side=TOP, fill=X)

        self.listWidget.pack(side=TOP, fill=BOTH, expand=True)
        butListUp.pack(side=TOP, fill=X)
        butListDown.pack(side=TOP, fill=X)
        self.listSelectionTk.pack(side=TOP, fill=X)
        butDelete.pack(side=TOP, fill=X)

        self.radioFilter.pack(side=TOP, fill=BOTH, expand=True)
        self.rPixel.pack(side=TOP, fill=X)
        self.rGauss.pack(side=TOP, fill=X)
        self.rPNoise.pack(side=TOP, fill=X)
        self.rBitNoise.pack(side=TOP, fill=X)
        self.rShuffle.pack(side=TOP, fill=X)
        butApplyFilter.pack(side=TOP, fill=X)

        self.zoneCNN.pack(side=BOTTOM, fill=X)
        #zone CNN
        butDetection.pack( expand=True,side=LEFT, fill=X)
        butEvaluation.pack( expand=True ,side=RIGHT, fill=X)

    def openImage(self):
        f_types = [('Png Files', '*.png'),('Jpg Files', '*.jpg')]
        self.canSelect = False
        filename = filedialog.askopenfile(filetypes=f_types, initialdir = "./")
        if filename is not None:
            self.img = Image.open(filename.name)
            self.editedImg = self.img
            self.computeMetrics()
            self.display = ImageTk.PhotoImage(self.img)
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
        self.canSelect = True


    def saveImage(self):
        if hasattr(self, 'editedImg'):
            f_types = [('Png Files', '*.png'),('Jpg Files', '*.jpg')]
            filename = filedialog.asksaveasfile(filetypes=f_types, initialdir = "./")
            if filename is not None:
                self.editedImg.save(filename.name)

    def zoomDisplayNumber(self):
        result = 1
        if self.zoom > 0:
            result = 1 + self.zoom 
        elif self.zoom < 0:
            result = 1.0 / (1 -self.zoom)
        return round(result,2)

    def canvasZoom(self, event):
        if hasattr(self, 'img'):
            if event.num == 4 and ((self.zoom + self.zoomPas) < self.zoomMax):
                self.zoom = self.zoom + self.zoomPas
            elif event.num == 5 and ((self.zoom - self.zoomPas) > self.zoomMin):
                self.zoom = self.zoom-self.zoomPas
            self.computeImage()
            


    def applyZoom(self, img):
        if hasattr(self, 'canImg'):
            if(self.zoom > 0):
                self.display = img._PhotoImage__photo.zoom(1 + self.zoom)
            elif self.zoom < 0:
                self.display = img._PhotoImage__photo.subsample( 1 - self.zoom)
            else:
                self.display = img

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
        if(self.canSelect):
            self.selfirstPos = (event.x, event.y)

    def selectionMotion(self, event):
        if(self.canSelect):
            if event.x != self.selfirstPos[0] and event.y != self.selfirstPos[1]:
                if hasattr(self, 'selectHelper'):
                    self.canvas.delete(self.selectHelper)

                self.selectHelper = self.canvas.create_rectangle(event.x, event.y, self.selfirstPos[0], self.selfirstPos[1], outline="#f00")

    def selectionEnd(self, event):
        if(self.canSelect):
            print("Wat")
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
                        self.listSelectionTk.insert(END, f"[{sel.min[0]}, {sel.max[0]}] | [{sel.min[1]}, {sel.max[1]}] | {sel.filter}")
                        self.listSelectionTk.selection_clear(0, END)
                        self.listSelectionTk.selection_set(END)
                        self.listChangeSelected(None)
                if hasattr(self, 'selectHelper'):
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

        wRatio =  self.display.width() / self.img.size[0]
        hRatio =  self.display.height() / self.img.size[1]

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

        wRatio =  self.display.width() / self.img.size[0]
        hRatio =  self.display.height() / self.img.size[1]

        for e in self.selections:   
            self.updateSelectionZoom(e, minSelCan, wRatio, hRatio)

    def radioButtonChanged(self):
        a = 1

    def applyFilter(self):
        cursel = self.listSelectionTk.curselection()
        for i in range(len(cursel)):
            index = int(cursel[i])
            sel = self.selections[index]
            self.setFilter(index, self.filtrageValue.get(), [])
            self.listSelectionTk.delete(index)
            self.listSelectionTk.insert(index, f"[{sel.min[0]}, {sel.max[0]}] | [{sel.min[1]}, {sel.max[1]}] | {sel.filter}")
            self.generateImageAllFilter()
            self.computeImage()
        self.listSelectionTk.selection_clear(0, END)
            


    
    def listMoveUp(self):
        cursel = self.listSelectionTk.curselection()
        for i in range(len(cursel)):
            index = int(cursel[i])
            if index > 0:
                self.swapListElem(index, index - 1)
                self.computeImage()

    def listMoveDown(self):
        cursel = self.listSelectionTk.curselection()
        for i in range(len(cursel)-1, -1, -1 ):
            
            index = int(cursel[i])
            if index < self.listSelectionTk.size() - 1:
                self.swapListElem(index, index + 1)
                self.computeImage()


    def swapListElem(self, index1, index2):
        buf = self.selections[index2]
        self.selections[index2] = self.selections[index1]
        self.selections[index1] = buf

        txt = self.listSelectionTk.get(index1)
        self.listSelectionTk.delete(index1)
        self.listSelectionTk.insert(index2, txt)

        self.listSelectionTk.selection_set(index2)

    def listChangeSelected(self, event):
        cursel = self.listSelectionTk.curselection()
        if len(cursel) > 0:
            for i in range(len(self.selections)):
                found = False
                for j in range(len(cursel)):
                    if not found :
                        index = int(cursel[j])
                        if i == index:
                            found = True
                            self.canvas.itemconfig(self.selections[i].element, outline="#ff0")
                        else :
                            self.canvas.itemconfig(self.selections[i].element, outline="#0f0")

    def deleteSelection(self):
        cursel = self.listSelectionTk.curselection()
        for i in range(len(cursel)):
            index = int(cursel[i])
            
            self.listSelectionTk.delete(index)
            self.canvas.delete(self.selections[index].element)
            self.selections.remove(self.selections[index])
            if(self.listSelectionTk.size() > 0):
                if(index > self.listSelectionTk.size()-1): index = self.listSelectionTk.size()-1
                self.listSelectionTk.selection_set(index)
            self.generateImageAllFilter()
            self.computeImage()

    def setFilter(self, id, filter, parameters):
        if id >= 0:
            self.selections[id].setFilter(filter, parameters)
    
    def displayFilter(self, id, img):
        if id >= 0:
            e = self.selections[id]
            if e.filter == "pixel":
                return filter.imgPixelate(img, 4, e.min, e.max)
            elif e.filter == "gauss":
                return filter.imgBlurring(img, 2, e.min, e.max)
            elif e.filter == "partnoise":
                return filter.imgRandomNoise(img, 0.5, True, e.min, e.max)
            elif e.filter == "bitnoise":
                return filter.imgFullNoise(img, 2, True, 2,  e.min, e.max)
            elif e.filter == "shuffle":
                return filter.imgShuffle(img, e.min, e.max)
            else :
                return img 

    def computeImage(self):
        self.applyZoom(ImageTk.PhotoImage(self.editedImg))
    

    def generateImageAllFilter(self):
        if(self.img is not None):
            data = self.img.copy()
            for id in range(len(self.selections)):
                data = self.displayFilter(id, data)
            if self.editedImg != data : 
                self.editedImg = data
                self.computeMetrics()
            res = ImageTk.PhotoImage(data)
            return res
        return None

    def computeMetrics(self):
        psnr = metric.metric_PSNR(self.img, self.editedImg)
        mse = metric.metric_MSE(self.img, self.editedImg)
        rmse = metric.metric_RMSE(self.img, self.editedImg)
        sam = metric.metric_SAM(self.img, self.editedImg)
        ssim = metric.metric_SSIM(self.img, self.editedImg)
        haar = metric.metric_HaarPSI(self.img, self.editedImg)

        self.labelMetrics.config(text = f"PSNR : {psnr:.2f} | MSE : {mse:.2f} | RMSE : {rmse:.2f} | SAM : {sam:.2f} | SSIM : {ssim:.2f} | HAAR : {haar:.2f}")

    def askDetectionCNN(self):
        if hasattr(self, 'editedImg'):
            if not hasattr(self, 'yolo'):
                self.yolo = Yolo.Model_YOLO(pathModel)
            boxes = self.yolo.makePrediction(self.editedImg)[0] #Get the information [0] that is the selections boxes
            if hasattr(self, 'canImg'):
                for i in range(len(boxes)):
                    print()
                    element = self.canvas.create_rectangle(0, 0, 1, 1, outline="#0f0")
                    sel = Select((boxes[i].xmin, boxes[i].ymin), (boxes[i].xmax, boxes[i].ymax),element)
                    self.selections.append(sel)
                    self.listSelectionTk.insert(END, f"[{sel.min[0]}, {sel.max[0]}] | [{sel.min[1]}, {sel.max[1]}] | {sel.filter}")
                    self.listSelectionTk.selection_clear(0, END)
                    self.listChangeSelected(None)
                self.updateAllSelectionsZoom()


    def askEvalCNN(self):
        if hasattr(self, 'editedImg'):
            print("Execute Evaluation CNN")