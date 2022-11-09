#!/usr/bin/env python3
import PIL.Image
import os

import src.filter as filter
import src.interface as interface
import src.classifier as classifier

outputFolder = "output/"

def main():
    # Image input with size
    img = PIL.Image.open("input/ex.png")

    # Filters
    imgPixel = filter.imgPixelate(img, 4, (25, 25), (100,125))
    imgBlur = filter.imgBlurring(img, 2, (25, 25), (100,125))
    imgRandNoise = filter.imgRandomNoise(img, 0.5, True, (25, 25), (100,125))
    imgNoise = filter.imgFullNoise(img, 2, True, 2, (25, 25), (100,125))
    # imgNoiseBlur = filter.imgBlurring(imgNoise, 5)

    # Save
    if not(os.path.exists(outputFolder)):
        os.makedirs(outputFolder)

    imgPixel.save(outputFolder+'test_pixel.png', 'png')
    imgBlur.save(outputFolder+'test_blur.png', 'png')
    imgRandNoise.save(outputFolder+'test_random_noise.png', 'png')
    imgNoise.save(outputFolder+'test_full_noise.png', 'png')
    # imgNoiseBlur.save(outputFolder+'test_noise_blur.png', 'png')

    # Classifier
    # classifier.classifier()
    #classifier.predictModel('my_model', 'input/Cat03.jpg')
    classifier.load_imagenet_model()
    classifier.predict_imagenet('input/Beer_mug_transparent.png')

    # Interface
    # interface.initInterface()
    # interface.startInterface()

if __name__== "__main__":
    main()
