import cv2
import numpy as np

# Cascade yükleme
cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

# Video dosyasını yükleme
video = cv2.VideoCapture('CarVideos/test_video.mp4')


# Oranlı olarak yeniden boyutlandırma fonksiyonu
def resize_frame(frame, height=500):
    # Yükseklik 500 piksel olarak ayarlanır
    ratio = height / float(frame.shape[0])
    dim = (int(frame.shape[1] * ratio), height)
    # Görüntüyü yeniden boyutlandır
    resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    return resized


# Video'nun kaydedileceği VideoWriter nesnesini tanımlama
out = None

# Video karelerini işleme
while True:
    ret, frame = video.read()
    if not ret:
        break

    # Görüntüyü gri tona dönüştürme
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Plaka tespiti
    cars_detected = cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )

    # Plakaları dikdörtgenle işaretleme ve kırpma
    for (x, y, w, h) in cars_detected:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (145, 60, 255), 5)

        # Plakayı kırpma
        plate = frame[y:y + h, x:x + w]

        # Kırpılmış plakayı yeni bir pencerede gösterme
        cv2.imshow("Cropped License Plate", plate)

    # İşlenen kareyi yeniden boyutlandırma
    resized_frame = resize_frame(frame)

    # VideoWriter nesnesini yalnızca ilk kareden sonra oluşturma
    if out is None:
        (h, w) = resized_frame.shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output_video.avi', fourcc, 20.0, (w, h))

    # İşlenen ve yeniden boyutlandırılmış kareyi kaydetme
    out.write(resized_frame)

    # Videodaki yeniden boyutlandırılmış kareyi gösterme
    cv2.imshow("Video", resized_frame)

    # 'q' tuşuna basıldığında döngüyü sonlandırma
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tüm pencereleri kapatma ve video nesnelerini serbest bırakma
video.release()
out.release()
cv2.destroyAllWindows()
