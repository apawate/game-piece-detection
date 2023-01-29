import cv2
import numpy as np
import imutils
import calculations

cap = cv2.VideoCapture(0)
capture = True;
focal = input("Camera focal length(type c to calibrate): ")
if (focal == "c"):
    focal = calculations.calibrate((6.0, 4.8))
    print(focal)
else:
    focal = float(focal)
objh_blue = input("Purple object height: ")
objh_blue = float(objh_blue)
objw_blue = input("Purple object width: ")
objw_blue = float(objw_blue)
objh_yellow = input("Yellow object height: ")
objh_yellow = float(objh_yellow)
objw_yellow = input("Yellow object width: ")
objw_yellow = float(objw_yellow)

while(capture):
    _, frame = cap.read()
    while (frame is None):
        _, frame = cap.read()
    # Converts images from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([130,50,50])
    upper_blue = np.array([160,255,255])
    lower_yellow = np.array([25, 100, 100])
    upper_yellow = np.array([35, 255, 255])

    # Creates a mask showing all "blue" objects and one showing all "yellow" objects in the frame
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    #res_blue = cv2.bitwise_and(frame,frame, mask= mask_blue)
    #res_yellow = cv2.bitwise_and(frame, frame, mask= mask_yellow)
    pix_blue =  255 * mask_blue.shape[0] * mask_blue.shape[1]
    pix_yellow = 255 * mask_yellow.shape[0] * mask_yellow.shape[1]
    has_blue = (np.sum(mask_blue) > (0.01*pix_blue))
    has_yellow = (np.sum(mask_yellow) > (0.05*pix_yellow))
    cv2.imshow('frame',frame)
    if not has_yellow:
        blur = cv2.GaussianBlur(mask_blue, (5,5), 0)
    else:
        blur = cv2.GaussianBlur(mask_yellow, (5,5), 0)
    blur = cv2.Canny(blur, 50, 100)
    blur = cv2.dilate(blur, None, iterations=1)
    blur = cv2.erode(blur, None, iterations=1)
    contours = cv2.findContours(blur.copy(), cv2.RETR_EXTERNAL,
cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    max=0
    final_index=-1
    index = -1;
    if not has_yellow:
        ratio = objw_blue/objh_blue
    else:
        ratio = objw_yellow/objh_yellow
    for c in contours:
        index = index + 1
        if cv2.contourArea(c) < 100:
            continue
        x,y,w,h = cv2.boundingRect(c)
        if ((w/h > (1.5*ratio)) or (h/w > (1.5/ratio))):
            continue
        if ((w > h) and (w > max)):
            max = w
            final_index = index
        else:
            if (h > max):
                max = h
                final_index = index
    if ((final_index < len(contours)) and (final_index > 0)):
        max_contour = contours[final_index]
    elif (len(contours) > 0):
        max_contour = contours[0]
    else:
        max_contour = [np.array([[1,1],[10,50],[50,50]], dtype=np.int32) , np.array([[99,99],[99,60],[60,99]], dtype=np.int32)][0];
    x,y,w,h = cv2.boundingRect(max_contour)
    print("Width", w, "Height", h)
    if not has_yellow:
        print("Distance", calculations.find_distance(objh_blue, objw_blue, h, w, focal))
        cv2.rectangle(mask_blue, (x,y),(x+w,y+h),(255,255,255),2)
        cv2.imshow('mask', mask_blue)
    else:
        print("Distance", calculations.find_distance(objh_yellow, objw_yellow, h, w, focal))
        cv2.rectangle(mask_yellow, (x,y),(x+w,y+h),(255,255,255),2)
        cv2.imshow('mask', mask_yellow)    
    #cv2.imshow('res', res_blue)
    print("% blue", (np.sum(mask_blue)/pix_blue)*100)
    print("% yellow", (np.sum(mask_yellow)/pix_yellow)*100)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

# release the captured frame
cap.release()
