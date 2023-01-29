import numpy as np
import math
import cv2 as cv
import glob

def find_distance(obj_height, obj_width, img_height, img_width, focal_length):
        distance1 = (obj_height * focal_length)/img_height
        distance2 = (obj_width * focal_length)/img_width
        distance = (distance1 + distance2)/2
        return distance
def calibrate(aperture):
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
    for p in objp:
        p[0] = 35 * p[0]
        p[1] = 35 * p[1]
        p[2] = 35 * p[2]
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    images = glob.glob('chess*.jpg')
    for fname in images:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (7,6), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners2)
            # Draw and display the corners
            #cv.drawChessboardCorners(img, (7,6), corners2, ret)
            #cv.imshow('img', img)
            #cv.waitKey(500)
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    fov_x, fov_y, focal_len, principal, aspect = cv.calibrationMatrixValues(mtx, (1280, 720), aperture[0], aperture[0])
    return focal_len
    #cv.destroyAllWindows()
