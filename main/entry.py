from anpr import *
from firebase import *


def main():
    regPlatesCaptured = windows_imageProcess.startCapture() # Capture Areas for reg plates, return list
    corrections = config.correct_and_find_plates(regPlatesCaptured) # Take a list of posssible reg plates and run through regular expression return predictions
    plate = most_common_plate_manual(corrections) # Find most common plate using an O(n) algo. Return most common reg
    img_bucket_url = upload_file("../tests/img.jpg", plate) #Upload the region of interest and return the path
    user_from_reg = findCustomerAccount(plate) #Find the users UID from their registration plate and return UID if account exists else null
    addToDatabase(plate, img_bucket_url, user_from_reg) #Make post request to firebase firestore and add plate, time image, and UID/Null
    print(plate)


if __name__ == "__main__":
    main()