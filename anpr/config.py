import re

def correct_and_find_plates(ocr_detections):

    corrected_plates = []
    irish_plate_pattern = re.compile(r'^(\d{2,3})(1|2)?[A-Z]{1,2}\d{1,6}$', re.IGNORECASE)
    uk_plate_pattern = re.compile(r'^([A-Z]{2}\d{2}[A-Z]{3})|([A-Z]{3}\d{1,4})$', re.IGNORECASE)

    for detection in ocr_detections:

        corrected_detection = detection.replace('I', '1')
        corrected_detectionT = corrected_detection.replace('0', 'D')

        print("Corrected I-1:", corrected_detection, "Corrected 0-D:",corrected_detectionT)

        if irish_plate_pattern.match(corrected_detectionT) or uk_plate_pattern.match(corrected_detectionT):
            corrected_plates.append(corrected_detectionT.upper())
    return corrected_plates


#O(N) time complexity
def most_common_plate_manual(plates):
    # Dictionary to store plate counts
    plate_counts = {}

    # Loop through each plate in the list
    for plate in plates:
        if plate in plate_counts:
            # Increment the count of the plate if it's already in the dictionary
            plate_counts[plate] += 1
        else:
            # Add the plate to the dictionary with an initial count of 1
            plate_counts[plate] = 1

    # Find the plate with the maximum count
    most_common = None
    max_count = -1
    for plate, count in plate_counts.items():
        if count > max_count:
            most_common = plate
            max_count = count

    return most_common