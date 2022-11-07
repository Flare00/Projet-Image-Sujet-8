#!/usr/bin/env python3
from PIL import Image
from tkinter import * 

import filter

def main():

    initInterface()

    # Image input with size
    img = Image.open("ex.png")

    imgRandNoise = filter.imgRandomNoise(img, 0.5, True)
    imgNoise = filter.imgFullNoise(img, 2, True, 2)
    
    # Processing
    imgPixel = filter.imgPixelate(img, 16)
    imgBlur = filter.imgBlurring(img, 5)
    imgNoiseBlur = filter.imgBlurring(imgNoise, 5)

    # Save
    imgRandNoise.save('test_random_noise.png', 'png')
    imgNoiseBlur.save('test_noise_blur.png', 'png')
    imgNoise.save('test_full_noise.png', 'png')
    imgPixel.save('test_pixel.png', 'png')
    imgBlur.save('test_blur.png', 'png')

def initInterface():
    global fenetre, label
    fenetre = Tk()
    label = Label(fenetre, text="Fenetre")
    label.pack()
    fenetre.mainloop()

if __name__== "__main__":
    main()
