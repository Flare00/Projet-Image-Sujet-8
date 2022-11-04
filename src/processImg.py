#!/usr/bin/env python3
from PIL import Image, ImageFilter
import random

def imgPixelate(img, n):
    return img.resize((n,n), resample=Image.Resampling.BILINEAR).resize(img.size, Image.Resampling.NEAREST)

def imgBlurring(img, n):
    return img.filter(ImageFilter.GaussianBlur(n))

def imgRandomNoise(img, chance, randomPix: bool): #Replace random pixel by black
    res = img.copy()
    for x in range(img.width):
        for y in range (img.height):
            if(random.random() < chance):
                val = 0
                if(randomPix):
                    if(len(res.getpixel((x,y))) == 1):
                        val = (random.randint(0,255))
                    if(len(res.getpixel((x,y))) == 3):
                        val = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    if(len(res.getpixel((x,y))) == 4):
                        val = (random.randint(0,255), random.randint(0,255), random.randint(0,255), 255)
                res.putpixel((x,y), val)
    return res


#replace some bits of all pixel, according to the mode, if its msb and number of bits
def imgFullNoise(img, nbBit, msb : bool, mode): #mode = 0 : remplace par des 0, 1 : remplace par des 1, 2 : random
    res = img.copy()
    for x in range(img.width):
        for y in range (img.height):
            pix = res.getpixel((x,y))
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
            res.putpixel((x,y), pix)
    return res

        
        

def main():
    # Image input with size
    img = Image.open("rock.jpg")

    imgRandNoise = imgRandomNoise(img, 0.5, True)
    imgNoise = imgFullNoise(img, 2, True, 2)
    # Processing
    imgPixel = imgPixelate(img, 16)
    imgBlur = imgBlurring(img, 5)
    imgNoiseBlur = imgBlurring(imgNoise, 5)
    # Save
    
    imgRandNoise.save('test_random_noise.png', 'png')
    imgNoiseBlur.save('test_noise_blur.png', 'png')
    imgNoise.save('test_full_noise.png', 'png')
    imgPixel.save('test_pixel.png', 'png')
    imgBlur.save('test_blur.png', 'png')

if __name__== "__main__":
    main()
