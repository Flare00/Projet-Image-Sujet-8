import tensorflow as tf 
from PIL import Image
import numpy as np
import cv2

#From https://www.kaggle.com/code/akhileshdkapse/sr-super-resolution-gan-keras/notebook
class SubpixelConv2D(tf.keras.layers.Layer):
    def __init__(self, upsampling_factor=2, **kwargs):
        super(SubpixelConv2D, self).__init__(**kwargs)
        self.upsampling_factor = upsampling_factor

    def build(self, input_shape):
        last_dim = input_shape[-1]
        factor = self.upsampling_factor * self.upsampling_factor
        if last_dim % (factor) != 0:
            raise ValueError('Channel ' + str(last_dim) + ' should be of '
                             'integer times of upsampling_factor^2: ' +
                             str(factor) + '.')

    def call(self, inputs, **kwargs):
        return tf.nn.depth_to_space( inputs, self.upsampling_factor )

    def get_config(self):
        config = { 'upsampling_factor': self.upsampling_factor, }
        base_config = super(SubpixelConv2D, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    def compute_output_shape(self, input_shape):
        factor = self.upsampling_factor * self.upsampling_factor
        input_shape_1 = None
        if input_shape[1] is not None:
            input_shape_1 = input_shape[1] * self.upsampling_factor
        input_shape_2 = None
        if input_shape[2] is not None:
            input_shape_2 = input_shape[2] * self.upsampling_factor
        dims = [ input_shape[0],
                 input_shape_1,
                 input_shape_2,
                 int(input_shape[3]/factor)
               ]
        return tuple( dims )

class SRGAN:
    def __init__(self):
        print("Load SRGAN Weights")
        self.gan = tf.keras.models.load_model("model/srgan.h5", custom_objects={"SubpixelConv2D": SubpixelConv2D })

    def makePrediction(self, img):
        res = None
        if (self.gan is not None):
            input_w, input_h = 96, 96
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
            

    