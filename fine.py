# importing all the required Library
import cv2
import numpy as np
import face_recognition
import os
import requests
import json
from twilio.rest import Client
import info
from datetime import datetime

num = []
# Storing all the images
path = 'images'
images = []
# Storing all the names here
personName = []
myList = os.listdir(path)

# Reading the images using cv2 Model
for cu_img in myList:
    current_Img = cv2.imread(f'{path}/{cu_img}')
    images.append(current_Img)
    personName.append(os.path.splitext(cu_img)[0])



def faceEncodings(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list


encodeListKnown = faceEncodings(images)
print("Encodings are done")


def report(name):
    with open('RecordsOfPeople.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            time_now = datetime.now()
            tStr = time_now.strftime('%H:%M:%S')
            dStr = time_now.strftime('%d/%m/%Y')
            f.writelines(f'{name}, {tStr}, {dStr}\n')


# reading the camera
camera_port = 0
cap = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

    faceCurrent = face_recognition.face_locations(faces)
    encodesCurrentFrame = face_recognition.face_encodings(faces, faceCurrent)

    for encodeFace, faceLoc in zip(encodesCurrentFrame, faceCurrent):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = personName[matchIndex].upper()

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            for i in info.targe_no:
                 if i['Name '] == personName[matchIndex] :
                    num.append(i['Mobile No.'])
            report(name)

    cv2.imshow("Camera", frame)

    k = cv2.waitKey(10)
    if k == 27:
        break

url = 'https://7sj1hjl2qh.execute-api.us-east-1.amazonaws.com/test/attendance'
body = {

    "password": "hello",
    "name": "Marteena"
}
response = requests.post(url, data = json.dumps(body))

print(response.text)


cap.release()
cv2.destroyAllWindows()