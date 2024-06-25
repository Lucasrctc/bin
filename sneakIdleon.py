from subprocess import call
from subprocess import check_output
from PIL import Image
import time
import sys

coords = {  
            "deposit" : (200, 600),
            "storage" : (920, 600),
            "sneak" : (920, 920),
            #"sneak_inv" : (100, 700),
            "sneak_inv" : (100, 416),
        }

def co(s):
    return check_output(s).decode(sys.stdout.encoding)

def tap(x, y):
    subprocess.call(["xdotool", "mousemove", str(x), str(y), "click", "1"])
    time.sleep(.15)

def codex():
    cmd = "xdotool search --name Legends windowfocus --sync key c".split()
    call(cmd)

def idle(delta):
    delta = delta

    cmd = "xdotool getwindowfocus".split()
    wid = int(co(cmd))

    print("Open storage")
    cmd = ("xdotool search --name Legends windowfocus --sync mousemove --sync %s %s click 1 mousemove restore windowfocus %s"%(*coords["storage"], wid)).split()
    call(cmd)

    time.sleep(delta)

    print("Deposit")
    cmd = "xdotool getwindowfocus".split()
    wid = int(co(cmd))
    cmd = ("xdotool search --name Legends windowfocus --sync mousemove --sync %s %s click 1 mousemove restore windowfocus %s"%(*coords["deposit"], wid)).split()
    call(cmd)

    time.sleep(delta)

    print("Back to Codex")
    codex()
    cmd = ("xdotool windowfocus %s"%wid).split()
    call(cmd)

    time.sleep(delta)

    print("Open sneak")
    cmd = "xdotool getwindowfocus".split()
    wid = int(co(cmd))
    cmd = ("xdotool search --name Legends windowfocus --sync mousemove --sync %s %s click 1 mousemove restore windowfocus %s"%(*coords["sneak"], wid)).split()
    call(cmd)

    time.sleep(delta)

    print("Open sneak_inventory")
    cmd = "xdotool getwindowfocus".split()
    wid = int(co(cmd))
    cmd = ("xdotool search --name Legends windowfocus --sync mousemove --sync %s %s click 1 mousemove restore windowfocus %s"%(*coords["sneak_inv"], wid)).split()
    call(cmd)

    time.sleep(delta)

    print("Back to Codex")
    codex()
    cmd = ("xdotool windowfocus %s"%wid).split()
    call(cmd)

    time.sleep(delta)

def Screenshot():
    call(["rm", "screen.png"])
    idleonID = 1476970
    #call(cmd)
    cmd = "xwininfo  -name  Legends Of Idleon".split("  ")
    wid = co(cmd).decode(sys.stdout.encoding)
    wid = wid[wid.find("0x"):]
    wid = wid[:wid.find(" ")]
    cmd = ("import -window " + str(wid) +" screen.png").split()
    call(cmd)

def GetColourAtPixel (x, y):
    with Image.open("screen.png", "r") as infile:
        width, height = infile.size
        pixel_values = list(infile.getdata())
        pixel = pixel_values[width * y + x]
    return pixel

def GetSquareAverage(x, y):
    with Image.open("screen.png", "r") as infile:
        width, height = infile.size
        pixel_values = list(infile.getdata())
        pixel = [0, 0, 0]
        for j in range(42):
            for i in range(42):
                pixel[0] += pixel_values[width * (y+j) + x + i][0]
                pixel[1] += pixel_values[width * (y+j) + x + i][1]
                pixel[2] += pixel_values[width * (y+j) + x + i][2]
    return [i/(42*42) for i in pixel]

def GetCrossAtPixel(x, y):
    with Image.open("screen.png", "r") as infile:
        width, height = infile.size
        pixel_values = list(infile.getdata())
        pixel = []
        for j in range(-1, 2):
            for i in range(-1, 2):
                if j * i == 0:
                    pixel.append(pixel_values[width * (y+j) + x + i])
    return pixel

i = 0
while True:
    i += 1
    print(i)
    idle(2)

left = 187
right = 1530
top = 403
bot = 700

mouseleft = 191
mouseright = 1533
mousetop = 714
mousebot = 1018

col = 13
lin = 3

def getItemColours():
    sneakitemsx = [left + (right - left) // (2*col) + (i*((right - left)//col)) for i in range(col)]
    sneakitemsy = [top + (bot - top) // (2*lin) + (i*((bot - top)//lin)) for i in range(lin)]
    ret = []
    for j in range(lin - 1):
        for i in range(col):
            print("Pixel ", i + col * j + 1, sneakitemsx[i], sneakitemsy[j])
            ret.append(GetSquareAverage(sneakitemsx[i], sneakitemsy[j]))
    return ret
            
def Fast_Reset():
    print("Loop Reset")

    #To see the pointer information
    #call(["adb","shell","settings","put","system","pointer_location","1"])
    tap(*coords["LM Return"])
    compare = 25 + 33 + 43 + 255
    sumColours = compare
    while (abs(sumColours - compare) < 10):
        time.sleep(1)
        sumColours = GetColourAtPixel(*coords["Loop Reset"]) 
        print("Checking button colour before reset: ", sumColours)
        sumColours = sum(sumColours)
    tap(*coords["Loop Reset"])
    tap(*coords["Confirm Reset"])
    for j in range(5):
        tap(*coords["Charge Engine"])
    #call(["adb","shell","settings","put","system","pointer_location","0"])
    print("Done Loop Reset")

def avgColour(items):
    ret = [0, 0, 0]
    div = 1/len(items)
    for i in items:
        for n, j in enumerate(i):
            ret[n] += j * div
    return ret

#def classify(item, pool):
#    temp = []
#    for p in pool:
#        temp.append(abs(item[0] - p[0]))
#        temp[-1] += (abs(item[1] - p[1]))
#        temp[-1] += (abs(item[2] - p[2]))
#    return temp.index(min(temp))

def classify(item, pool):
    if item[2] < 41:
        return "chuck"
    if item[1] > 82:
        return "bomb"
    if item[2] > 80:
        return "jewel"
    if item[1] > 55:
        return "stump"
    return "nothing"

def testClassify():
    Screenshot()
    items = getItemColours()
    classifyData = [
    [80.51370851370852, 54.14182642754072, 38.29179550608122],
    [71.90680272108844, 66.43253968253968, 56.91303854875284],
    [80.68920068027211, 86.45804988662132, 87.22548185941044],
    [62.79931972789116, 79.78911564625851, 90.77267573696145],
    [66.60104875283446, 48.069019274376416, 42.3047052154195]
    ]
    chucks = items[:11]
    stumps = items[12:17]
    bombs = items[17:21]
    jewel = items[21:22]
    nothing = items[22:]

    for n, i in enumerate(items):
        print(n, i)

    #classifyData = [avgColour(chucks), avgColour(stumps), avgColour(bombs), avgColour(jewel), avgColour(nothing)]

    for n, i in enumerate(classifyData):
        print(n, i)

    for n, i in enumerate(items):
        print(n, classify(i, classifyData))

#xdotool getwindowfocus mousemove 220 1675 click 1 windowfocus --sync %1 mousemove restore 
