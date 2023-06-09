from Model import Detector, Recognizer
import cv2
import random
import numpy as np
import Data
import urllib

detector = Detector()


def load_random_images():
    bgr_images = []
    face_coordinates = []
    cropped_gray_faces = []
    image_labels = []

    images_url, labels = Data.get_assets()

    combined = [(image_url, label) for image_url, label in zip(images_url, labels)]
    random.shuffle(combined)

    #must be checked all image must have faces
    people_count = 0
    for image_url, label in combined:
        #load image from web
        image_url = image_url.replace(" ", "%20")
        response = urllib.request.urlopen(image_url)
        img_array = np.array(bytearray(response.read()), dtype=np.uint8)
        bgr_img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        #resize image
        bgr_img = cv2.resize(bgr_img, (250, 250), interpolation=cv2.INTER_AREA)

        #grayscale image
        gray_image = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)

        #detect face
        detected_faces = detector.detectFace(gray_image)

        if len(detected_faces) != 1:
            continue
        
        for face in detected_faces:
            x, y, h, w = face
            cropped_face = gray_image[y:y+h, x:x+w]

            cropped_gray_faces.append(cropped_face)
            bgr_images.append(bgr_img)
            face_coordinates.append(face)
            image_labels.append(label)

        people_count += 1
        if people_count >= 15:
            break
    
    return cropped_gray_faces, face_coordinates, bgr_images, image_labels


def draw_image_faces(face_coordinate, bgr_image, label, prediction, classes):
    x, y, w, h = face_coordinate
    name_label = classes[prediction]

    c = (0, 255, 0) if label == prediction else (0, 0, 255) 
    cv2.rectangle(bgr_image, (x, y), (x+w, y+h), c, 2)
    cv2.putText(bgr_image, name_label, (x-25, y-5), cv2.FONT_HERSHEY_DUPLEX, 0.5, c, 2)

    return bgr_image

def display_result(drawn_images):
    list_images = [drawn_images[0:5], drawn_images[5:10], drawn_images[10:15]]

    list_row_images = [np.hstack(images) for images in list_images]
    combined = np.vstack(list_row_images)
        
    cv2.imshow("Random 15 Images", combined)
    cv2.waitKey(0)


if __name__ == "__main__":

    classes = Data.get_all_label()

    #get 15 random images
    cropped_gray_faces, face_coordinates, bgr_images, labels = load_random_images()

    #model
    clf = Recognizer()

    #load data
    clf.load()

    #predict result
    predictions = [clf.predict(face) for face in cropped_gray_faces]

    #draw faces
    drawn_images = [draw_image_faces(face_coordinate, bgr_image, label, prediction, classes) for face_coordinate, bgr_image, label, prediction in zip(face_coordinates, bgr_images, labels, predictions)]

    #display result
    display_result(drawn_images)