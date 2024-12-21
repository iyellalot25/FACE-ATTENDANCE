import cv2

cap=cv2.VideoCapture(0) #0 for default camera 1 for external camera
cap.set(3,1280)
cap.set(4,720)

imgBackground= cv2.imread('resources/background.png')

while True:
    success, img= cap.read()
    cv2.imshow("Webcam",img)
    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break