import cv2
import face_recognition
import pickle
import os
import re

def extract_numbers(text):
    pattern = r'\d+'
    matches = re.findall(pattern, text)
    number_string = ''.join(matches)
    return number_string

#Importing the student images and ids
folderPath="images"
imgList=[]
studentids=[]
for path in os.listdir(folderPath):
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentids.append(extract_numbers(path))

def findEncodings(imagesList):
    encodeList=[]
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("Encoding initialised...")
encodeListKnown=findEncodings(imgList)
encodeListKnownWithIds=[encodeListKnown,studentids]
print("Encoding Complete")
