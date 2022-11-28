import tensorflow as tf 
from PIL import Image
import numpy as np
import cv2

class SRGAN:
    def __init__(self):
        print("Load SRGAN Weights")
        self.gan = tf.keras.models.load_model("model/srgan.h5")

    def makePrediction(self, img):
        res = None
        if (self.gan is not None):
            input_w, input_h = 384, 384
            img = img.resize((input_w, input_h))
            img = tf.keras.utils.img_to_array(img)
            img = img.astype('float32')
            img /= 255.0
            img = np.expand_dims(img, 0)

            res = self.gan.predict(img)[0]
            res = res*255.0
            res = res.astype(np.uint8)
            res = Image.fromarray(res)
            res.show()
        return res
            

    