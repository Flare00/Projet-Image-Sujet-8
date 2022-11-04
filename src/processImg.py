#!/usr/bin/env python3
from PIL import Image, ImageFilter


def imgPixelate(img, n):
    return img.resize((n,n), resample=Image.Resampling.BILINEAR).resize(img.size, Image.Resampling.NEAREST)

def imgBlurring(img, n):
    return img.filter(ImageFilter.GaussianBlur(n))

def main():
    # Image input with size
    img = Image.open("ex.png")

    # Processing
    imgPixel = imgPixelate(img, 16)
    imgBlur = imgBlurring(img, 5)
    
    # Save
    imgPixel.save('test_pixel.png', 'png')
    imgBlur.save('test_blur.png', 'png')


if __name__== "__main__":
    main()