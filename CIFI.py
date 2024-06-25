#Based on phone.py
from subprocess import call
from subprocess import check_output as co
import time
import sys

widthheight = co(["adb", "shell", "wm", "size"]).decode(sys.stdout.encoding)
widthheight = widthheight[widthheight.rfind(" ") + 1:-1]
width = int(widthheight[:widthheight.find("x")])
height = int(widthheight[widthheight.find("x") + 1:])

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

GetColorAtPixel = ColourFunction(width, height)

coords = {  "Next Ship" : (800, 2065),
            "Previous Ship" : (300, 2065),
            "Build Ship" : (540, 1700),
            "Upgrades" : (540, 2300),
            "Loop Mods" : (540, 1800),
            "Loop Reset" : (310, 800),
            "Confirm Reset" : (530, 2000),
            "Charge Engine" : (530, 2100),
            "LM Return" : (530, 2300),
            "Loop Wheel" : (572, 1248),
        }

def tap(x, y):
    call(["adb", "shell", "input", "tap", str(x), str(y)])
    time.sleep(.1)

def Long_Reset(compare): #Compare = 393
    print("Loop Reset")

    #To see the pointer information
    #call(["adb","shell","settings","put","system","pointer_location","1"])
    tap(*coords["LM Return"])
    sumColours = -9000
    while (abs(sumColours - compare) > 50):
        time.sleep(1)
        sumColours = GetColorAtPixel(*coords["Loop Wheel"]) 
        print("Checking button colour before reset: ", sumColours, sum(sumColours))
        sumColours = sum(sumColours)
    tap(*coords["Loop Reset"])
    tap(*coords["Confirm Reset"])
    for j in range(5):
        tap(*coords["Charge Engine"])
    #call(["adb","shell","settings","put","system","pointer_location","0"])
    print("Done Loop Reset")

def Fast_Reset(compare): #compare = 356
    print("Loop Reset")

    #To see the pointer information
    #call(["adb","shell","settings","put","system","pointer_location","1"])
    tap(*coords["LM Return"])
    sumColours = compare
    while (abs(sumColours - compare) < 10):
        time.sleep(1)
        sumColours = GetColorAtPixel(*coords["Loop Reset"]) 
        print("Checking button colour before reset: ", sumColours)
        sumColours = sum(sumColours)
    tap(*coords["Loop Reset"])
    tap(*coords["Confirm Reset"])
    for j in range(5):
        tap(*coords["Charge Engine"])
    #call(["adb","shell","settings","put","system","pointer_location","0"])
    print("Done Loop Reset")

call(["adb","shell","settings","put","system","pointer_location","0"])
for i in range(1000):
    #Fast_Reset(25+33+43+255)    
    temp = GetColorAtPixel(*coords["Loop Wheel"])
    print(temp, sum(temp))
    Long_Reset(393)    
