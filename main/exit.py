from anpr import *
from firebase import *


def main():
    regPlatesCaptured = windows_imageProcess.startCapture() # Capture Areas for reg plates, return list
    corrections = config.correct_and_find_plates(regPlatesCaptured) # Take a list of posssible reg plates and run through regular expression return predictions
    plate = config.most_common_plate_manual(corrections) # Find most common plate using an O(n) algo. Return most common reg
    updateExitTime(plate)
    userID = findCustomerAccount(plate)
    response = getInfoFromReg(plate)
    customerData = getCustomerInfoFromReg(plate)
    customerBalance = customerData['balance']
    img_path = response['image']
    entryTime = response['entryTime']
    exitTime = response['exitTime']

    if userID == "null" or "":
        if check_payment_status(plate) == True:
            print("Gate Open")
        else:
            print("Not Paid", plate)
    else:
        cost = calculateCost(entryTime,exitTime)
        if customerBalance > cost:
            updateCustomerBalance(plate, customerBalance - cost)
            createHistory(plate, img_path, userID, entryTime, exitTime, cost)
            deleteSession(plate)
            print("Gate Open")
        else:
            print(f"{plate} has balance {customerBalance} for but cost is {cost}")





if __name__ == "__main__":
    main()