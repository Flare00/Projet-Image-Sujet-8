#!/usr/bin/env python3

import numpy as np
from mtcnn import MTCNN
 
class Model_MTCNN:
    def __init__(self):
        self.detector = MTCNN()
    
    def makePrediction(self, imageTest, threshold=0.9):
        detections = self.detector.detect_faces(np.array(imageTest))
        res = []
        if not detections:
            print("INFO : MTCNN found nothing")
        else:
            for d in detections:
                arr = []
                score = d["confidence"]
                arr.append(score)
                if score > threshold:
                    arr.append(d["box"]) # (x, y, w, h) : y -> y+h | x -> x+w
                res.append(arr)

        return res