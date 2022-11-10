# import matplotlib.pyplot as plt
# from keras.datasets import cifar10
# from keras.models import Sequential, load_model
# from keras.layers import Dense, Dropout, Conv2D, MaxPool2D, Flatten, Input

import logging, os
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import numpy as np
import tensorflow as tf 
from keras.utils import np_utils, load_img, img_to_array
from keras.applications import EfficientNetV2L as Construct
from keras.applications import efficientnet_v2 as Architecture

def load_imagenet_model():
  global imagenet_model
  imagenet_model = Construct(
    weights="imagenet",
    classes=1000
  )

def predict_imagenet(path_img):
  global imagenet_model
  #img = tf.expand_dims(img_to_array(load_img(path_img)))
  img = tf.expand_dims(img_to_array(load_img(path_img, target_size=(480,480))),0)
  #img = Architecture.preprocess_input(img)
  predictions = imagenet_model.predict(img)
  print('Shape: {}'.format(predictions.shape))
  for name, desc, score in Architecture.decode_predictions(predictions)[0]:
    print(f"-{desc} : {100*score}")
  
"""
cifar10_label = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

def predictModel(path_model, path_img):
  model = load_model(path_model, compile = True)
  img = tf.expand_dims(img_to_array(load_img(path_img, target_size=(32,32))),0)
  predictions = model.predict(img)
  res = predictions.argmax(axis=-1)
  print(cifar10_label[res[0]])



def classifier():
    # loading the dataset
    (X_train, y_train), (X_test, y_test) = cifar10.load_data()

    # building the input vector from the 32x32 pixels
    X_train = X_train.reshape(X_train.shape[0], 32, 32, 3)
    X_test = X_test.reshape(X_test.shape[0], 32, 32, 3)
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')

    # normalizing the data to help with the training
    print('>>> Before normalization : Min={}, Max={}'.format(X_train.min(), X_train.max()))
    X_train /= 255
    X_test /= 255
    print('>>> After normalization : Min={}, Max={}'.format(X_train.min(), X_train.max()))

    # one-hot encoding using keras' numpy-related utilities
    n_classes = 10
    print(">>> Shape before one-hot encoding: ", y_train.shape)
    Y_train = np_utils.to_categorical(y_train, n_classes)
    Y_test = np_utils.to_categorical(y_test, n_classes)
    print(">>> Shape after one-hot encoding: ", Y_train.shape)

    # building a linear stack of layers with the sequential model
    model = Sequential()

    # input 32*32 RGB images
    model.add( Input(shape=(32,32,3)) ) 

    # convolutional layer
    model.add( Conv2D(50, (3,3), activation='relu') )

    model.add( Conv2D(75, (3,3), activation='relu') )
    model.add( MaxPool2D((2,2)))
    model.add( Dropout(0.25) )

    model.add( Conv2D(125, (3,3), activation='relu') )
    model.add( MaxPool2D((2,2)))
    model.add( Dropout(0.25) )

    # flatten output of conv
    model.add( Flatten() )

    # hidden layer
    model.add( Dense(500, activation='relu') )
    model.add( Dropout(0.4) )
    model.add( Dense(250, activation='relu') )
    model.add( Dropout(0.3) )

    # output layer
    model.add( Dense(10, activation='softmax') )

    # Compiling the sequential model
    model.compile(
        loss='categorical_crossentropy', 
        metrics=['accuracy'], 
        optimizer='adam'
    )

    # Sums parameters and output shape
    model.summary()

    # Training the model
    history = model.fit(
        X_train, 
        Y_train, 
        batch_size=1024, 
        epochs=64, 
        validation_data=(X_test, Y_test)
    )

    # Accuracy
    score = model.evaluate(X_test, Y_test, verbose=0)
    print(f'Test loss     : {score[0]:4.4f}')
    print(f'Test accuracy : {score[1]:4.4f}')

    # plot Accuracy
    model.metrics_names
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc=('upper left'))
    plt.show()

    # Save : creates a SavedModel folder "my_model"
    model.save('my_model')

    # Reload
    # reconstructed_model = keras.models.load_model("my_model")

    # Check
    np.testing.assert_allclose(
      model.predict(test_input), reconstructed_model.predict(test_input)
    )

    # The reconstructed model is already compiled and has retained the optimizer state, so training can resume:
    # reconstructed_model.fit(test_input, test_target)


class estimator:
  _estimator_type = ''
  classes = []
  def __init__(self, model, classes):
    self.model = model
    self._estimator_type = 'classifier'
    self.classes = classes
  def predict(self, X):
    y_prob = self.model.predict(X)
    y_pred = y_prob.argmax(axis=1)
    return y_pred

class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
classifier = estimator(model, class_names)
plot_confusion_matrix(estimator=classifier, X=x_test, y_true=y_test)
"""