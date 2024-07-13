# Based on phone.py
from subprocess import check_output as co
from phoneLib import *
import sys
import os

os.chdir("aux_images")

# Get phone screen dimensions
#widthheight = co(["adb", "shell", "wm", "size"]).decode(sys.stdout.encoding)
#widthheight = widthheight[widthheight.rfind(" ") + 1:-1]
#width = int(widthheight[:widthheight.find("x")])
#height = int(widthheight[widthheight.find("x") + 1:])

# Make colour function
#GetColorAtPixel = ColourFunction(width, height)
#260, 200
#450, 560
coords = {  
            "Inventory" : [(a, b) for b in [200 + (560 - 200)*j/4 for j in range(5)] for a in [260 + (450 - 260) * i/2 for i in range(3)]],
            "InvBox": (218, 155, 485, 610)
        }

# Crop screenshots
def cropActiveCogs(img, debug = False):
    # Get a screenshot
    screenshot(img)
    #300, 235
    sep = 14
    l, t, r, b = 590, 150, 1700, 900
    print((l, t, r, b))
    rows = 5
    cols = 3
    boxdim = (r - l - (cols - 1) * sep)/cols
    im = CropImage(img, l, t, r, b, False)
    if debug:
        im.show()
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
    im.save("test.png", "PNG")

def cropActiveCogNumbers(img, debug = True):
    # Get a screenshot
    screenshot(img)
    #300, 235
    l, t, r, b = 608, 209, 1692, 884
    print((l, t, r, b))
    rows = 8
    cols = 12
    boxdim = (r - l)/cols
    for row in range(rows):
        for col in range(cols):
            im = CropImage(img, l + col * boxdim, t + row * boxdim, l + (col + 1) * boxdim - 12, t + (row + 1) * boxdim, False)
            im.save(str(row) + "_" + str(col) + "_" + "activeCog.png", "PNG")
        if debug:
            im.show()
            cv2.waitKey(0)
            cv2.destroyAllWindows() 

def cropCogs(img):
    # Get a screenshot
    screenshot(img)
    #300, 235
    sep = 14
    l, t, r, b = coords["InvBox"]
    print((l, t, r, b))
    rows = 5
    cols = 3
    boxdim = (r - l - (cols - 1) * sep)/cols
    print(boxdim - ((b - t - (rows - 1) * sep)/rows))
    for row in range(rows):
        for col in range(cols):
            im = CropImage(img, l + col * (sep + boxdim), t + row * (sep + boxdim), l + col * (sep + boxdim) + boxdim , t + row * (sep + boxdim) + boxdim, False)
            im.save(str(row) + "_" + str(col) + "_" + "cog.png", "PNG")

def cropCogNumbers(img):
    # Get a screenshot
    screenshot(img)
    #300, 235
    sep = 14
    l, t, r, b = coords["InvBox"]
    print((l, t, r, b))
    rows = 5
    cols = 3
    boxdim = (r - l - (cols - 1) * sep)/cols
    print(boxdim - ((b - t - (rows - 1) * sep)/rows))
    for row in range(rows):
        for col in range(cols):
            left = l + col * (sep + boxdim)
            top = t + row * (sep + boxdim) + 2*boxdim/3
            #20 to remove the %
            right = l + col * (sep + boxdim) + boxdim - 20
            bottom = t + row * (sep + boxdim) + boxdim
            im = CropImage(img, left, top, right, bottom, False)
            im.save(str(row) + "_" + str(col) + "_" + "cog.png", "PNG")

#call(["adb","shell","settings","put","system","pointer_location","0"])

#cropActiveCogs("screen.jpg")

#cropActiveCogNumbers("screen.jpg")
def getActiveCogCoords(image):
    contours = contourImage(image)

    llist = sorted(set([x[0] for x in contours]))
    tlist = sorted(set([x[1] for x in contours]))
    rlist = sorted(set([x[2] for x in contours]))
    blist = sorted(set([x[3] for x in contours]))
    
    dx = 25
    for j in [llist, tlist, rlist, blist]:
        base = j[0]
        for i in j[1:]:
            if abs(i - base) < dx:
                j.remove(i)
            else:
                j.append(base)
            base = i
        j.append(base)
    
    llist = sorted(llist)
    tlist = sorted(tlist)
    rlist = sorted(rlist)
    blist = sorted(blist)
    
    for j in [llist, tlist, rlist, blist]:
        print(j)
    
    rows = 8
    cols = 12
    
    activeCogs = []
    
    for row in range(rows):
        r = 2*row
        for col in range(cols):
            c = 2*col
            print(r, c)
            addition = (rlist[c + 1] - 72, tlist[r], rlist[c + 1] - 12, tlist[r] + 30)
            print(addition)
            activeCogs.append(addition)
            #cv2.rectangle(image, (addition[0],addition[1]), (addition[2],addition[3]),(36, 255, 12), 3)
            im = CropImage(image, *addition, False)
            im.save(str(row) + "_" + str(col) + "_" + "activeCog.png", "PNG")
    #image = cv2.imread(image)
    #cv2.destroyAllWindows() 
    print(activeCogs)

    #for row in range(2):
    #    for col in range(9):
    #        print(img2text(str(row) + "_" + str(col) + "_" + "activeCog.png", True))

    return activeCogs

#CropImage("screen.jpg", 400, 200, 500, 800)


if __name__== "__main__":
    acc = getActiveCogCoords("test.png")
    cropCogNumbers("screen.png")
    for row in range(2):
        for col in range(2):
            print(img2text(str(row) + "_" + str(col) + "_" + "cog.png", True))
            print(img2text(str(row) + "_" + str(col) + "_" + "activeCog.png", True))

    for x in coords["Inventory"]:
        print(x)
        #tap(*x)
