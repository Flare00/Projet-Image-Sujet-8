#!/usr/bin/env python3

import logging, os
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
print("[INFO] Loading TensorFlow...")

import src.interface as interface
print("[INFO] TensorFlow Loaded.")

def main():

    """
    img = Image.open("input/imgtest.jpg")
    w,h = img.size
    imgPixel = filter.imgPixelate(img, 4, (0, 0), (w, h))
    pixel = filter.resizeByPixelSize(imgPixel)
    
    
    model = edsr.edsr(scale=4, num_res_blocks=16)
    model.load_weights('src/super-resolution/edsr_weights.h5')

    #lr = np.array(imgPixel)
    sr = resolve_single(model, np.array(pixel))
    #sr = resolve_single(model, np.array(Image.open("sr.jpg")))

    #img = Image.fromarray(np.uint8(lr))
    #img.save("lr.jpg")
    sr = Image.fromarray(np.uint8(sr))
    sr.save("sre.jpg")
    
    # pixel.save("pixel.jpg")
    # imgPixel.save("lr.jpg")
    """

    interface.initInterface()
    interface.startInterface()

if __name__== "__main__":
    main()





### ARCHIVES
"""
    import PIL.Image
    import os
    import src.filter as filter
    import src.classifier as classifier
    import src.metric as metric
    import src.yoloDetection as yolo

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
    print(metric.metric_MSE(img, img))
    print(metric.metric_RMSE(img, img))
    print(metric.metric_PSNR(img, img))
    print(metric.metric_SSIM(img, img))
    print(metric.metric_SAM(img, img))
    print(metric.metric_HaarPSI(img, img))

    # Save
    imgPixel.save(outputFolder+'test_pixel.png', 'png')
    imgBlur.save(outputFolder+'test_blur.png', 'png')
    imgRandNoise.save(outputFolder+'test_random_noise.png', 'png')
    imgNoise.save(outputFolder+'test_full_noise.png', 'png')
    imgShuffle.save(outputFolder+'test_suffle.png', 'png')

    ### My Classifier
    # classifier.classifier()
    # classifier.predictModel('my_model', 'input/Cat03.jpg')
    
    ### EfficientNetV2L Classifier 
    # classifier.load_imagenet_model()
    # classifier.predict_imagenet('input/Beer_mug_transparent.png')

    ### Yolo Detection
    img = PIL.Image.open("input/img2.jpg")
    m = yolo.Model_YOLO("./model/")
    m.makePrediction(img)
    """