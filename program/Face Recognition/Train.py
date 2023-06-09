from Model import Detector, Recognizer
import cv2
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
import Data
import urllib

detector = Detector()

def augment_image(image):
    #flip image
    flipped_image = cv2.flip(image, 1)
    #rotate
    rotate_degrees = [20, 15, 10, 5]
    images = []

    images.append(image)
    images.append(flipped_image)

    #image rotation
    for degree in rotate_degrees:
        images.append(ndimage.rotate(image, degree))
        images.append(ndimage.rotate(image, degree * -1))
        images.append(ndimage.rotate(flipped_image, degree))
        images.append(ndimage.rotate(flipped_image, degree * -1))

    return images


def load_datasets():
    cropped_gray_faces = []
    face_labels = []

    images_url, labels = Data.get_assets()

    for image_url, label in zip(images_url, labels):
        #load grayscale image from web
        image_url = image_url.replace(" ", "%20")
        response = urllib.request.urlopen(image_url)
        img_array = np.array(bytearray(response.read()), dtype=np.uint8)
        gray_image = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)

        #resize image
        gray_image = cv2.resize(gray_image, (250, 250), interpolation=cv2.INTER_AREA)

        #augment image
        augmented_images = augment_image(gray_image)

        for img in augmented_images:
            #detect face
            detected_faces = detector.detectFace(img)

            if len(detected_faces) < 1:
                continue

            for face in detected_faces:
                x, y, h, w = face
                cropped_face = img[y:y+h, x:x+w]
                cropped_gray_faces.append(cropped_face)
                face_labels.append(label)

    return cropped_gray_faces, face_labels


def evaluate(y_test, y_pred, labels):
    #get accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\naccuracy: {accuracy*100} %\n")

    #get num labels
    num_labels = [i for i in range(len(labels))]

    #confusion matrix
    cm = confusion_matrix(y_test, y_pred, num_labels)
    display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.array(num_labels))
    
    display.plot()
    display.ax_.set_title("Prediction Confusion Matrix")
    plt.show()


if __name__ == "__main__":

    classes = Data.get_all_label()

    cropped_gray_faces, face_labels = load_datasets()

    print(f"Number of images: {len(cropped_gray_faces)}")

    #split dataset into training and testing
    X_train, X_test, y_train, y_test = train_test_split(cropped_gray_faces, face_labels, test_size=0.08, random_state=42)

    #model
    clf = Recognizer()

    #train
    clf.train(X_train, y_train)
    
    #save model
    clf.save()

    #get prediction result
    y_pred = [clf.predict(X) for X in X_test]

    evaluate(y_test, y_pred, classes)