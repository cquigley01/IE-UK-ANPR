from anpr import *
import unittest
import re

irish_plate_pattern = re.compile(r'^(\d{2,3})(1|2)?[A-Z]{1,2}\d{1,6}$', re.IGNORECASE)
uk_plate_pattern = re.compile(r'^([A-Z]{2}\d{2}[A-Z]{3})|([A-Z]{3}\d{1,4})$', re.IGNORECASE)

class TestRegistrationRegex(unittest.TestCase):
    def test_valid_irish_plates(self):
        valid_plates = ["191G1234", "05D567", "12KK56789", "00DL123456"]
        for plate in valid_plates:
            self.assertTrue(re.match(irish_plate_pattern, plate))

    def test_invalid_irish_plates(self):
        invalid_plates = ["AB1234","12834MH131", "191H1234567", "151AB"]
        for plate in invalid_plates:
            self.assertFalse(re.match(irish_plate_pattern, plate))

    def test_valid_uk_plates(self):
        valid_plates = ["FSZ7202", "WJ66AKZ", "FM21DSU"]
        for plate in valid_plates:
            self.assertTrue(re.match(uk_plate_pattern, plate))

    def test_invalid_uk_plates(self):
        invalid_plates = ["1234ABCD", "AB1234", "AA111AA1"]
        for plate in invalid_plates:
            self.assertFalse(re.match(uk_plate_pattern, plate))



class TestMostCommonPlate(unittest.TestCase):

    def test_most_common_plate(self):
        # Test data with multiple occurrences of the same plate
        test_data = ["EI2345", "01D234", "GB123456", "YY123", "YY123", "XX99999", "AB12CD", "YY123"]
        expected_plate = "YY123"  # YY123 appears most frequently

        most_common_plate = most_common_plate_manual(test_data)
        self.assertEqual(most_common_plate, expected_plate)

        # Test data with a tie for most common plate
        test_data = ["EI2345", "01D234", "GB123456", "YY123", "XX99999", "AB12CD", "XX99999"]
        expected_plate = "XX99999"

        most_common_plate = most_common_plate_manual(test_data)
        self.assertEqual(most_common_plate, expected_plate)





if __name__ == '__main__':
    unittest.main()