import cv2
import sqlite3
import os
import pickle
import face_recognition
import numpy as np
import cvzone
from datetime import datetime
import time


# Connect to SQLite database
conn = sqlite3.connect('database/students.db')
cursor = conn.cursor()

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

def mark_attendance(student_id):
    current_time = datetime.now()
    cursor.execute("SELECT total_attendance, last_attendance_time FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    if student:
        total_attendance, last_attendance_time_str = student
        last_attendance_time = datetime.strptime(last_attendance_time_str, '%Y-%m-%d %H:%M:%S')
        
        if (current_time - last_attendance_time).total_seconds() >= 3:
            total_attendance += 1
            cursor.execute("UPDATE students SET total_attendance = ?, last_attendance_time = ? WHERE id = ?",
                        (total_attendance, current_time.strftime('%Y-%m-%d %H:%M:%S'), student_id))
            conn.commit()
            print(f"Attendance marked for student ID {student_id}. Total attendance: {total_attendance}")
            return True
        else:
            print("Attendance prevented: Last attendance was less than 30 seconds ago.")
            return False
    else:
        print("Student not found.")
        return False

def fetch_student_data(student_id):
    conn = sqlite3.connect('database/students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student_data = cursor.fetchone()
    conn.close()
    
    if student_data:
        human_readable_data = []
        for item in student_data:
            if isinstance(item, bytes):
                try:
                    # Attempt to decode as UTF-8
                    human_readable_data.append(item.decode('utf-8'))
                except UnicodeDecodeError:
                    # If decoding fails, handle it as binary or skip
                    human_readable_data.append(f"Binary data (length: {len(item)})")
            else:
                human_readable_data.append(item)
        return human_readable_data
    else:
        return None

def fetch_image(student_id):
    image_path = f'images/{student_id}.jpg'  # Assuming images are stored as '123.jpg', '456.jpg', etc.
    
    if os.path.exists(image_path):
        img = cv2.imread(image_path)
        return img
    else:
        print(f"Image for student ID {student_id} not found.")
        return None


counter=0
modeType=0
id=-1
imgStudent=[]

while True:
    success, img= cap.read()

    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame=face_recognition.face_locations(imgS)
    encodeCurFrame=face_recognition.face_encodings(imgS,faceCurFrame)

    imgBackground[162:162+480,55:55+640]= img #for overlay
    imgBackground[44:44+633,808:808+414]= imgModeList[modeType] #for mode selection
    
    if faceCurFrame:
        for encoFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encoFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encoFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                id = studentids[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                #result = mark_attendance(id)
                if counter==0:
                    counter=1
                    modeType=1
        if counter!=0:
            if counter==1:
                #Fetch data from face
                studentInfo=fetch_student_data(id)
                print(studentInfo)  
                #Fetch image from storage(local) later implement from db
                imgStudent=fetch_image(id)
                imgStudent = cv2.resize(imgStudent, (260, 216))
                #Update db
                if studentInfo:
                    new_attendance = studentInfo[4] + 1
                    cursor.execute("UPDATE students SET total_attendance = ? WHERE id = ?", (new_attendance, id))
                    conn.commit()
                    print(f"Attendance updated for ID {id}. Total attendance: {new_attendance}")
                    studentInfo = fetch_student_data(id) #Refreshing

                
        if counter<=10:
            cv2.putText(imgBackground,str(studentInfo[4]),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
            cv2.putText(imgBackground,str(studentInfo[2]),(1006,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
            cv2.putText(imgBackground,str(studentInfo[0]),(1006,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
            cv2.putText(imgBackground,str(studentInfo[5]),(910,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
            cv2.putText(imgBackground,str(studentInfo[6]),(1025,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
            cv2.putText(imgBackground,str(studentInfo[3]),(1125,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)

            (w,h),_=cv2.getTextSize(studentInfo[1],cv2.FONT_HERSHEY_COMPLEX,1,1) #1 corresponds to name in database
            offset=(414-w)//2
            cv2.putText(imgBackground,str(studentInfo[1]),(808+offset,445),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)

            imgBackground[175:175+216,909:909+260]=imgStudent
        counter+=1


    #cv2.imshow("Webcam",img) #for display webcam feed seperately
    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break