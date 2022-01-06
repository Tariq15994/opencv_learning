import cv2
# for camera
cap = cv2.VideoCapture(0)
cap.set(3,4000)
cap.set(4,4800)
cap.set(11,100)
while True:
    success, img = cap.read()
    cv2.imshow("Cam", img)
    if cv2.waitKey(1)& 0xFF ==ord('q'):
        break


