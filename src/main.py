#!/usr/bin/env python3
from PIL import Image
import filter

def main():
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

if __name__== "__main__":
    main()
