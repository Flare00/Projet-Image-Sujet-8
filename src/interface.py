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

        self.root = Tk()
        self.root.title = 'Safe-Eye'
        width = 800
        height = 600
        screenWidth = self.root.winfo_screenwidth()
        screenHeight= self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenWidth - width) / 2, (screenHeight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        butOpen = Button(self.root, text="Open Image", justify="center", command=self.openImage)
        butOpen["justify"] = "center"
        butOpen["text"] = "Open Image"
        butOpen["command"] = self.openImage

        butOpen.pack(side="right")

        self.canvas = Canvas(self.root)
        self.canvas.pack(side="left")

    def openImage(self):
        f_types = [('Png Files', '*.png'),('Jpg Files', '*.jpg')]
        filename = filedialog.askopenfile(filetypes=f_types)

        print(filename)
        self.img = ImageTk.PhotoImage(file=filename.name)
        self.canvas.create_image(0,0, anchor="nw", image = self.img)