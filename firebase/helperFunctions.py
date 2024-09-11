import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime, timedelta
import os
print(os.getcwd())

#Firebase Config
cred = credentials.Certificate('./firebase/acesstoken.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'parkit-c49c2.appspot.com'
})
db = firestore.client()


time_now = datetime.utcnow()


def findCustomerAccount(reg):
    users_ref = db.collection('users')
    query_ref = users_ref.where(u'reg', u'==', reg)

    results = list(query_ref.stream())  # Convert to list to handle easily

    if results:
        document = results[0]
        print('UserID:', document.to_dict()['uid'])

        userID = document.to_dict()['uid']
    else:
        print('No document found with that registration number.')
        userID = "null"

    return userID

def getInfoFromReg(reg):
    users_ref = db.collection('parkingsessions')
    query_ref = users_ref.where(u'reg_plate', u'==', reg)

    results = list(query_ref.stream())  # Convert to list to handle easily

    if results:
        document = results[0]
        results = document.to_dict()
    else:
        print('No document found with that registration number.')

    return results

def getCustomerInfoFromReg(reg):
    users_ref = db.collection('users')
    query_ref = users_ref.where(u'reg', u'==', reg)

    results = list(query_ref.stream())  # Convert to list to handle easily

    if results:
        document = results[0]
        results = document.to_dict()
    else:
        print('No document found with that registration number.')


    return results

def getBalanceFromReg(reg):
    users_ref = db.collection('users')
    query_ref = users_ref.where(u'reg', u'==', reg)

    results = list(query_ref.stream())  # Convert to list to handle easily

    if results:
        document = results[0]
        print('Balance:', document.to_dict()['balance'])

        customer_balance = document.to_dict()['balance']
    else:
        print('No document found with that registration number.')
        customer_balance = -10000

    return customer_balance

def deleteSession(reg):
    users_ref = db.collection('parkingsessions')
    query_ref = users_ref.where(u'reg_plate', u'==', reg)

    try:
        docs = query_ref.get()  # Get matching documents
        for doc in docs:
            doc.reference.delete()
        return True  # Indicate success

    except Exception as e:
        print(f"Error deleting documents: {e}")
        return False  # Indicate failure



def addToDatabase(regPlate, img_path, uid):
    print(regPlate)
    data = {
        'reg_plate': regPlate, #string
        'entryTime': time_now, #dateTime
        'exitTime': '', #dateTime
        'paid': False, #boolean
        'image': img_path,
        'userID': uid
    }

    collection_ref = db.collection('parkingsessions')
    doc_ref = collection_ref.document()  # Use auto-generated ID
    doc_ref.set(data)

def createHistory(regPlate, img_path, uid, entryTime, exitTime, cost):
    print(regPlate)
    data = {
        'reg_plate': regPlate, #string
        'entryTime': entryTime, #dateTime
        'exitTime': exitTime, #dateTime
        'paid': True, #boolean
        'image': img_path,
        'userID': uid,
        'cost': cost
    }

    collection_ref = db.collection('historicalsessions')
    doc_ref = collection_ref.document()  # Use auto-generated ID
    doc_ref.set(data)

def updateExitTime(regPlate):
    collection_ref = db.collection(u'parkingsessions')
    query_ref = collection_ref.where(u'reg_plate', u'==', regPlate)
    results = query_ref.stream()

    if results:
        for doc in results:
            doc_ref = collection_ref.document(doc.id)
            # Update the 'exitTime' field
            doc_ref.update({
                u'exitTime': time_now
            })
            print(f'Updated document {doc.id} with exit time {time_now}')
    else:
        print('No documents found with that registration plate.')

def updateCustomerBalance(regPlate, new_balance):
    collection_ref = db.collection(u'users')
    query_ref = collection_ref.where(u'reg', u'==', regPlate)
    results = query_ref.stream()

    if results:
        for doc in results:
            doc_ref = collection_ref.document(doc.id)
            # Update the 'exitTime' field
            doc_ref.update({
                u'balance': new_balance
            })
            print("200")
    else:
        print('No documents found with that registration plate.')

def calculateCost(entryTime, exitTime):
    # Calculate the total duration in minutes
    duration = (exitTime - entryTime).total_seconds() / 60

    # Calculate the number of 30-minute intervals
    # We use ceil to charge for any fraction of a 30-minute interval
    num_intervals = (duration + 29) // 30  # Adding 29 minutes to round up to the next interval

    # Cost is $0.50 per 30-minute interval
    cost = num_intervals * 0.50

    return cost

def getExitEntryTimes(reg):

    ref = db.collection('parkingsessions')
    query_ref = ref.where(u'reg_plate', u'==', reg)

    results = list(query_ref.stream())  # Convert to list to handle easily

    if results:
        document = results[0]

        entryTime = document.to_dict()['entryTime']
        exitTime = document.to_dict()['exitTime']
    else:
        print('Details not found .')


    return entryTime, exitTime

def check_payment_status(reg_plate):
    # Reference to the collection where parking sessions are stored
    collection_ref = db.collection(u'parkingsessions')

    query_ref = collection_ref.where(u'reg_plate', u'==', reg_plate)
    results = query_ref.stream()

    # Process the results
    for doc in results:
        # Assuming there is only one document for each registration plate
        print(doc.to_dict()['paid'])
        paid_status = doc.to_dict().get('paid', False)  # Default to False if 'paid' not found
        return paid_status  # Return the status of 'paid'

    return None

def updateCost(regPlate, cost):
    collection_ref = db.collection(u'parkingsessions')
    query_ref = collection_ref.where(u'reg_plate', u'==', regPlate)
    results = query_ref.stream()

    if results:
        for doc in results:
            doc_ref = collection_ref.document(doc.id)
            # Update the 'cost' field
            doc_ref.update({
                u'cost': cost
            })
            print(f'Updated document {doc.id} with cost {cost}')
    else:
        print('No documents found with that registration plate.')

def upload_file(local_file, regPlate):
    bucket = storage.bucket()
    uploadName = f"collected_Plates/{time_now}_{regPlate}jpg"
    print(uploadName)
    blob = bucket.blob(uploadName)
    blob.upload_from_filename(local_file)

    blob.make_public()
    return blob.public_url




if __name__ == "__main__":
    reg = "131D36617"
    upload_file('dcu.jpg', "131D36617")
    #check_payment_status(reg)
    updateCost(reg, 2)
    #entryTime, exitTime = getExitEntryTimes(reg)
    #cost = calculateCost(entryTime, exitTime)
    #print(cost)

    #findCustomerAccount(reg)
    #addToDatabase(reg)
    #updateExitTime(reg)

