import cv2
import numpy as np
import matplotlib.pyplot as plt

cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

cars = cv2.imread('CarPictures/testImage3.jpg')

gray = cv2.cvtColor(cars, cv2.COLOR_BGR2GRAY)

def convertToRGB(image):
    return cv2.cvtColor(image,cv2.COLOR_BGR2RGB)


cars_detected = cascade.detectMultiScale(
    gray,
    scaleFactor=1.2,
    minNeighbors=5,
    minSize=(20,2)
)

print('found_Numbers', len(cars_detected))

for (x,y,w,h) in cars_detected:
    cv2.rectangle(cars, (x,y),(x+w,y+h),(145, 60, 255),5)

    plate = cars[y:y + h, x:x + w]

    # Kırpılmış plakayı yeni bir pencerede gösterme
    cv2.imshow("Cropped License Plate", plate)
    cv2.waitKey(0)

plt.imshow(convertToRGB(cars))
plt.imsave('Detected.png',convertToRGB(cars))
plt.waitforbuttonpress()