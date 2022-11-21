#!/usr/bin/env python3
from PIL import Image, ImageFilter
import random
import numpy as np
seedV = random.randint(1,2**32)


# min et max sont des tuples (x,y)
def cropImage(img, min, max):
    width, height = img.size
    if min[0] >= 0 and max[0] <= width and min[1] >= 0 and max[1] <= height:
            # Area : Left - Up - Right - Below
            area = (min[0], min[1], max[0], max[1])
            cropped_img = img.crop(area)
            return cropped_img
    else:
        raise Exception("Error Size cropImage()") 

def imgPixelate(img, largeurPX, min, max):
    res = img.copy()
    nX = int((max[0]-min[0]) / largeurPX)
    nY = int((max[1]-min[1]) / largeurPX)
    crop = cropImage(img, min, max)
    res.paste(crop.resize((nX,nY), resample=Image.Resampling.BILINEAR).resize(crop.size, Image.Resampling.NEAREST), min)
    return res


def imgBlurring(img, n, min, max):
    res = img.copy()
    crop = cropImage(img, min, max)
    res.paste(crop.filter(ImageFilter.GaussianBlur(n)), min)
    return res

def imgRandomNoise(img, chance, randomPix: bool, min, max): #Replace random pixel by black
    random.seed(seedV)
    res = img.copy()
    crop = cropImage(img, min, max)
    for x in range(crop.width):
        for y in range (crop.height):
            if(random.random() < chance):
                val = 0
                if(randomPix):
                    if(len(crop.getpixel((x,y))) == 1):
                        val = (random.randint(0,255))
                    if(len(crop.getpixel((x,y))) == 3):
                        val = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    if(len(crop.getpixel((x,y))) == 4):
                        val = (random.randint(0,255), random.randint(0,255), random.randint(0,255), 255)
                crop.putpixel((x,y), val)
    res.paste(crop, min)
    return res


#replace some bits of all pixel, according to the mode, if its msb and number of bits
def imgFullNoise(img, nbBit, msb : bool, mode, min, max): #mode = 0 : remplace par des 0, 1 : remplace par des 1, 2 : random
    random.seed(seedV)
    res = img.copy()
    crop = cropImage(img, min, max)
    for x in range(crop.width):
        for y in range (crop.height):
            pix = crop.getpixel((x,y))
            pixVal = list(pix)

            for c in range(len(pix)):
                if(c < 4):
                    noise = 0
                    mask = 0b11111111
                    if(mode == 1):
                        for i in range (nbBit):
                            noise = (noise << 1) | 1
                    elif(mode == 2):
                        noise = random.getrandbits(nbBit)

                    if(msb):
                        mask = (mask >> nbBit)& 0b11111111
                        noise = (noise << 8-nbBit) &  0b11111111
                    else :
                        mask = (mask << nbBit) & 0b11111111
                    pixVal[c] = (pixVal[c] & mask) | noise

            pix = tuple(pixVal)
            crop.putpixel((x,y), pix)
    res.paste(crop, min)
    return res

def imgShuffle(img, min, max):
    np.random.seed(seed=seedV)

    res = img.copy()

    crop = cropImage(img, min, max)
    w, h = crop.size
    size = w*h
    cropData = crop.getdata()
    bands = len(crop.getbands())
    cropData = np.reshape(cropData, (size, bands))
    np.random.shuffle(cropData)
    cropData = np.reshape(cropData, (h,w, bands))
    
    res.paste(Image.fromarray(cropData.astype('uint8')), min)

    return res