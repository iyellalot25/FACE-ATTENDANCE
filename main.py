import cv2
import os

cap=cv2.VideoCapture(0) #0 for default camera 1 for external camera
cap.set(3,640)
cap.set(4,480)

imgBackground= cv2.imread('resources/background.png')

#Importing the mode images into a list
folderModePath="resources/modes"
imgModeList=[]
for path in os.listdir(folderModePath):
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))

while True:
    success, img= cap.read()

    imgBackground[162:162+480,55:55+640]= img #for overlay
    imgBackground[44:44+633,808:808+414]= imgModeList[0] #for mode selection

    #cv2.imshow("Webcam",img) #for display webcam feed seperately
    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break