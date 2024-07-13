# Based on phone.py
from PIL import Image
from subprocess import call
from subprocess import check_output as co
from phoneLib import *
import time
import sys
import os

# Image processing libs
import cv2
import numpy as np
import pytesseract
from imutils import contours

os.chdir("./aux_images")
# Load image, grayscale, Gaussian blur, Canny edge detection
image = cv2.imread("screen.png")

def contourImage(image)
    original = image.copy()
    
    # Cvt to hsv
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
    # Get binary-mask
    sensitivity = 15
    msk = cv2.inRange(hsv, np.array([0, 0, 255 - sensitivity]), np.array([255, sensitivity, 255]))
    krn = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    dlt = cv2.dilate(msk, krn, iterations=1)
    thr = 255 - cv2.bitwise_and(dlt, msk)
    #cv2.imshow("Changed image", thr)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows() 
    blurred = cv2.GaussianBlur(thr, (3,3), 0)
    canny = cv2.Canny(blurred, 120, 255, 1)
    
    ret = []

    # Find contours and extract ROI
    ROI_number = 0
    cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts, _ = contours.sort_contours(cnts, method="left-to-right")
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        ROI = original[y:y+h, x:x+w]
        cv2.rectangle(image, (x,y), (x+w,y+h),(36, 255, 12), 3)
        ret.append((x, y, x+w, y+h))
        ROI_number += 1
    
    print('Contours Detected: {}'.format(ROI_number))
    cv2.imshow("image", image)
    cv2.waitKey()
    cv2.imshow("canny", canny)
    cv2.waitKey()
    cv2.destroyAllWindows() 
    return ret

def img2text(imagefile, debug = False):
    # Load the img
    img = cv2.imread(imagefile)
    
    # Cvt to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Get binary-mask
    sensitivity = 15
    msk = cv2.inRange(hsv, np.array([0, 0, 255 - sensitivity]), np.array([255, sensitivity, 255]))
    krn = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    dlt = cv2.dilate(msk, krn, iterations=1)
    thr = 255 - cv2.bitwise_and(dlt, msk)
    
    if debug:
        cv2.imshow("Changed image", thr)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
    
    # OCR
    d = pytesseract.image_to_string(thr, config="--psm 10")
    return d

call(["adb","shell","settings","put","system","pointer_location","0"])

if __name__== "__main__":
    print("Test")
        #tap(*x)
