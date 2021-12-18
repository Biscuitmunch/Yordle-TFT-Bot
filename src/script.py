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

# Importing Stage Images
stage_one_image = cv2.imread('stageNumbers\\stageOne.png', cv2.IMREAD_UNCHANGED)
stage_two_image = cv2.imread('stageNumbers\\stageTwo.png', cv2.IMREAD_UNCHANGED)
stage_three_image = cv2.imread('stageNumbers\\stageThree.png', cv2.IMREAD_UNCHANGED)
stage_four_image = cv2.imread('stageNumbers\\stageFour.png', cv2.IMREAD_UNCHANGED)
stage_five_image = cv2.imread('stageNumbers\\stageFive.png', cv2.IMREAD_UNCHANGED)
stage_six_image = cv2.imread('stageNumbers\\stageSix.png', cv2.IMREAD_UNCHANGED)

dash_one_image = cv2.imread('stageNumbers\\dashOne.png', cv2.IMREAD_UNCHANGED)
dash_two_image = cv2.imread('stageNumbers\\dashTwo.png', cv2.IMREAD_UNCHANGED)
dash_three_image = cv2.imread('stageNumbers\\dashThree.png', cv2.IMREAD_UNCHANGED)
dash_four_image = cv2.imread('stageNumbers\\dashFour.png', cv2.IMREAD_UNCHANGED)
dash_five_image = cv2.imread('stageNumbers\\dashFive.png', cv2.IMREAD_UNCHANGED)
dash_six_image = cv2.imread('stageNumbers\\dashSix.png', cv2.IMREAD_UNCHANGED)
dash_seven_image = cv2.imread('stageNumbers\\dashSeven.png', cv2.IMREAD_UNCHANGED)

# Screenshotter
sct = mss.mss()

bottomval = 0.9

type = 'null'

gold = 0
level = 1

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

stage_dimensions = {
        'left': 740,
        'top': 1,
        'width': 440,
        'height': 34
    }

def orbPickups():

    boardScr = np.array(sct.grab(monitor_dimensions))

    # Common Orbs
    matchedCommonOrbs = cv2.matchTemplate(boardScr, common_orb_image, cv2.TM_CCOEFF_NORMED)
    matchedRareOrbs = cv2.matchTemplate(boardScr, rare_orb_image, cv2.TM_CCOEFF_NORMED)
    matchedLegendaryOrbs = cv2.matchTemplate(boardScr, legendary_orb_image, cv2.TM_CCOEFF_NORMED)

    orbLocations = []

    # Adding Common Orbs
    yloc, xloc = np.where(matchedCommonOrbs >= 0.72)

    for (x, y) in zip(xloc, yloc):
        orbLocations.append([int(x), int(y), int(common_orb_image.shape[1]), int(common_orb_image.shape[0])])
        break
    
    # Adding Rare Orbs
    yloc, xloc = np.where(matchedRareOrbs >= 0.72)

    for (x, y) in zip(xloc, yloc):
        orbLocations.append([int(x), int(y), int(rare_orb_image.shape[1]), int(rare_orb_image.shape[0])])
        break

    # Adding Legendary Orbs
    yloc, xloc = np.where(matchedLegendaryOrbs >= 0.72)
    
    for (x, y) in zip(xloc, yloc):
        orbLocations.append([int(x), int(y), int(legendary_orb_image.shape[1]), int(legendary_orb_image.shape[0])])
        break

    for (x, y, w, h) in orbLocations:
        pyautogui.moveTo(x=x, y=y, duration=0.2)
        pyautogui.mouseDown(button='right')
        sleep(0.1)
        pyautogui.mouseUp(button='right')
        sleep(1.5)


def purchaseUnits():

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

def getStageNumber():

    stageScr = np.array(sct.grab(stage_dimensions))

    StageOne = cv2.matchTemplate(stageScr, stage_one_image, cv2.TM_CCOEFF_NORMED).max()
    StageTwo = cv2.matchTemplate(stageScr, stage_two_image, cv2.TM_CCOEFF_NORMED).max()
    StageThree = cv2.matchTemplate(stageScr, stage_three_image, cv2.TM_CCOEFF_NORMED).max()
    StageFour = cv2.matchTemplate(stageScr, stage_four_image, cv2.TM_CCOEFF_NORMED).max()
    StageFive = cv2.matchTemplate(stageScr, stage_five_image, cv2.TM_CCOEFF_NORMED).max()
    StageSix = cv2.matchTemplate(stageScr, stage_six_image, cv2.TM_CCOEFF_NORMED).max()

    stageVals = [StageOne, StageTwo, StageThree, StageFour, StageFive, StageSix]
    maxStageMatch = max(stageVals)
    stageValue = stageVals.index(maxStageMatch) + 1


    DashOne = cv2.matchTemplate(stageScr, dash_one_image, cv2.TM_CCOEFF_NORMED).max()
    DashTwo = cv2.matchTemplate(stageScr, dash_two_image, cv2.TM_CCOEFF_NORMED).max()
    DashThree = cv2.matchTemplate(stageScr, dash_three_image, cv2.TM_CCOEFF_NORMED).max()
    DashFour = cv2.matchTemplate(stageScr, dash_four_image, cv2.TM_CCOEFF_NORMED).max()
    DashFive = cv2.matchTemplate(stageScr, dash_five_image, cv2.TM_CCOEFF_NORMED).max()
    DashSix = cv2.matchTemplate(stageScr, dash_six_image, cv2.TM_CCOEFF_NORMED).max()
    DashSeven = cv2.matchTemplate(stageScr, dash_seven_image, cv2.TM_CCOEFF_NORMED).max()

    dashNums = [DashOne, DashTwo, DashThree, DashFour, DashFive, DashSix, DashSeven]
    maxDashMatch = max(dashNums)
    dashValue = dashNums.index(maxDashMatch) + 1


    return stageValue * 10 + dashValue

def roundType():
    # PvE Stage. Checking for Stage '1 - x', 'x - 1', or 'x - 7'

    if stageNumber == 11 or (stageNumber - 4) % 10 == 0:
        type = 'carousel'
    elif stageNumber < 20 or (stageNumber - 7) % 10 == 0:
        type = 'pve'
    elif (stageNumber - 1) % 10 == 0:
        type = 'postpve'
    else:
        type = 'standard'

    return type

def goldRead():

    goldScr = np.array(sct.grab(gold_dimensions))
    goldScr = np.flip(goldScr[:, :, :3], 2)

    # Reading the gold and saving it
    try:
        goldText = pytesseract.image_to_string(goldScr, config='--psm 8')
        goldNumFind = re.findall('[0-9]+', goldText)
        gold = int(goldNumFind[0])
    except:
        print("Not tabbed onto league!")

    return gold

def levelRead():

    # Changing to RGB
    levelScr = np.array(sct.grab(level_dimensions))
    levelScr = np.flip(levelScr[:, :, :3], 2)

    # Reading the level and saving it
    try:
        levelText = pytesseract.image_to_string(levelScr)
        lvlNumFind = re.findall('[0-9]+', levelText)
        level = int(lvlNumFind[0])
    except:
        print("Not tabbed onto league!")

    return level

# Game Loop
while True:

    sleep(0.1)

    # Format stage in 10's, dash in 1's eg 2-3 is 23
    stageNumber = getStageNumber()

    # Checking if standard, PvE, or carousel
    type = roundType()
    
    print(stageNumber)

    # YORDLE PURCHASING FROM NATURAL ROLL
    purchaseUnits()

    if (type == 'pve' or type == 'postpve'):
        orbPickups()

    # LEVEL & GOLD INFORMATION

    gold = goldRead()

    level = levelRead()

    print(level)
    print(gold)
    print(type)

    # Level if below 6
    while (gold >= 54 and level < 6):
        pyautogui.moveTo(x=360, y=960, duration=0.2)
        pyautogui.mouseDown()
        sleep(0.05)
        pyautogui.mouseUp()

        purchaseUnits()

        gold = goldRead()
        level = levelRead()
    
    # Roll if 6
    while (gold >= 52 and level == 6):
        pyautogui.moveTo(x=360, y=1040, duration=0.2)
        pyautogui.mouseDown()
        sleep(0.05)
        pyautogui.mouseUp()

        purchaseUnits()

        gold = goldRead()
        level = levelRead()

    # Skip to 8 (Janna and Veigar)
    if (gold >= 70 and level == 7):
        pyautogui.moveTo(x=360, y=960, duration=0.2)
        while (level < 8):
            pyautogui.mouseDown()
            sleep(0.05)
            pyautogui.mouseUp()

            level = levelRead()


    while (gold >= 12 and level >= 8):
        pyautogui.moveTo(x=360, y=1040, duration=0.2)
        pyautogui.mouseDown()
        sleep(0.05)
        pyautogui.mouseUp()

        purchaseUnits()

        gold = goldRead()
        level = levelRead()
