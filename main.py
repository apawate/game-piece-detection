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

    # Creates a mask showing all "blue" images in the frame
	mask = cv2.inRange(hsv, lower_blue, upper_blue)
	res = cv2.bitwise_and(frame,frame, mask= mask)
	cv2.imshow('frame',frame)
	cv2.imshow('mask',mask)
	cv2.imshow('res',res)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()

# release the captured frame
cap.release()
