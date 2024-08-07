import cv2
import imutils
import numpy as np
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Kamerayı başlat
cap = cv2.VideoCapture(0)
fps = 15
delay = int(1000 / fps)

while True:
    start_time = time.time()

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (600, 400))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gürültüyü azaltma (Blur)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Kenar tespiti (Canny)
    edged = cv2.Canny(blurred, 30, 200)

    # Kenarları belirgin hale getirme (Dilate)
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edged, kernel, iterations=1)

    # Konturları bulma
    contours = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print("No contour detected")
    else:
        detected = 1

    if detected == 1:
        cv2.drawContours(frame, [screenCnt], -1, (0, 0, 255), 3)

        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
        new_image = cv2.bitwise_and(frame, frame, mask=mask)

        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

        text = pytesseract.image_to_string(Cropped, config='--psm 11')
        print("Plaka Tanıma Programlaması\n")
        print("Plaka Numarası:", text)

    cv2.imshow('Araba', frame)

    # Gecikmeyi ayarla
    elapsed_time = (time.time() - start_time) * 1000
    remaining_time = delay - elapsed_time
    if remaining_time > 0:
        cv2.waitKey(int(remaining_time))
    else:
        cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
