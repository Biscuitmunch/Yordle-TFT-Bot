import cv2
import numpy as np
import keyboard
import mss
import pyautogui
from time import time, sleep

# Importing yordle's card image
yordle_card_image = cv2.imread('charCards\\yordleCard.png', cv2.IMREAD_UNCHANGED)

# Shop Area
shop_dimnensions = {
        'left': 472,
        'top': 924,
        'width': 1010,
        'height': 151
    }

# Screenshotter
sct = mss.mss()

bottomval = 0.9

# Game Loop
while True:

    sleep(1)

    scr = np.array(sct.grab(shop_dimnensions))

    matchSpots = cv2.matchTemplate(scr, yordle_card_image, cv2.TM_CCOEFF_NORMED)

    yloc, xloc = np.where(matchSpots >= bottomval)

    yordleCards = []

    for (x, y) in zip(xloc, yloc):
        yordleCards.append([int(x), int(y), int(yordle_card_image.shape[1]), int(yordle_card_image.shape[0])])

    for (x, y, w, h) in yordleCards:
        sleep(1)
        pyautogui.click(x=x+472, y=y+924)

    if keyboard.is_pressed('p'):
        break
