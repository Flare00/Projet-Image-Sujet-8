#!/usr/bin/env python3
import PIL.Image
import os

import src.filter as filter
import src.interface as interface
import src.classifier as classifier
import src.metric as metric

outputFolder = "output/"

def main():
    # Image input
    img = PIL.Image.open("input/ex.png")
    w,h = img.size

    # Filters
    imgPixel = filter.imgPixelate(img, 4, (15, 15), (w-15, h-15))
    imgBlur = filter.imgBlurring(img, 2, (15, 15), (w-15, h-15))
    imgRandNoise = filter.imgRandomNoise(img, 0.5, True, (15, 15), (w-15, h-15))
    imgNoise = filter.imgFullNoise(img, 2, True, 2, (15, 15), (w-15, h-15))
    imgShuffle = filter.imgShuffle(img, (15, 15), (w-15, h-15))

    # Metrics
    """
    print("--- MSE")
    print(metric.metric_MSE(img, img))
    print(metric.metric_MSE(img, imgPixel))
    print(metric.metric_MSE(img, imgBlur))
    print(metric.metric_MSE(img, imgRandNoise))
    print(metric.metric_MSE(img, imgNoise))
    print("--- RMSE")
    print(metric.metric_RMSE(img, img))
    print(metric.metric_RMSE(img, imgPixel))
    print(metric.metric_RMSE(img, imgBlur))
    print(metric.metric_RMSE(img, imgRandNoise))
    print(metric.metric_RMSE(img, imgNoise))
    print("--- PSNR")
    print(metric.metric_PSNR(img, img))
    print(metric.metric_PSNR(img, imgPixel))
    print(metric.metric_PSNR(img, imgBlur))
    print(metric.metric_PSNR(img, imgRandNoise))
    print(metric.metric_PSNR(img, imgNoise))
    print("--- SSIM")
    print(metric.metric_SSIM(img, img))
    print(metric.metric_SSIM(img, imgPixel))
    print(metric.metric_SSIM(img, imgBlur))
    print(metric.metric_SSIM(img, imgRandNoise))
    print(metric.metric_SSIM(img, imgNoise))
    print("--- SAM")
    print(metric.metric_SAM(img, img))
    print(metric.metric_SAM(img, imgPixel))
    print(metric.metric_SAM(img, imgBlur))
    print(metric.metric_SAM(img, imgRandNoise))
    print(metric.metric_SAM(img, imgNoise))
    print("--- HaarPSI")
    print(metric.metric_HaarPSI(img, img))
    print(metric.metric_HaarPSI(img, imgPixel))
    print(metric.metric_HaarPSI(img, imgBlur))
    print(metric.metric_HaarPSI(img, imgRandNoise))
    print(metric.metric_HaarPSI(img, imgNoise))
    """

    # Folder Save
    if not(os.path.exists(outputFolder)):
        os.makedirs(outputFolder)
    
    # Save
    imgPixel.save(outputFolder+'test_pixel.png', 'png')
    imgBlur.save(outputFolder+'test_blur.png', 'png')
    imgRandNoise.save(outputFolder+'test_random_noise.png', 'png')
    imgNoise.save(outputFolder+'test_full_noise.png', 'png')
    imgShuffle.save(outputFolder+'test_suffle.png', 'png')

    ### Classifier Creation
    # classifier.classifier()
    # classifier.predictModel('my_model', 'input/Cat03.jpg')
    
    ### Classifier Model
    # classifier.load_imagenet_model()
    # classifier.predict_imagenet('input/Beer_mug_transparent.png')

    ### Interface
    # interface.initInterface()
    # interface.startInterface()

if __name__== "__main__":
    main()
