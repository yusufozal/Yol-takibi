import cv2
import numpy as np
import math


# finMaxCounter yol üzerinde bulunan tüm köşeleri söyler
def findMaxContour(contours):
    max_i = 0
    max_area = 0
    for i in range(len(contours)):
        area_line = cv2.contourArea(contours[i])

        if max_area < area_line:
            max_area = area_line
            max_i = i
        try:
            c = contours[max_i]
        except:
            contours = [0]
            c = contours[0]
        return c

# köşe fonksiyonu yolda köşe sayısna göre yolu
def köşe(contours,frame):
    for cnt in contours:
        area = cv2.contourArea(cnt)

        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if len(approx) == 4:
            return "straight",approx

        elif len(approx)==6:
            return "L line",approx

        elif len(approx)==8:
            return "T line",approx

        else:
            return "dont line",approx




