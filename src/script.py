import cv2
import numpy as np
import keyboard
import mss
import pyautogui
import pytesseract
from time import time, sleep

# Importing images for matching
yordle_card_image = cv2.imread('charCards\\yordleCard.png', cv2.IMREAD_UNCHANGED)
common_orb_image = cv2.imread('orbPickups\\commonOrb.png', cv2.IMREAD_UNCHANGED)
rare_orb_image = cv2.imread('orbPickups\\rareOrb.png', cv2.IMREAD_UNCHANGED)
legendary_orb_image = cv2.imread('orbPickups\\legendaryOrb.png', cv2.IMREAD_UNCHANGED)


# Shop Area
shop_dimensions = {
        'left': 472,
        'top': 924,
        'width': 1010,
        'height': 151
    }

monitor_dimensions = {
        'left': 0,
        'top': 0,
        'width': 1920,
        'height': 1080
    }

# Screenshotter
sct = mss.mss()

bottomval = 0.9

# Game Loop
while True:

    sleep(1)

    # YORDLE PURCHASING
    shopScr = np.array(sct.grab(shop_dimensions))

    matchedYordleCards = cv2.matchTemplate(shopScr, yordle_card_image, cv2.TM_CCOEFF_NORMED)

    yloc, xloc = np.where(matchedYordleCards >= bottomval)

    yordleCards = []

    for (x, y) in zip(xloc, yloc):
        yordleCards.append([int(x), int(y), int(yordle_card_image.shape[1]), int(yordle_card_image.shape[0])])

    for (x, y, w, h) in yordleCards:
        pyautogui.moveTo(x=x+472, y=y+924, duration=0.2)
        pyautogui.mouseDown()
        sleep(0.1)
        pyautogui.mouseUp()
        

    if keyboard.is_pressed('p'):
        break


    # ORB PICKUPS
    boardScr = np.array(sct.grab(monitor_dimensions))

    # Common Orbs
    matchedCommonOrbs = cv2.matchTemplate(boardScr, common_orb_image, cv2.TM_CCOEFF_NORMED)
    matchedRareOrbs = cv2.matchTemplate(boardScr, rare_orb_image, cv2.TM_CCOEFF_NORMED)
    matchedLegendaryOrbs = cv2.matchTemplate(boardScr, legendary_orb_image, cv2.TM_CCOEFF_NORMED)

    orbLocations = []

    # Adding Common Orbs
    yloc, xloc = np.where(matchedCommonOrbs >= bottomval)

    for (x, y) in zip(xloc, yloc):
        orbLocations.append([int(x), int(y), int(common_orb_image.shape[1]), int(common_orb_image.shape[0])])
    
    # Adding Rare Orbs
    yloc, xloc = np.where(matchedRareOrbs >= bottomval)

    for (x, y) in zip(xloc, yloc):
        orbLocations.append([int(x), int(y), int(rare_orb_image.shape[1]), int(rare_orb_image.shape[0])])

    # Adding Legendary orbs
    yloc, xloc = np.where(matchedLegendaryOrbs >= bottomval)
    
    for (x, y) in zip(xloc, yloc):
        orbLocations.append([int(x), int(y), int(legendary_orb_image.shape[1]), int(legendary_orb_image.shape[0])])

    for (x, y, w, h) in orbLocations:
        pyautogui.moveTo(x=x, y=y, duration=0.2)
        pyautogui.mouseDown(button='right')
        sleep(0.1)
        pyautogui.mouseUp(button='right')
        sleep(1.5)