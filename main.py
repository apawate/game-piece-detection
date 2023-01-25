import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)
capture = True;

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
    has_yellow = (np.sum(mask_yellow) > (0.1*pix_yellow))
    cv2.imshow('frame',frame)
    if not has_yellow:
        cv2.imshow('mask', mask_blue)
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
            (x, y), (w, h), r = cv2.minAreaRect(c_blue)
            if ((w/h > 2) or (h/w > 2)):
                continue
            if ((w > h) and (w > blue_max)):
                blue_max = w
                blue_index = index
            else:
                if (h > blue_max):
                    blue_max = h
                    blue_index = index
        max_contour = contours_blue[blue_index]
        print(max_contour)
            
        #cv2.imshow('res', res_blue)
    else:
        cv2.imshow('mask',mask_yellow)
        blur_yellow = cv2.GaussianBlur(mask_yellow, (5,5), 0)
        contours_yellow, hierarchy_yellow = cv2.findContours(thresh_yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        #cv2.imshow('res',res_yellow)
    print("% blue", (np.sum(mask_blue)/pix_blue)*100)
    print("% yellow", (np.sum(mask_yellow)/pix_yellow)*100)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

# release the captured frame
cap.release()
