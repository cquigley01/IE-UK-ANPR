from firebase import helperFunctions
import unittest

class TestRegistrationInfo(unittest.TestCase):


    def test_send_reg_info(self):
        test_reg_plate = "AB123CD"
        test_img_path = "img.jpg"
        test_uid = 123
        helperFunctions.addToDatabase(test_reg_plate, test_img_path, test_uid)
        response = helperFunctions.getInfoFromReg(test_reg_plate)

        self.assertEqual(response['reg_plate'], test_reg_plate)
        self.assertEqual(response['image'], test_img_path)
        self.assertEqual(response['userID'], test_uid)


if __name__ == '__main__':
    unittest.main()
