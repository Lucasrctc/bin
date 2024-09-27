import pyautogui
import sys
import time
from PIL import Image, ImageDraw

def toBox(left, top, width, height):
    return (left, top, left + width, top + height)

def drawX(draw, pos):
        draw.line((pos[0] - 10, pos[1] - 10, pos[0] + 10, pos[1] + 10), fill=128, width = 3)
        draw.line((pos[0] + 10, pos[1] - 10, pos[0] - 10, pos[1] + 10), fill=128, width = 3)

def mainLoop(harvest, shovel, sprinkler, log):
    dt = 1
    pyautogui.click(*shovel, duration = dt)
    pyautogui.click(*harvest, duration = dt)
    #for i in range(3):
        #pyautogui.click(*sprinkler, duration = dt)
        #pyautogui.click(*harvest, duration = dt)
    pyautogui.click(*log, duration = dt)
    time.sleep(2)
    card = 1
    i = 0
    ret = False
    while card != None and i != 20:
        i += 1
        try:
            card = pyautogui.locateCenterOnScreen('aux/card.png', confidence = .8)
            pyautogui.click(*card)
            ret = True
        except:
            card = None
        time.sleep(2)
    return ret

shovel = pyautogui.locateCenterOnScreen('aux/shovel.png', confidence = .79)
log = pyautogui.locateCenterOnScreen('aux/log.png', confidence = .79)
sprinkler = None
#sprinkler = pyautogui.locateCenterOnScreen('aux/sprinkler.png', confidence = .9)
harvest = pyautogui.locateCenterOnScreen('aux/harvest_button.png', confidence = .79)

while True:
    p = []
    try:
        p = [pyautogui.locateOnScreen('aux/chem.png', confidence = .7)]
    except:
        p = []
    print(len(p), "Matches")
    print(p)
#    pyautogui.screenshot('aux/foo.png')

#    with Image.open("aux/foo.png") as im:
#        draw = ImageDraw.Draw(im)
#        drawX(draw, shovel)
#        drawX(draw, log)
#        #drawX(draw, sprinkler)
#        drawX(draw, harvest)
#        #im.show()
    loop = mainLoop(harvest, shovel, sprinkler, log)
    for target in p:
        while loop:
            loop = mainLoop(harvest, shovel, sprinkler, log)
        target = pyautogui.center(target)
        pyautogui.click(*target)
        #box = toBox(*target)
        #draw.rectangle(box, outline=128)
        #drawX(draw, pyautogui.center(target))
