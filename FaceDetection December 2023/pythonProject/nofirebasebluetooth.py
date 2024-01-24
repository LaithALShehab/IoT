import cv2
import pickle
import face_recognition
import numpy as np
from firebase_admin import credentials, initialize_app, db, storage
from time import strftime, localtime, time
import os
import serial


# Initialize Firebase
cred = credentials.Certificate("key.json")
initialize_app(cred, {
    'databaseURL': "https://imgid-3de22-default-rtdb.firebaseio.com/",
    'storageBucket': "imgid-3de22.appspot.com"
})

bluetooth_port = 'COM7'  # Replace 'COMX' with your Arduino's COM port
baud_rate = 9600
ser = serial.Serial(bluetooth_port, baud_rate, timeout=1)


# Set frame width and height
frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(1)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()

encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds)
print("Encode File Loaded")

authorized_ref = db.reference('authorized')
unauthorized_ref = db.reference('unauthorized')

delay_started = None
delay_interval = 5  # 5 seconds delay

# Create a directory 'entry' if it doesn't exist
if not os.path.exists('entry'):
    os.makedirs('entry')

# List to keep track of local images
local_images = []

while True:
    success, img = cap.read()

    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    if delay_started is not None and time() - delay_started >= delay_interval:
        delay_started = None  # Reset delay timer

    if delay_started is None:
        entry_added = False  # Flag to track if an entry was added

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            y1, x2, y2, x1 = faceLoc

            # Calculate the coordinates for the center area
            center_x = frameWidth // 2
            center_y = frameHeight // 2
            tolerance_x = 100  # Tolerance for the x-axis
            tolerance_y = 100  # Tolerance for the y-axis

            # Check if the face is within the specified area around the center
            if (center_x - tolerance_x < (x1 + x2) // 2 < center_x + tolerance_x) and \
                    (center_y - tolerance_y < (y1 + y2) // 2 < center_y + tolerance_y):
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)

                # Inside the loop where the face is recognized and identified as authorized
                if matches[matchIndex]:
                    print("Known Face Detected")
                    print(studentIds[matchIndex])

                    ser.write(matchIndex.encode())  # Sending the user's name as serial data to Arduino


                    delay_started = time()

                    break


                else:  # If face is unknown or unauthorized
                    print("Unknown Face Detected")
                    # Sending 'Unauthorized' message to Arduino
                    unauthorized_message = 'Unauthorized'
                    ser.write(unauthorized_message.encode())  # Sending 'Unauthorized' as serial data to Arduino

                    entry_added = True  # Set the flag to indicate an entry was added
                    delay_started = time()
                    break

        if entry_added:
            break  # Exit the loop if an entry was added

    cv2.imshow("Result", img)

    if cv2.getWindowProperty("Result", 0) >= 0:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

# Remove local images after processing
folder_path = "entry"
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"{file_path} is not a file.")
    except OSError as e:
        print(f"Error deleting file: {file_path} - {e}")
