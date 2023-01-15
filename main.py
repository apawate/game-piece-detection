import cv2
import numpy as np

cap = cv2.VideoCapture(0)
capture = true;

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
	res_blue = cv2.bitwise_and(frame,frame, mask= mask_blue)
	res_yellow = cv2.bitwise_and(frame, frame, mask= mask_yellow)
	cv2.imshow('frame',frame)
	cv2.imshow('mask',mask_yellow)
	cv2.imshow('res',res_yellow)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()

# release the captured frame
cap.release()
