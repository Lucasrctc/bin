import pyautogui
import sys
import time
from PIL import Image, ImageDraw

def toBuilding(x, y):
    dy = 20
    return (x, y + dy)

def toBox(left, top, width, height):
    return (left, top, left + width, top + height)

def drawX(draw, pos):
        draw.line((pos[0] - 10, pos[1] - 10, pos[0] + 10, pos[1] + 10), fill=128, width = 3)
        draw.line((pos[0] + 10, pos[1] - 10, pos[0] - 10, pos[1] + 10), fill=128, width = 3)

def locate(img, conf):
    try:
        return pyautogui.locateOnScreen(img, confidence = conf)
    except:
        return None

def mainLoop():
    dt = 0.5

    target = locate("aux/build_done.png", 0.9)
    if target != None:
        target = pyautogui.center(target)
        print("Building finished")
        target = toBuilding(*target)
        pyautogui.click(*target, duration = dt)
        build = locate("aux/build_button.png", 0.8)
        if build != None:
            build = pyautogui.center(build)
            print("Building button found")
            pyautogui.click(*build, duration = dt)
            pyautogui.click(*build, duration = dt)
            pyautogui.click(*build, duration = dt)
        pyautogui.click(*target, duration = dt)

i = 1
while True:
    mainLoop()
    print(i)
    time.sleep(1)
    i += 1
