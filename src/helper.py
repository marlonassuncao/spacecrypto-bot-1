from random import random, uniform
import sys
import cv2
import mss
import time
import numpy as np
import pyautogui

try:
    from pyclick import HumanClicker
except ImportError or ModuleNotFoundError:
    print('pyclick not found! Run pip install -r requirements.txt again.')
    time.sleep(5)
    sys.exit(1)

hc = HumanClicker()

pyautogui.MINIMUM_DURATION = 0.1
pyautogui.MINIMUM_SLEEP = 0.1
pyautogui.PAUSE = 1


def handlePopup(screen=None):
    if screen is None:
        screen = printSreen()

    if(hasImage('close-button.png', 0.7, screen)):
        clickDestinationImage(
            'close-button.png', 'close-button')

    handleConfirm(screen)
    handleAfterBattleConfirm(screen)


def handleConfirm(screen=None):
    if(hasImage('confirm-button.png', 0.65, screen)):
        clickDestinationImage(
            'confirm-button.png', 'confirm-button', 1, 0.65)


def handleAfterBattleConfirm(screen=None):
    if(hasImage('after-battle-confirm-button.png', 0.65, screen)):
        clickDestinationImage(
            'after-battle-confirm-button.png', 'after-battle-confirm-button', 0.5, 0.65)

    if(hasImage('after-battle-confirm-button2.png', 0.65, screen)):
        clickDestinationImage(
            'after-battle-confirm-button2.png', 'after-battle-confirm-button', 0.5, 0.65)


def moveDestination(x, y, time=2):
    hc.move((int(x), int(y)), time)


def clickDestination(x, y, duration=2):
    moveDestination(x, y, duration)
    time.sleep(1)
    pyautogui.click()


def clickDestinationImage(img, name=None, timeout=2, threshold=0.7):
    if not name is None:
        pass

    start = time.time()
    while(True):
        matches = getImagePositions(img, threshold)
        if(len(matches) == 0):
            has_timed_out = time.time()-start > timeout
            if(has_timed_out):
                return False

            continue

        if(len(matches) < 1):
            print('Destination image not found: ', img)
            return

        x, y, w, h = matches[0]

        pos_click_x = round(x+w/2+uniform(2, 10))
        pos_click_y = round(y+h/2+uniform(-2, -10))

        clickDestination(pos_click_x, pos_click_y, 2)

        #pyautogui.moveTo(pos_click_x, pos_click_y, 1 + random()/2)
        # pyautogui.click()

        return True


def getImage(filename):
    path = 'target_images/' + filename

    return cv2.imread(path)


def hasImage(name, threshold=0.7, img=None):
    image = getImagePositions(name, threshold, img)

    return len(image) > 0


def getImagePositions(imageName, threshold=0.7, img=None):
    if img is None:
        img = printSreen()

    target = getImage(imageName)

    result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

    return rectangles


def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))

        return sct_img[:, :, :3]


def isShipSelectScreen(screen=None):
    positions = getImagePositions(
        'genesis-box-text.png', 0.9, screen)

    return len(positions) > 0


def isBattling():
    positions = getImagePositions('surrender-button.png')

    return len(positions) > 0


def isShipsListFull(screen=None):
    shipsInListFull = getImagePositions(
        'main-ship-list-full.png', 0.95, screen)

    return len(shipsInListFull)
