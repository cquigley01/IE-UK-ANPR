import easyocr
from picamera2 import Picamera2
import numpy as np
harcascade = "../../model/haarcascade_russian_plate_number.xml"
reader = easyocr.Reader(['en'], gpu=False)

def startCapture():
    from cv2 import CascadeClassifier, cvtColor, COLOR_BGR2GRAY
    print("Creating Picamera2 instance...")
    piCam = Picamera2()
    print("Creating video configuration...")
    video_config = piCam.create_video_configuration(main={"size": (640, 480)}, controls={"FrameRate": 3.0})
    print("Configuring camera...")
    piCam.configure(video_config)
    print("Starting camera...")
    piCam.start()
    print("Camera Started")
    i = 0
    valid = []
    while i < 5:
        img = piCam.capture_array()
        plate_cascade = CascadeClassifier(harcascade)
        img_gray = cvtColor(img, COLOR_BGR2GRAY)
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
    from cv2 import equalizeHist, adaptiveThreshold, morphologyEx, THRESH_BINARY_INV, ADAPTIVE_THRESH_GAUSSIAN_C, dilate, MORPH_CLOSE, MORPH_CLOSE, MORPH_OPEN
    # Apply Gaussian blur to reduce noise
    #blur = cv2.GaussianBlur(gray, (5, 5), 0)
    equalized = equalizeHist(img)
    #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    #equalized = clahe.apply(gray)
    # Use adaptive thresholding to highlight text
    # cv2.ADAPTIVE_THRESH_GAUSSIAN_C for Gaussian-weighted sums
    # cv2.THRESH_BINARY_INV to invert the black and white (make text white on black background)
    # Block size of 11 and a C value of 2 seems to work well in many cases, but you may need to adjust these for your specific images
    thresh = adaptiveThreshold(equalized, 255, ADAPTIVE_THRESH_GAUSSIAN_C,
                               THRESH_BINARY_INV, 9, 31)
    # Optionally, you can dilate the text a bit to make it more contiguous
    # This can help if the text characters are broken up
    kernel = np.ones((1,1), np.uint8)
    closing = morphologyEx(thresh, MORPH_CLOSE, kernel)
    opening = morphologyEx(closing, MORPH_OPEN, kernel)
    dilated = dilate(opening, kernel, iterations=1)
    #cv2.imwrite('processed_image.jpg', dilated)
    return dilated
