import cv2
import numpy as np
import keyboard
import mss
import pyautogui
import pytesseract
import re
from time import time, sleep

tesseract_location = open('tesseract.txt', 'r').read()
pytesseract.pytesseract.tesseract_cmd = tesseract_location

# Importing images for matching
yordle_card_image = cv2.imread('charCards\\yordleCard.png', cv2.IMREAD_UNCHANGED)
janna_image = cv2.imread('charCards\\janna.png', cv2.IMREAD_UNCHANGED)
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

level_dimensions = {
        'left': 265,
        'top': 878,
        'width': 160,
        'height': 30
    }

gold_dimensions = {
        'left': 868,
        'top': 883,
        'width': 40,
        'height': 30
    }

# Screenshotter
sct = mss.mss()

bottomval = 0.9

gold = 0
level = 1

# Game Loop
while True:

    # YORDLE PURCHASING

    shopScr = np.array(sct.grab(shop_dimensions))

    matchedYordleCards = cv2.matchTemplate(shopScr, yordle_card_image, cv2.TM_CCOEFF_NORMED)

    yloc, xloc = np.where(matchedYordleCards >= bottomval)

    yordleCards = []

    for (x, y) in zip(xloc, yloc):
        yordleCards.append([int(x), int(y), int(yordle_card_image.shape[1]), int(yordle_card_image.shape[0])])

    if level >= 7:
        matchedJannaCard = cv2.matchTemplate(shopScr, janna_image, cv2.TM_CCOEFF_NORMED)
        yloc, xloc = np.where(matchedJannaCard >= bottomval)

        for (x, y) in zip(xloc, yloc):
            yordleCards.append([int(x), int(y), int(janna_image.shape[1]), int(janna_image.shape[0])])


    for (x, y, w, h) in yordleCards:
        pyautogui.moveTo(x=x+472+(w/2), y=y+924+(h/2), duration=0.2)
        pyautogui.mouseDown()
        sleep(0.05)
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
    yloc, xloc = np.where(matchedCommonOrbs >= 0.75)

    for (x, y) in zip(xloc, yloc):
        orbLocations.append([int(x), int(y), int(common_orb_image.shape[1]), int(common_orb_image.shape[0])])
        break
    
    # Adding Rare Orbs
    yloc, xloc = np.where(matchedRareOrbs >= 0.75)

    for (x, y) in zip(xloc, yloc):
        orbLocations.append([int(x), int(y), int(rare_orb_image.shape[1]), int(rare_orb_image.shape[0])])
        break

    # Adding Legendary Orbs
    yloc, xloc = np.where(matchedLegendaryOrbs >= 0.75)
    
    for (x, y) in zip(xloc, yloc):
        orbLocations.append([int(x), int(y), int(legendary_orb_image.shape[1]), int(legendary_orb_image.shape[0])])
        break

    for (x, y, w, h) in orbLocations:
        pyautogui.moveTo(x=x, y=y, duration=0.2)
        pyautogui.mouseDown(button='right')
        sleep(0.1)
        pyautogui.mouseUp(button='right')
        sleep(1.5)


    # LEVEL & GOLD INFORMATION

    # Changing to RGB
    levelScr = np.array(sct.grab(level_dimensions))
    levelScr = np.flip(levelScr[:, :, :3], 2)

    goldScr = np.array(sct.grab(gold_dimensions))
    goldScr = np.flip(goldScr[:, :, :3], 2)

    # Reading the level and saving it
    try:
        levelText = pytesseract.image_to_string(levelScr)
        lvlNumFind = re.findall('[0-9]+', levelText)
        level = int(lvlNumFind[0])
    except:
        print("Not tabbed onto league!")

    # Reading the gold and saving it
    try:
        goldText = pytesseract.image_to_string(goldScr, config='--psm 8')
        goldNumFind = re.findall('[0-9]+', goldText)
        gold = int(goldNumFind[0])
    except:
        print("Not tabbed onto league!")

    print(level)
    print(gold)

    # Level if below 6
    if (gold >= 54 and level < 6):
        pyautogui.moveTo(x=360, y=960, duration=0.2)
        pyautogui.mouseDown()
        sleep(0.05)
        pyautogui.mouseUp()
    
    # Roll if 6
    if (gold >= 52 and level == 6):
        pyautogui.moveTo(x=360, y=1040, duration=0.2)
        pyautogui.mouseDown()
        sleep(0.05)
        pyautogui.mouseUp()

    # Alternate above 6
    if (gold >= 70 and level == 7):
        pyautogui.moveTo(x=360, y=960, duration=0.2)
        while (gold > 3):
            pyautogui.mouseDown()
            sleep(0.05)
            pyautogui.mouseUp()

    if (gold >= 12 and level >= 8):
        pyautogui.moveTo(x=360, y=1040, duration=0.2)
        pyautogui.mouseDown()
        sleep(0.05)
        pyautogui.mouseUp()
