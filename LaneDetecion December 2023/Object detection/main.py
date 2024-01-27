import cv2
# Threshold to detect objects
thres = 0.45
# Open a connection to the webcam (camera index 0)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width of the frame
cap.set(4, 720)   # Set height of the frame
cap.set(10, 70)   # Set brightness
# Load the class names from the file 'coco.names'
classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')
# Load the pre-trained model for object detection
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'
net = cv2.dnn_DetectionModel(weightsPath, configPath)
# Set input parameters for the model
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(False)  # Change to False to avoid color swapping
# Main loop for capturing and processing frames from the webcam
while True:
    # Read a frame from the webcam
    success, img = cap.read()
    # Check if the frame is successfully captured
    if not success or img is None:
        print("Error: Unable to capture an image from the camera.")
        break
    # Detect objects in the frame
    classIds, confs, bbox = net.detect(img, confThreshold=thres)
    print(classIds, bbox)
    # If objects are detected, draw bounding boxes and labels
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
            cv2.putText(img, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    # Display the output frame
    cv2.imshow("Output", img)
    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
