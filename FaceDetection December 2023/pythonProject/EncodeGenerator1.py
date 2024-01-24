import cv2
import face_recognition
import pickle
import os


# Importing  images
folderPath = 'images'
# list files (images) in the images folder
pathList = os.listdir(folderPath)
print(pathList)

imgList = []
studentIds = []

for path in pathList:
    # read image and append it to the img list
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    # remove file extension e.g.(jpg) and add image id to student ids
    studentIds.append(os.path.splitext(path)[0])

    # print ids
    print(os.path.splitext(path)[0])

print(studentIds)


def find_encodings(images_list):
    encode_list = []
    for img in images_list:
        # turn image t0 rgb
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # encode image
        encode = face_recognition.face_encodings(img)[0]
        # append encoding to list
        encode_list.append(encode)

    return encode_list


print("Encoding Started ...")

# call encoding function and save encoding list in encodeListKnown
encodeListKnown = find_encodings(imgList)
# create a list with  two elements: the list of face encodings and
# the list of student IDs. This is done to associate each encoding with its corresponding ID.
encodeListKnownWithIds = [encodeListKnown, studentIds]

print("Encoding Complete")
# open file in write mode
file = open("EncodeFile.p", 'wb')
# save encodeListKnownWithIds list to the file
pickle.dump(encodeListKnownWithIds, file)
file.close()

print("File Saved")
