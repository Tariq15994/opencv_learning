import cv2

faceCascade= cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")# this haarcascade is very old but it is fast
img = cv2.imread('tariq.jpg') # load the image
# landImg = cv2.imread('wp.jpg') # load the landimage which has no face
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # BGR to GRAY

faces = faceCascade.detectMultiScale(imgGray,1.24,4)


for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)


cv2.imshow("Result", img)
cv2.waitKey(0)
