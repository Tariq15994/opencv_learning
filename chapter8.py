import cv2
import numpy as np

def stackImages(scale,imgArray): # for Stacking Images
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img):
    # first find contours using cv2.findContours
    contours , hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt) # find area for Threeshold value
        if area>500:
            cv2.drawContours(imgContour,cnt,-1,(0,255,0),2) # Draw contour on img
            peri = cv2.arcLength(cnt,True) # find length of contour
            approx = cv2.approxPolyDP(cnt,0.02*peri,True) # find the corner values of contour
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx) # find boundingbox points
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(255,0,0),2) # draw bounding box
            if objCor ==3:
                # if object has 3 corner means it is Triangle
                objectType = "Triangle"
            elif objCor ==4:
                # if object has 4 corner and its height and width are same means it is Square
                aspRatio = w/float(h)
                if aspRatio >0.95 and aspRatio <1.05: # aspRatio with 5% deviation
                    objectType = "Square"
                else:   #otherwise it is Rectangle
                    objectType = "Rectangle"

            elif objCor>4:     # if object has  corner means it is Circle
                objectType = "Circle"

            cv2.putText(imgContour, objectType,
                        (x+(w//2)-20,y+(h//2)-10),
                        cv2.FONT_HERSHEY_DUPLEX,0.5,(0,0,0),2)
path = 'shapes.png'
img = cv2.imread(path)
imgContour = img.copy()

imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
imgCanny = cv2.Canny(imgBlur,50,50)
getContours(imgCanny)
imgBlank = np.zeros_like(img)

imgStack = stackImages(0.8,([img,imgGray,imgBlur],
                            [imgCanny,imgContour,imgBlank]))

cv2.imshow("Stack", imgStack)
cv2.waitKey(0)