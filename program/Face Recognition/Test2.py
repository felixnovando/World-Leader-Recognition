from Model import Detector, Recognizer
import cv2
import matplotlib.pyplot as plt
import Data
import urllib
import numpy as np

detector = Detector()

def load_testing_image():
    list_bgr_image = []
    list_cropped_gray_faces = [] #array of arrays
    list_image_face_corrdinates = [] #array of arrays

    image_urls = Data.get_final_photo()

    for image_url in image_urls:
        #load image from web
        image_url = image_url.replace(" ", "%20")
        response = urllib.request.urlopen(image_url)
        img_array = np.array(bytearray(response.read()), dtype=np.uint8)
        bgr_image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        #resize image
        bgr_image = cv2.resize(bgr_image, (1000, 600), interpolation=cv2.INTER_AREA)

        #grayscale image
        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

        #detect face
        detected_faces = detector.detectFace(gray_image)

        if len(detected_faces) < 1:
            continue
        
        cropped_gray_faces = []
        image_face_corrdinates = []

        for face in detected_faces:
            x, y, h, w = face
            cropped_face = gray_image[y:y+h, x:x+w]

            cropped_gray_faces.append(cropped_face)
            image_face_corrdinates.append(face)
        
        list_cropped_gray_faces.append(cropped_gray_faces)
        list_image_face_corrdinates.append(image_face_corrdinates)
        list_bgr_image.append(bgr_image)

    return list_cropped_gray_faces, list_image_face_corrdinates, list_bgr_image


def predict_and_draw_image_faces(clf, cropped_gray_faces, image_face_coordinates, bgr_image, classes):
    results = [clf.predict(cropped_gray_face) for cropped_gray_face in cropped_gray_faces]

    for (result, face_coordinate) in zip(results, image_face_coordinates):
        x, y, h, w = face_coordinate
        name_label = classes[result]
        cv2.rectangle(bgr_image, (x, y), (x+w, y+h), (0, 255, 0), 3)
        cv2.putText(bgr_image, name_label, (x-25, y-10), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 255, 0), 2)
    
    return bgr_image


def display_result(drawn_images):
    plt.figure("World Leaders")
    for idx, image in enumerate(drawn_images):
        plt.subplot(2, 2, idx+1)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.xticks([])
        plt.yticks([])
    plt.show()

if __name__ == "__main__":

    classes = Data.get_all_label()

    list_cropped_gray_faces, list_image_face_corrdinates, list_bgr_image = load_testing_image()

    #model
    clf = Recognizer()

    #load data
    clf.load()

    #draw faces
    drawn_images = []
    for (cropped_gray_face, image_face_coordinates, bgr_image) in zip(list_cropped_gray_faces, list_image_face_corrdinates, list_bgr_image):
        drawn_images.append(predict_and_draw_image_faces(clf, cropped_gray_face, image_face_coordinates, bgr_image, classes))

    #display result
    display_result(drawn_images)
