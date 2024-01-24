import cv2
import pickle
import face_recognition
import numpy as np
from firebase_admin import credentials, initialize_app, db, storage
from time import strftime, localtime, time
import os
import serial
import sys


# Set frame width and height
frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(1)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

# Bluetooth initialization
bluetooth_port = 'COM7'  # Replace 'COMX' with your Arduino's COM port
baud_rate = 9600
ser = serial.Serial(bluetooth_port, baud_rate, timeout=1)

# Check if the Bluetooth connection is open
if not ser.isOpen():
    print("Bluetooth connection not open. Exiting.")
    ser.close()
    sys.exit()

print("Bluetooth connection open.")

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

                    id = studentIds[matchIndex]
                    studentInfo = db.reference(f'IDP/{id}').get()
                    print(studentInfo)

                    name = studentInfo['name']

                    current_time = localtime(time())  # Get current local time
                    formatted_time = strftime("%d/%m/%Y/%H:%M", current_time)  # Format timestamp to dd/mm/yyyy/h/m

                    entry_data = {
                        'name': name,
                        'time_entered': formatted_time,
                    }

                    # Save the image locally in the 'entry' folder
                    current_time_str = strftime("%d%m%Y%H%M%S", current_time)
                    image_filename = f'entry/authorized_entry_{current_time_str}.jpg'
                    cv2.imwrite(image_filename, img)
                    local_images.append(image_filename)

                    # Save the image to Firebase Storage and get its URL
                    image_blob = storage.bucket().blob(image_filename)
                    image_blob.upload_from_filename(image_filename)
                    image_blob.make_public()  # Make the image publicly accessible
                    image_url = image_blob.public_url

                    entry_data['image'] = image_url

                    # Remove local image file after uploading to Firebase Storage
                    os.remove(image_filename)

                    # Push all data in a single node
                    authorized_ref.push().set(entry_data)

                    # Sending the user's name to Arduino
                    ser.write(name.encode())  # Sending the user's name as serial data to Arduino

                    entry_added = True  # Set the flag to indicate an entry was added
                    delay_started = time()

                    break

                else:  # If face is unknown or unauthorized
                    print("Unknown Face Detected")

                    current_time = localtime(time())
                    formatted_time = strftime("%d/%m/%Y/%H:%M", current_time)

                    unauthorized_entry = {
                        'time_tried_entering': formatted_time,
                    }

                    # Save the image of unauthorized person locally in the 'entry' folder
                    current_time_str = strftime("%d%m%Y%H%M%S", current_time)
                    image_filename = f'entry/unauthorized_entry_{current_time_str}.jpg'
                    cv2.imwrite(image_filename, img)
                    local_images.append(image_filename)

                    # Save the image to Firebase Storage and get its URL
                    image_blob = storage.bucket().blob(image_filename)
                    image_blob.upload_from_filename(image_filename)
                    image_blob.make_public()  # Make the image publicly accessible
                    image_url = image_blob.public_url

                    unauthorized_entry['image'] = image_url
                    unauthorized_ref.push().set(unauthorized_entry)

                    # Sending 'Unauthorized' message to Arduino
                    unauthorized_message = 'Unauthorized'
                    ser.write(unauthorized_message.encode())  # Sending 'Unauthorized' as serial data to Arduino

                    entry_added = True  # Set the flag to indicate an entry was added
                    delay_started = time()

                    # break  # Remove break statement to keep processing frames after detecting an unknown face

        # Remove the following line to keep processing frames after detecting an unknown face
        # if entry_added:
        #     break  # Exit the loop if an entry was added

    cv2.imshow("Result", img)

    if cv2.getWindowProperty("Result", 0) >= 0:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()


# Close the Bluetooth connection
ser.close()
