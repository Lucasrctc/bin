#Based on phone.py
from PIL import Image
from subprocess import call
import time
import cv2
import numpy as np
import pytesseract
from imutils import contours

# Returns a function which gets the rgba colour at the x, y pixel on the phone screen
def ColourFunction(width, height):
    def GetColorAtPixel (x, y) :
        call(["rm", "screen.dump"])
        with open("screen.dump", "w") as outfile:
            call(["adb", "shell", "screencap"], stdout=outfile)
        with open("screen.dump", "rb") as infile:
            byte = infile.read()[12:]
        pixel = (width * y + x) * 4
        return byte[pixel], byte[pixel + 1], byte[pixel+2], byte[pixel+3]
    
    return GetColorAtPixel

def tap(x, y):
    call(["adb", "shell", "input", "tap", str(x), str(y)])
    time.sleep(.1)

def screenshot(img):
    with open(img, "w") as outfile:
        cmd = "adb shell screencap -p /sdcard/screen.png"
        cmd = cmd.split()
        print(cmd)
        call(cmd)
        cmd = "adb pull /sdcard/screen.png screen.png"
        cmd = cmd.split()
        print(cmd)
        call(cmd)
        cmd = "convert screen.png screen.jpg"
        cmd = cmd.split()
        print(cmd)
        call(cmd)

def CropImage(img, l, t, r, b, debug = True):
    # Opens a image in RGB mode
    im = Image.open(img)
    
    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    print(im.size)
    print((l, t, r, b))
    
    # Setting the points for cropped image
    
    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im.crop((l, t, r, b))
    
    # Shows the image in image viewer
    if debug:
        im1.show()
        cv2.waitKey(0)

    return im1

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

def contourImage(image):
    image = cv2.imread(image)
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

