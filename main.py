import cv2
import numpy as np
import imutils
import calculations

cap = cv2.VideoCapture(0)
capture = True;
focal = input("Camera focal length: ")
focal = float(focal)
objh_blue = input("Blue object height: ")
objh_blue = float(objh_blue)
objw_blue = input("Blue object width: ")
objw_blue = float(objw_blue)
objh_yellow = input("Yellow object height: ")
objh_yellow = float(objh_yellow)
objw_yellow = input("Yellow object width: ")
objw_yellow = float(objw_yellow)
_, frame = cap.read()
cv2.imwrite('a.jpg', frame)

while(capture):
    _, frame = cap.read()
    # Converts images from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

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
        blur_blue = cv2.GaussianBlur(mask_blue, (5,5), 0)
        blur_blue = cv2.Canny(blur_blue, 50, 100)
        blur_blue = cv2.dilate(blur_blue, None, iterations=1)
        blur_blue = cv2.erode(blur_blue, None, iterations=1)
        contours_blue = cv2.findContours(blur_blue.copy(), cv2.RETR_EXTERNAL,
cv2.CHAIN_APPROX_SIMPLE)
        contours_blue = imutils.grab_contours(contours_blue)
        blue_max=0
        blue_index=-1
        index = -1;
        for c_blue in contours_blue:
            index = index + 1
            if cv2.contourArea(c_blue) < 100:
                continue
            x,y,w,h = cv2.boundingRect(c_blue)
            if ((w/h > (1.5*objw_yellow/objh_yellow)) or (h/w > (1.5*objh_yellow/objw_yellow))):
                continue
            if ((w > h) and (w > blue_max)):
                blue_max = w
                blue_index = index
            else:
                if (h > blue_max):
                    blue_max = h
                    blue_index = index
        max_contour = contours_blue[blue_index]
        x,y,w,h = cv2.boundingRect(max_contour)
        print("Width", w, "Height", h)
        print("Distance", calculations.find_distance(objh_blue, objw_blue, h, w, focal))
        cv2.rectangle(mask_blue, (x,y),(x+w,y+h),(255,255,255),2)
        cv2.imshow('mask', mask_blue)    
        #cv2.imshow('res', res_blue)
    else:
        blur_yellow = cv2.GaussianBlur(mask_yellow, (5,5), 0)
        blur_yellow = cv2.Canny(blur_blue, 50, 100)
        blur_yellow = cv2.dilate(blur_blue, None, iterations=1)
        blur_yellow = cv2.erode(blur_blue, None, iterations=1)
        contours_yellow = cv2.findContours(blur_yellow.copy(), cv2.RETR_EXTERNAL,
cv2.CHAIN_APPROX_SIMPLE)
        contours_yellow = imutils.grab_contours(contours_yellow)
        yellow_max=0
        yellow_index=0
        index = 0;
        for c_yellow in contours_yellow:
            index = index + 1
            if cv2.contourArea(c_yellow) < 100:
                continue
            x,y,w,h = cv2.boundingRect(c_yellow)
            if ((w/h > (1.5*objw_yellow/objh_yellow)) or (h/w > (1.5*objh_yellow/objw_yellow))):
                continue
            if ((w > h) and (w > yellow_max)):
                yellow_max = w
                yellow_index = index
            else:
                if (h > yellow_max):
                    yellow_max = h
                    yellow_index = index
        max_contour = contours_yellow[yellow_index]
        x,y,w,h = cv2.boundingRect(max_contour)
        print("Width", w, "Height", h)
        print("Distance", calculations.find_distance(objh_yellow, objw_yellow, h, w, focal))
        cv2.rectangle(mask_yellow, (x,y),(x+w,y+h),(255,255,255),2)
        cv2.imshow('mask', mask_yellow)
        #cv2.imshow('res',res_yellow)
    print("% blue", (np.sum(mask_blue)/pix_blue)*100)
    print("% yellow", (np.sum(mask_yellow)/pix_yellow)*100)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

# release the captured frame
cap.release()
