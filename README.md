# Safe-Eye : CNN Visual Safety Rating of Obfuscated Images
This project aims to offer a program capable of anonymizing the sensitive elements of an image according to various image obfuscation processes (pixelating, blurring, masking, etc).  
A measure of security and a measure of the quality of the image can thus be offered to the user.  
This is a university project on which the students will be graded.

## Members
Florentin DENIS  
Khélian LARVET  
(University of Montpellier : M2 IMAGINE, 2022-2023)

## Dependencies
- Python : v3.0
- Tkinter (GUI toolkit) : v8.6
- Python Imaging Library (PIL) : v9.3.0
- NumPy : v1.23.4
- Keras : v2.10.0
- TensorFlow : v2.10.0
- MTCNN architecture : v0.1.1

```console
pip install tk
pip install pillow  
pip install numpy  
pip install keras  
pip install tensorflow
pip install mtcnn

cd src/yolo-coco 
wget "https://pjreddie.com/media/files/yolov3.weights" 
cd ../../
```
If you don't have wget, you can also download the weights file (https://pjreddie.com/media/files/yolov3.weights) and put it in src/yolo-coco