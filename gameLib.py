from PIL import Image
from subprocess import call
from subprocess import check_output
import sys
import time
import cv2
import numpy as np
import pytesseract
from imutils import contours

# Returns the rgba colour at the x, y pixel on the screen
def GetColourAtPixel (x, y):
    with Image.open("screen.png", "r") as infile:
        width, height = infile.size
        pixel_values = list(infile.getdata())
        pixel = pixel_values[width * y + x]
    return pixel

def WindowCoords():
    idleonID = 1476970
    cmd = "xwininfo  -name  Legends Of Idleon".split("  ")
    winfo = co(cmd)
    winfo = winfo[winfo.find("Absolute upper-left X:"):]
    winfo = winfo[winfo.find(":") + 1:]
    x = int(winfo[:winfo.find("\n")])
    winfo = winfo[winfo.find("Absolute upper-left Y:"):]
    winfo = winfo[winfo.find(":") + 1:]
    y = int(winfo[:winfo.find("\n")])
    winfo = winfo[winfo.find("Width:"):]
    winfo = winfo[winfo.find(":") + 1:]
    w = int(winfo[:winfo.find("\n")])
    winfo = winfo[winfo.find("Height:"):]
    winfo = winfo[winfo.find(":") + 1:]
    h = int(winfo[:winfo.find("\n")])
    return x, y, w, h
    #cmd = ("import -window " + str(winfo) +" screen.png").split()
    #call(cmd)

def abs2scr(absx, absy):
    wx, wy, ww, wh = WindowCoords()
    return absx - wx, absy - wy

def abs2rel(absx, absy):
    wx, wy, ww, wh = WindowCoords()
    return 1000 * (absx - wx) // ww, 1000 * (absy - wy) // wh

def rel2abs(relx, rely):
    wx, wy, ww, wh = WindowCoords()
    return relx * ww // 1000 + wx, rely * wh // 1000 + wy

def rel2scr(relx, rely):
    wx, wy, ww, wh = WindowCoords()
    return relx * ww // 1000, rely * wh // 1000

def scr2rel(scrx, scry):
    wx, wy, ww, wh = WindowCoords()
    return 1000 * (scrx) // ww, 1000 * (scry) // wh

def scr2abs(scrx, scry):
    wx, wy, ww, wh = WindowCoords()
    return scrx + wx, scry + wy

def co(s):
    return check_output(s).decode(sys.stdout.encoding)

def swipe(x, y, x2, y2):
    call(["xdotool", "mousemove", str(x), str(y), "mousedown", "1", "mousemove", str(x2), str(y2), "mousemove", "restore"])
    time.sleep(.1)

def tap(x, y):
    call(["xdotool", "mousemove", str(x), str(y), "click", "1", "mousemove", "restore"])
    time.sleep(.1)

def mousemove(x, y):
    call(["xdotool", "mousemove", str(x), str(y)])
    time.sleep(.1)

def Screenshot():
    call(["rm", "screen.png"])
    idleonID = 1476970
    cmd = "xwininfo  -name  Legends Of Idleon".split("  ")
    wid = co(cmd)
    wid = wid[wid.find("0x"):]
    wid = wid[:wid.find(" ")]
    cmd = ("import -window " + str(wid) +" screen.png").split()
    call(cmd)

def CropImage(img, l, t, r, b, debug = True):
    # Opens a image in RGB mode
    im = Image.open(img)
    
    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    
    # Setting the points for cropped image
    
    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im.crop((l, t, r, b))
    
    # Shows the image in image viewer
    if debug:
        im1.show()

    im1.save("crop.png", "PNG")
    return im1

def img2text(imagefile, debug = False):
    # Load the img
    img = cv2.imread(imagefile)
    
    # Cvt to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Get binary-mask
    sensitivity = 50
    msk = cv2.inRange(hsv, np.array([0, 0, 255 - sensitivity]), np.array([255, sensitivity, 255]))
    krn = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    dlt = cv2.dilate(msk, krn, iterations=1)
    thr = 255 - cv2.bitwise_and(dlt, msk)
    
    if debug:
        cv2.imshow("Changed image", thr)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
    
    # OCR
    d = pytesseract.image_to_string(thr, config="-c tessedit_char_whitelist=0123456789 --psm 10")
    return d

def contourBWImage(image):
    image = cv2.imread(image)
    original = image.copy()
    
    # Cvt to hsv
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
    # Get binary-mask
    sensitivity = 50
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
    try:
        cnts, _ = contours.sort_contours(cnts, method="left-to-right")
    except:
        cnts = []
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        ROI = original[y:y+h, x:x+w]
        cv2.rectangle(image, (x,y), (x+w,y+h),(36, 255, 12), 1)
        ret.append((x, y, x+w, y+h))
        ROI_number += 1
    
    print('Contours Detected: {}'.format(ROI_number))
    cv2.imshow("image", image)
    cv2.waitKey()
    cv2.imshow("canny", canny)
    cv2.waitKey()
    cv2.destroyAllWindows() 
    return ret

def contourImage(image):
    image = cv2.imread(image)
    original = image.copy()
    
    blurred = cv2.GaussianBlur(image, (3,3), 0)
    canny = cv2.Canny(blurred, 100, 175, 1)
    
    ret = []

    # Find contours and extract ROI
    ROI_number = 0
    cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    try:
        cnts, _ = contours.sort_contours(cnts, method="left-to-right")
    except:
        cnts = []
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

