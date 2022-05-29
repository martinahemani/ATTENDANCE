import cv2
import numpy as np
import face_recognition
import os
from twilio.rest import Client
import info
from datetime import datetime
num = []
path = 'images'
images = []
personName = []
myList = os.listdir(path)
# print(myList)

for cu_img in myList:
    current_Img = cv2.imread(f'{path}/{cu_img}')
    images.append(current_Img)
    personName.append(os.path.splitext(cu_img)[0])
    # print(personName)


def faceEncodings(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list


encodeListKnown = faceEncodings(images)
print(" Encodings Done")


def attendance(name):
    with open('RecordFile.csv', 'r+') as f:
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
            attendance(name)

    cv2.imshow("Camera", frame)

    k = cv2.waitKey(10)
    if k == 27:
        break

client = Client(info.account_sid, info.auth_token)
message = client.messages \
    .create(
    body="You are entering to our locker room, if it isn't you then call on Bank's Helpline nummber 988684",
    from_=info.twilio_no,
    to= '+91'+str(num[0])

)

print(message.body)

cap.release()
cv2.destroyAllWindows()