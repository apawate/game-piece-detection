import numpy as np
import math
import cv2

def find_distance(obj_height, obj_width, img_height, img_width, focal_length):
        distance1 = (obj_height * focal_length)/img_height
        distance2 = (obj_width * focal_length)/img_width
        distance = (distance1 + distance2)/2
        return distance
