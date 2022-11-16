#!/usr/bin/env python3

import logging, os

logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
print("Loading TensorFlow...")

import PIL.Image
# import os
# import src.filter as filter
# import src.classifier as classifier
# import src.metric as metric
import src.interface as interface
import src.yoloDetection as yolo

def main():

    # Image input
    """
    img = PIL.Image.open("input/ex.png")
    w,h = img.size
	"""
    # Filters
    """
    imgPixel = filter.imgPixelate(img, 4, (15, 15), (w-15, h-15))
    imgBlur = filter.imgBlurring(img, 2, (15, 15), (w-15, h-15))
    imgRandNoise = filter.imgRandomNoise(img, 0.5, True, (15, 15), (w-15, h-15))
    imgNoise = filter.imgFullNoise(img, 2, True, 2, (15, 15), (w-15, h-15))
    imgShuffle = filter.imgShuffle(img, (15, 15), (w-15, h-15))
	"""
    # Metrics
    """
    print(metric.metric_MSE(img, img))
    print(metric.metric_RMSE(img, img))
    print(metric.metric_PSNR(img, img))
    print(metric.metric_SSIM(img, img))
    print(metric.metric_SAM(img, img))
    print(metric.metric_HaarPSI(img, img))
    """

    # Save
    """
    imgPixel.save(outputFolder+'test_pixel.png', 'png')
    imgBlur.save(outputFolder+'test_blur.png', 'png')
    imgRandNoise.save(outputFolder+'test_random_noise.png', 'png')
    imgNoise.save(outputFolder+'test_full_noise.png', 'png')
    imgShuffle.save(outputFolder+'test_suffle.png', 'png')
	"""
    ### Classifier Creation
    # classifier.classifier()
    # classifier.predictModel('my_model', 'input/Cat03.jpg')
    
    ### Classifier Model
    # classifier.load_imagenet_model()
    # classifier.predict_imagenet('input/Beer_mug_transparent.png')

    ### Yolo Detection
    """
    yolo.create_save_yolov3Model()
    yolo.make_prediction()
    """
    img = PIL.Image.open("input/img2.jpg")
    m = yolo.Model_YOLO("./model/")
    m.makePrediction(img)
    

    ### Interface
    # interface.initInterface()
    # interface.startInterface()

if __name__== "__main__":
    main()
