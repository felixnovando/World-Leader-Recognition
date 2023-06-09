import cv2
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()
MODEL_PATH = os.getenv("MODEL_PATH")

class Recognizer:
    def __init__(self):
        self.__recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    def train(self, datas, labels):
        self.__recognizer.train(datas, np.array(labels))

    def predict(self, data):
        res, _  = self.__recognizer.predict(data)
        return res

    def save(self):
        print("Saving model data...")
        self.__recognizer.write(MODEL_PATH)

    def load(self):
        if os.path.isfile(MODEL_PATH) == True:
            print("Importing model data...")
            self.__recognizer.read(MODEL_PATH)
        else:
            print("No data loaded")   


class Detector:
    def __init__(self):
        self.__face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    def detectFace(self, gray_image):
        return self.__face_cascade.detectMultiScale(gray_image, scaleFactor=1.2, minNeighbors=5)
