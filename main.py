import cv2
import os
import pickle
import face_recognition
import numpy as np

cap=cv2.VideoCapture(0) #0 for default camera 1 for external camera
cap.set(3,640)
cap.set(4,480)

imgBackground= cv2.imread('resources/background.png')

#Importing the mode images into a list
folderModePath="resources/modes"
imgModeList=[]
for path in os.listdir(folderModePath):
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))

#Loading the encoding file
print("Loading Encode File...")
with open('EncodeFile.p','rb') as file:
    encodeListKnownWithIds= pickle.load(file)
    encodeListKnown,studentids=encodeListKnownWithIds
print("Encode file loaded...")

while True:
    success, img= cap.read()

    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame=face_recognition.face_locations(imgS)
    encodeCurFrame=face_recognition.face_encodings(imgS,faceCurFrame)

    imgBackground[162:162+480,55:55+640]= img #for overlay
    imgBackground[44:44+633,808:808+414]= imgModeList[0] #for mode selection

    for encoFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encoFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encoFace)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = studentids[matchIndex].upper()
            print(name)

    #cv2.imshow("Webcam",img) #for display webcam feed seperately
    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break