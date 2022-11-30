#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np

import src.metric as metric
import src.filter as filter
import src.yoloDetection as Yolo
import src.mtcnnDetection as MTCNN
import src.superResolution.edsr as edsr
import src.deblur.deblurgan as deblur

outputFolder = "output/"
tmpFileSave = "tmp.png"
pathModel = "./model/"
weightsEDSR = "src/superResolution/edsr_weights.h5"
weightsDEBLUR = "src/deblur/deblur.h5"


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

class ParametersInterface:
    def __init__(self,parentWin, filterSelected, callback):
        self.parentWin = parentWin
        self.callback = callback
        self.filter = filterSelected;
        self.root = Toplevel(parentWin)
        self.root.grab_set()
        self.root.title(f"{self.filter}")
        self.root.protocol("WM_DELETE_WINDOW", self.onClose )
        width = 300
        height = 125
        screenWidth = self.root.winfo_screenwidth()
        screenHeight= self.root.winfo_screenheight()
        self.root.resizable(width=False, height=False)

        self.ZoneTop = Frame(self.root)
        self.ZoneLabels = Frame(self.ZoneTop)
        self.ZoneChamps = Frame(self.ZoneTop)
        self.ZoneButton = Frame(self.root)

        pad = 5
        butCancel = Button(self.ZoneButton, text="Cancel", justify="center", command=self.cancel)
        butValidate = Button(self.ZoneButton, text="Validate", justify="center", command=self.validate)

        self.ZoneTop.pack(fill=BOTH, side=TOP, expand=True, padx = pad, pady = pad)
        self.ZoneButton.pack( fill=X, side=BOTTOM, padx = pad, pady = pad)

        butCancel.pack(fill=X, side=LEFT, expand=True, ipadx = pad)
        butValidate.pack(fill=X, side=RIGHT, expand=True, ipadx = pad)

        self.ZoneLabels.pack( fill=BOTH, side=LEFT,expand=True , ipadx = pad)
        self.ZoneChamps.pack( fill=BOTH, side=RIGHT,expand=True , ipadx = pad)

        self.isset = False

        if self.filter == "pixel":
            self.pixelValue = StringVar(value="4")
            self.pixelLabel = Label(self.ZoneLabels, text="Pixel Size")
            self.pixelChamp = Entry(self.ZoneChamps, textvariable=self.pixelValue)

            self.pixelLabel.pack(fill=X, side=TOP)
            self.pixelChamp.pack(fill=X, side=TOP)
            self.isset = True
            #return filter.imgPixelate(img, 4, e.min, e.max)
        elif self.filter == "gauss":
            self.gaussValue = StringVar(value="2")
            self.gaussLabel = Label(self.ZoneLabels, text="Blur Size")
            self.gaussChamp = Entry(self.ZoneChamps, textvariable=self.gaussValue)

            self.gaussLabel.pack(fill=X, side=TOP)
            self.gaussChamp.pack(fill=X, side=TOP)

            self.isset = True
            #return filter.imgBlurring(img, 2, e.min, e.max)
        elif self.filter == "partnoise":
            self.pnoiseChanceValue = StringVar(value="0.5")
            self.pnoiseChanceLabel = Label(self.ZoneLabels, text="Chance [0.0 -> 1.0]")
            self.pnoiseChanceChamp = Entry(self.ZoneChamps, textvariable=self.pnoiseChanceValue)

            self.pnoiseColorValue = IntVar(value=1)
            self.pnoiseColorLabel = Label(self.ZoneLabels, text="Colored")
            self.pnoiseColorChamp = Checkbutton(self.ZoneChamps, variable=self.pnoiseColorValue,  onvalue = 1, offvalue= 0, )

            self.pnoiseChanceLabel.pack(fill=X, side=TOP)
            self.pnoiseChanceChamp.pack(fill=X, side=TOP)

            self.pnoiseColorLabel.pack(fill=X, side=TOP)
            self.pnoiseColorChamp.pack(fill=X, side=TOP)

            self.isset = True
            #return filter.imgRandomNoise(img, 0.5, True, e.min, e.max)
        elif self.filter == "bitnoise":
            self.bnoisNBbitValue = StringVar(value="1")
            self.bnoiseNBbitLabel = Label(self.ZoneLabels, text="Nb bit [0 -> 8]")
            self.bnoiseNBbitChamp = Entry(self.ZoneChamps, textvariable=self.bnoisNBbitValue)

            self.bnoiseMSBValue = IntVar(value=1)
            self.bnoiseMSBLabel = Label(self.ZoneLabels, text="MSB")
            self.bnoiseMSBChamp = Checkbutton(self.ZoneChamps, variable=self.bnoiseMSBValue,  onvalue = 1, offvalue= 0)

            self.bnoiseModeOptions = ["0", "1", "Random"]
            self.bnoiseModeValue = StringVar(value=self.bnoiseModeOptions[0])
            self.bnoiseModeLabel = Label(self.ZoneLabels, text="Replace by")
            self.bnoiseModeChamp = OptionMenu(self.ZoneChamps, self.bnoiseModeValue, *self.bnoiseModeOptions )


            self.bnoiseNBbitLabel.pack(fill=X, side=TOP)
            self.bnoiseNBbitChamp.pack(fill=X, side=TOP)

            self.bnoiseMSBLabel.pack(fill=X, side=TOP)
            self.bnoiseMSBChamp.pack(fill=X, side=TOP)

            self.bnoiseModeLabel.pack(fill=X, side=TOP)
            self.bnoiseModeChamp.pack(fill=X, side=TOP)

            self.isset = True


        if self.isset :
            self.root.mainloop()
        else:
            
            self.callback([])
            self.cancel()


    def cancel(self):
        self.onClose()

    def onClose(self):
        self.root.grab_release()
        self.root.destroy()

    def validate(self):
        if self.filter == "pixel":
            self.callback([int(self.pixelValue.get())])
        elif self.filter == "gauss":
            self.callback([int(self.gaussValue.get())])
        elif self.filter == "partnoise":
            self.callback([float(self.pnoiseChanceValue.get()), int(self.pnoiseColorValue.get())])
        elif self.filter == "bitnoise":
            mode = 2
            if self.bnoiseModeValue.get() == "1" :
                mode = 1
            elif self.bnoiseModeValue.get() == "0" :
                mode = 0
            self.callback([int(self.bnoisNBbitValue.get()), int(self.bnoiseMSBValue.get()), mode])

        self.cancel()
        
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
        self.canvas.bind("<Button-4>", self.canvasZoom)
        self.canvas.bind("<Button-5>", self.canvasZoom)

        self.canvas.bind("<B3-Motion>", self.canvasPan)
        self.canvas.bind("<Button-3>", self.canvasPanStart)
        self.canvas.bind("<ButtonRelease-3>", self.canvasPanStop)

        self.canvas.bind("<Button-1>", self.selectionStart)
        self.canvas.bind("<B1-Motion>", self.selectionMotion)
        self.canvas.bind("<ButtonRelease-1>", self.selectionEnd)

        #Zone Bouttons
        self.zoneButtons = Frame(self.root, width=300)
        
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
        self.zoneDetection= Frame(self.zoneCNN)
        butDetectionYOLO= Button(self.zoneDetection, text="Detection YOLO", justify="center", command=self.askDetectionYOLO)
        butDetectionMTCNN= Button(self.zoneDetection, text="Detection MTCNN", justify="center", command=self.askDetectionMTCNN)
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
        self.zoneDetection.pack(expand=True, side=LEFT, fill=BOTH)
        #zone CNN
        butDetectionYOLO.pack( expand=True,side=TOP, fill=X)
        butDetectionMTCNN.pack( expand=True,side=BOTTOM, fill=X)
        
        butEvaluation.pack( expand=True ,side=RIGHT, fill=BOTH)

    def openImage(self):
        f_types = [('Image', '*.png *.jpg *.jpeg')]
        self.canSelect = False
        filename = filedialog.askopenfile(filetypes=f_types, initialdir = "./input/")
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
                self.listSelectionTk.delete(0, END)
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
        if(hasattr(self, "img") and len(self.listSelectionTk.curselection()) > 0):
            self.tmpSelection = self.listSelectionTk.curselection()
            ParametersInterface(self.root, self.filtrageValue.get(), self.applyFilterWithParameter)
            
    def applyFilterWithParameter(self, params):
        cursel = self.tmpSelection
        for i in range(len(cursel)):
            index = int(cursel[i])
            sel = self.selections[index]
            self.setFilter(index, self.filtrageValue.get(), params)
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
                return filter.imgPixelate(img, e.parameters[0], e.min, e.max)
            elif e.filter == "gauss":
                return filter.imgBlurring(img, e.parameters[0], e.min, e.max)
            elif e.filter == "partnoise":
                return filter.imgRandomNoise(img, e.parameters[0], e.parameters[1], e.min, e.max)
            elif e.filter == "bitnoise":
                return filter.imgFullNoise(img, e.parameters[0], e.parameters[1], e.parameters[2],  e.min, e.max)
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
        sam = metric.metric_SAM(self.img, self.editedImg)
        ssim = metric.metric_SSIM(self.img, self.editedImg)
        haar = metric.metric_HaarPSI(self.img, self.editedImg)

        self.labelMetrics.config(text = f"PSNR : {psnr:.2f} | SAM : {sam:.2f} | SSIM : {ssim:.2f} | HAAR : {haar:.2f}")

    def askDetectionYOLO(self):
        if hasattr(self, 'editedImg'):
            if not hasattr(self, 'yolo'):
                self.yolo = Yolo.Model_YOLO(pathModel)
            boxes = self.yolo.makePrediction(self.editedImg)[0] #Get the information [0] that is the selections boxes
            if hasattr(self, 'canImg'):
                for i in range(len(boxes)):
                    w, h = self.img.size
                    min = (boxes[i].xmin if boxes[i].xmin > 0 else 0, boxes[i].ymin if boxes[i].ymin > 0 else 0)
                    max = (boxes[i].xmax if boxes[i].xmax < w else w, boxes[i].ymax if boxes[i].ymax < h else h)
                    element = self.canvas.create_rectangle(0, 0, 1, 1, outline="#0f0")
                    sel = Select(min,max ,element)
                    self.selections.append(sel)
                    self.listSelectionTk.insert(END, f"[{sel.min[0]}, {sel.max[0]}] | [{sel.min[1]}, {sel.max[1]}] | {sel.filter}")
                    self.listSelectionTk.selection_clear(0, END)
                    self.listChangeSelected(None)
                self.updateAllSelectionsZoom()

    def askDetectionMTCNN(self):
        if(hasattr(self,'editedImg')):
            if not hasattr(self, 'mtcnn'):
                self.mtcnn = MTCNN.Model_MTCNN()
            data = self.mtcnn.makePrediction(self.editedImg)
            if hasattr(self, 'canImg'):
                for i in range(len(data)):
                    wImg, hImg = self.img.size
                    x,y,w,h = data[i][1] #get the box, Box = [x, y, w, h], y' = y+h, x' = x+w
                    min = (x if x > 0 else 0, y if y > 0 else 0)
                    max = (x+w if x+w < wImg else wImg, y+h if y+h < hImg else hImg)
                    element = self.canvas.create_rectangle(0, 0, 1, 1, outline="#0f0")
                    sel = Select(min,max ,element)
                    self.selections.append(sel)
                    self.listSelectionTk.insert(END, f"[{sel.min[0]}, {sel.max[0]}] | [{sel.min[1]}, {sel.max[1]}] | {sel.filter}")
                    self.listSelectionTk.selection_clear(0, END)
                    self.listChangeSelected(None)
                self.updateAllSelectionsZoom()


    def askEvalCNN(self):
        if hasattr(self, 'editedImg'):
            print("Execute Evaluation CNN")
            if not hasattr(self, "edsrgan"):
                self.edsrgan = edsr.edsr(scale=4, num_res_blocks=16)
                self.edsrgan.load_weights(weightsEDSR)
            if not hasattr(self, "deblurgan"):
                self.deblurgan = deblur.generator_model()
                self.deblurgan.load_weights(weightsDEBLUR)
            res = self.editedImg.copy()
            for i in range(len(self.selections)):
                min = (self.selections[i].min[0], self.selections[i].min[1])
                max = self.selections[i].max

                srImg = filter.resizeByPixelSize(filter.cropImage(self.editedImg, min, max).copy())
                srImg = Image.fromarray(np.uint8(edsr.resolve_single(self.edsrgan, np.array(srImg))))
                srImg = srImg.resize((max[0] - min[0], max[1] - min[1]))
                #res = deblur.resolve(self.deblurgan, filter.cropImage(self.editedImg, min, max).copy())
                res.paste(srImg, (min[0],min[1]))
            res.show()