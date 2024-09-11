import time

import easyocr
import numpy as np
import cv2

harcascade = "../model/haarcascade_russian_plate_number.xml"
reader = easyocr.Reader(['en'], gpu=False)

def startCapture():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    i = 0
    valid = []

    while i < 5:
        success, img = cap.read()
        plate_cascade = cv2.CascadeClassifier(harcascade)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

        for (x,y,w,h) in plates:
            #cv2.imwrite('unprocessed_image.jpg', img)
            #img_path = 'unprocessed_image.jpg'
            img_roi = img_gray[y: y+h, x:x+w]
            processed_image = preprocess_image_for_ocr(img_roi)
            detections = reader.readtext(processed_image)

            for detection in detections:
                bbox, text, score = detection
                text = text.upper().replace(' ', '')
                text = text.upper().replace(':', '-')
                text = text.upper().replace('_', '-')
                text = text.upper().replace('-', '')
                print("Found:", text, "{:.3f}".format(score))
                valid.append(text)
                i = i + 1

    return valid

def preprocess_image_for_ocr(img):

    equalized = cv2.equalizeHist(img)

    thresh = cv2.adaptiveThreshold(equalized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 31)
    kernel = np.ones((1,1), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
    dilated = cv2.dilate(opening, kernel, iterations=4)
    cv2.imwrite('imgthis.jpg', dilated)
    cv2.imwrite('2.jpg', thresh)
    return dilated
