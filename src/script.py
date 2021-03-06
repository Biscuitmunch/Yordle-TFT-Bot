from contextlib import nullcontext
from enum import Enum
from os import write
import cv2
import numpy as np
import keyboard
import mss
import pyautogui
import pytesseract
import re
from time import time, sleep
import random

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

# Importing Yordle Ult Images
poppy_ult_image = cv2.imread('ultIcons\\poppyUlt.png', cv2.IMREAD_UNCHANGED)
ziggs_ult_image = cv2.imread('ultIcons\\ziggsUlt.png', cv2.IMREAD_UNCHANGED)
lulu_ult_image = cv2.imread('ultIcons\\luluUlt.png', cv2.IMREAD_UNCHANGED)
tristana_ult_image = cv2.imread('ultIcons\\tristanaUlt.png', cv2.IMREAD_UNCHANGED)
heimer_ult_image = cv2.imread('ultIcons\\heimerUlt.png', cv2.IMREAD_UNCHANGED)
vex_ult_image = cv2.imread('ultIcons\\vexUlt.png', cv2.IMREAD_UNCHANGED)

#import tierList
tierListFile = open("augmentTierList.txt", "r")
augmentTierList = tierListFile.readlines()
#remove the newline character at the end of each augment name
for i in range(len(augmentTierList)) : 
    augmentTierList[i] = augmentTierList[i][:-1]

class Champions(Enum) :
    Nothing=0
    Something=1
    Poppy=2
    Ziggs=3
    Lulu=4
    Tristana=5
    Heimerdinger=6
    Vex=7
    Janna=8
    Veigar=9

# Hex Positions
hex_positions = [[561, 444, 0], [679, 444, 0], [787, 444, 0], [900, 444, 0], [1020, 444, 0], [1136, 444, 0], [1250, 444, 0],
                 [607, 515, 0], [730, 515, 0], [846, 515, 0], [963, 515, 0], [1081, 515, 0], [1200, 515, 0], [1320, 515, 0],
                 [561, 591, 0], [679, 591, 0], [787, 591, 0], [900, 591, 0], [1020, 591, 0], [1136, 591, 0], [1250, 591, 0],
                 [607, 670, 0], [730, 670, 0], [846, 670, 0], [963, 670, 0], [1081, 670, 0], [1200, 670, 0], [1320, 670, 0]]

bench_positions = [[457, 787, 0], [575, 787, 0], [683, 787, 0], [802, 787, 0], [920, 787, 0], [1040, 787, 0], [1156, 787, 0], [1270, 787, 0], [1390, 787, 0]]

# Screenshotter
sct = mss.mss()

bottomval = 0.9

yordlesBought = 0

singleExpBuy = 0

gameMode = 'null'

gold = 0
level = 1

augmentsPicked = [False,False,False]

# Shop Area
shop_dimensions = {
        'left': 485,
        'top': 954,
        'width': 830,
        'height': 80
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

ultimate_dimensions = {
        'left': 423,
        'top': 675,
        'width': 1133,
        'height': 142
    }

def orbPickups():

    sleep(0.4)
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
        rightClick()
        sleep(1.5)

def taunt():

    tauntLines = open('taunts.txt').read().splitlines()
    tauntLineChosen = random.choice(tauntLines)

    pyautogui.press('enter')
    pyautogui.write(tauntLineChosen)
    pyautogui.press('enter')


def purchaseUnits():

    global yordlesBought
    shopScr = np.array(sct.grab(shop_dimensions))

    matchedYordleCards = cv2.matchTemplate(shopScr, yordle_card_image, cv2.TM_CCOEFF_NORMED)

    yloc, xloc = np.where(matchedYordleCards >= bottomval)

    yordleCards = []

    for (x, y) in zip(xloc, yloc):
        yordlesBought = yordlesBought + 1
        yordleCards.append([int(x), int(y), int(yordle_card_image.shape[1]), int(yordle_card_image.shape[0])])

    if level >= 7:
        
        matchedJannaCard = cv2.matchTemplate(shopScr, janna_image, cv2.TM_CCOEFF_NORMED)
        yloc, xloc = np.where(matchedJannaCard >= bottomval)

        for (x, y) in zip(xloc, yloc):
            yordleCards.append([int(x), int(y), int(janna_image.shape[1]), int(janna_image.shape[0])])


    for (x, y, w, h) in yordleCards:
        pyautogui.moveTo(x=x+472+(w/2), y=y+924+(h/2))
        pyautogui.mouseDown()
        sleep(0.05)
        pyautogui.mouseUp()


def getStageNumber():

    sleep(0.4)
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

def getGameMode():

    if (stageNumber == 14) or (stageNumber == 33) or (stageNumber == 46):
        if(checkIfAugmentSelected()==False):
            return 'augment'

    # PvE Stage. Checking for Stage '1 - x', 'x - 1', or 'x - 7'

    if stageNumber == 11 or (stageNumber - 4) % 10 == 0: #BUG fix this
        return 'carousel'
    elif stageNumber < 20 or (stageNumber - 7) % 10 == 0:
        return 'pve'
    elif (stageNumber - 1) % 10 == 0:
        return 'postpve'
    else:
        return 'standard'

def readGold():

    sleep(0.4)
    goldScr = np.array(sct.grab(gold_dimensions))
    goldScr = np.flip(goldScr[:, :, :3], 2)

    goldCurrent = 0

    # Reading the gold and saving it
    try:
        goldText = pytesseract.image_to_string(goldScr, config='--psm 8')
        goldNumFind = re.findall('[0-9]+', goldText)
        goldCurrent = int(goldNumFind[0])
    except:
        print("Not tabbed onto league!")

    return goldCurrent

def readLevel():

    sleep(0.4)
    # Changing to RGB
    levelScr = np.array(sct.grab(level_dimensions))
    levelScr = np.flip(levelScr[:, :, :3], 2)

    levelCurrent = 1

    # Reading the level and saving it
    try:
        levelText = pytesseract.image_to_string(levelScr)
        lvlNumFind = re.findall('[0-9]+', levelText)
        levelCurrent = int(lvlNumFind[0])
    except:
        print("Not tabbed onto league!")

    return levelCurrent

#returns if augment cards are on screen
def checkIfAugmentSelected():
    if(stageNumber==14):
        if(augmentsPicked[0]==False):
            augmentsPicked[0]==True
            return False
    elif(stageNumber==33):
        if(augmentsPicked[1]==False):
            augmentsPicked[1]==True
            return False
    elif(stageNumber==46):
        if(augmentsPicked[2]==False):
            augmentsPicked[2]==True
            return False

    return True

#returns the names of the 3 displayed augments on the screen
def readAugments(): #TODO implement augment text reading
    return ['null','null','null']

#selects which augment to pick
def selectAugment():

    augments = readAugments()
    augmentRanks = [255,255,255]

    for i in range(3):
        augmentRanks[i] = getAugmentTier(augments[i])

    augmentToPick = 0
    if (augmentRanks[0]>augmentRanks[1]):
        augmentToPick = 1
    if (augmentRanks[augmentToPick]>augmentRanks[2]):
        augmentToPick = 2

    augmentXLocation = 590+augmentToPick*360
    pyautogui.moveTo(x=augmentXLocation, y=530)
    click()
    sleep(1) #wait for augment selection animation to resolve

#find and return the position of the augment in the tierlist, if not match is found then return 255 and print an error message
def getAugmentTier(currentAugment):

    for i in range(len(augmentTierList)):
        if augmentTierList[i] == currentAugment:
            return i

    print("Augment Not Recognised") #TODO log a screenshot of the augment and what it was read as to know what went wrong
    return 255

def checkYordle(yor, tileArray):

    # 0 = Nothing, 1 = Something, 2 = Poppy, 3 = Ziggs, 4 = Lulu, 5 = Tristana, 6 = Heimerdinger, 7 = Vex, 8 = Janna, 9 = Veigar
    # Right clicking to see character
    pyautogui.moveTo(x=tileArray[yor][0], y=tileArray[yor][1], duration=0.2)

    rightClick()

    pyautogui.moveTo(x=460, y=652, duration=0.01)
    rightClick()
    sleep(0.05)

    # Right Clicked Unit Screenshot
    if (tileArray == bench_positions):
        unitScr = np.array(sct.grab(ultimate_dimensions))
        print('correct')
    else:
        unitScr = np.array(sct.grab(monitor_dimensions))

    

    poppySpot = cv2.matchTemplate(unitScr, poppy_ult_image, cv2.TM_CCOEFF_NORMED).max()
    ziggsSpot = cv2.matchTemplate(unitScr, ziggs_ult_image, cv2.TM_CCOEFF_NORMED).max()
    luluSpot = cv2.matchTemplate(unitScr, lulu_ult_image, cv2.TM_CCOEFF_NORMED).max()
    tristanaSpot = cv2.matchTemplate(unitScr, tristana_ult_image, cv2.TM_CCOEFF_NORMED).max()
    heimerSpot = cv2.matchTemplate(unitScr, heimer_ult_image, cv2.TM_CCOEFF_NORMED).max()
    vexSpot = cv2.matchTemplate(unitScr, vex_ult_image, cv2.TM_CCOEFF_NORMED).max()
    
    yorVals = [poppySpot, ziggsSpot, luluSpot, tristanaSpot, heimerSpot, vexSpot]
    maxYordleMatch = max(yorVals)
    
    if maxYordleMatch > 0.95:
        return yorVals.index(maxYordleMatch) + 2
    else:
        return 1

def rightClick():
    pyautogui.mouseDown(button='right')
    sleep(0.01)
    pyautogui.mouseUp(button='right')

def click():
    pyautogui.mouseDown()
    sleep(0.05)
    pyautogui.mouseUp()



def stageOneTwo():
    # Moving first unit on
    pyautogui.moveTo(x=bench_positions[0][0], y=bench_positions[0][1], duration=0.2)
    pyautogui.mouseDown()
    pyautogui.moveTo(x=hex_positions[2][0], y=hex_positions[2][1], duration=0.2)
    pyautogui.mouseUp()

    hex_positions[2][2] = checkYordle(2, hex_positions)

def stageOneThree():
    # Buying a second unit
    pyautogui.moveTo(x=565, y=1000, duration=0.2)
    click()

    # Moving on a unit
    pyautogui.moveTo(x=bench_positions[0][0], y=bench_positions[0][1], duration=0.2)
    pyautogui.mouseDown()
    pyautogui.moveTo(x=hex_positions[21][0], y=hex_positions[21][1], duration=0.2)
    pyautogui.mouseUp()

    hex_positions[21][2] = checkYordle(21, hex_positions)

def stageOneFour():
    # Buying a third unit
    pyautogui.moveTo(x=565, y=1000, duration=0.2)
    click()

    # Moving on a unit
    pyautogui.moveTo(x=bench_positions[0][0], y=bench_positions[0][1], duration=0.2)
    pyautogui.mouseDown()
    pyautogui.moveTo(x=hex_positions[26][0], y=hex_positions[26][1], duration=0.2)
    pyautogui.mouseUp()

    hex_positions[26][2] = checkYordle(26, hex_positions) # TODO set something back here, if it swaps w another yordle

def cycleBench():

    for i in range(9):
        currentYordle = checkYordle(i, bench_positions)

        bench_positions[i][2] = currentYordle

        if(Champions(currentYordle) == Champions.Something):
            sellUnit(i)

        elif (Champions(currentYordle) != Champions.Nothing):
            swapYordles(currentYordle, i)


def swapYordles(yordleType, benchSpot):
    if Champions(yordleType) == Champions.Poppy:
        if Champions(hex_positions[2][2]) != Champions.Poppy:
            pyautogui.moveTo(x=bench_positions[benchSpot][0], y=bench_positions[benchSpot][1], duration=0.2)
            pyautogui.mouseDown()
            pyautogui.moveTo(x=hex_positions[2][0], y=hex_positions[2][1], duration=0.2)
            pyautogui.mouseUp()

            hex_positions[2][2] = yordleType
    
    elif Champions(yordleType) == Champions.Ziggs:
        if Champions(hex_positions[21][2]) != Champions.Ziggs:
            pyautogui.moveTo(x=bench_positions[benchSpot][0], y=bench_positions[benchSpot][1], duration=0.2)
            pyautogui.mouseDown()
            pyautogui.moveTo(x=hex_positions[21][0], y=hex_positions[21][1], duration=0.2)
            pyautogui.mouseUp()

            hex_positions[21][2] = yordleType

    elif Champions(yordleType) == Champions.Lulu:
        if Champions(hex_positions[27][2]) != Champions.Lulu:
            pyautogui.moveTo(x=bench_positions[benchSpot][0], y=bench_positions[benchSpot][1], duration=0.2)
            pyautogui.mouseDown()
            pyautogui.moveTo(x=hex_positions[27][0], y=hex_positions[27][1], duration=0.2)
            pyautogui.mouseUp()

            hex_positions[27][2] = yordleType

    elif Champions(yordleType) == Champions.Tristana:
        if Champions(hex_positions[26][2]) != Champions.Tristana:
            pyautogui.moveTo(x=bench_positions[benchSpot][0], y=bench_positions[benchSpot][1], duration=0.2)
            pyautogui.mouseDown()
            pyautogui.moveTo(x=hex_positions[26][0], y=hex_positions[26][1], duration=0.2)
            pyautogui.mouseUp()

            hex_positions[26][2] = yordleType

    elif Champions(yordleType) == Champions.Heimerdinger:
        if Champions(hex_positions[22][2]) != Champions.Heimerdinger:
            pyautogui.moveTo(x=bench_positions[benchSpot][0], y=bench_positions[benchSpot][1], duration=0.2)
            pyautogui.mouseDown()
            pyautogui.moveTo(x=hex_positions[22][0], y=hex_positions[22][1], duration=0.2)
            pyautogui.mouseUp()

            hex_positions[22][2] = yordleType

    elif Champions(yordleType) == Champions.Vex:
        if Champions(hex_positions[4][2]) != Champions.Vex:
            pyautogui.moveTo(x=bench_positions[benchSpot][0], y=bench_positions[benchSpot][1], duration=0.2)
            pyautogui.mouseDown()
            pyautogui.moveTo(x=hex_positions[4][0], y=hex_positions[4][1], duration=0.2)
            pyautogui.mouseUp()

            hex_positions[4][2] = yordleType

def sellUnit(benchSpot):
    pyautogui.moveTo(x=bench_positions[benchSpot][0], y=bench_positions[benchSpot][1])
    pyautogui.mouseDown()
    pyautogui.moveTo(x=565, y=1000)
    pyautogui.mouseUp()

def level_up():
    pyautogui.moveTo(x=360, y=960)
    click()

def roll():
    pyautogui.moveTo(x=360, y=1040)
    click()

# Game Loop
while True:

    sleep(0.1)

    # Format stage in 10's, dash in 1's eg 2-3 is 23
    stageNumber = getStageNumber()

    # Checking if standard, PvE, or carousel
    gameMode = getGameMode()
    
    print(stageNumber)

    # YORDLE PURCHASING FROM NATURAL ROLL
    purchaseUnits()

    # LEVEL & GOLD INFORMATION

    gold = readGold()

    level = readLevel()

    if (gameMode == 'augment') :
        selectAugment()
        continue

    if (stageNumber > 20 and gameMode != 'carousel'):
        cycleBench()

    print(level)
    print(gold)
    print(gameMode)

    if singleExpBuy == 0 and gold > 14:
        level_up()

        singleExpBuy = singleExpBuy + 1


    # Level if below 6
    while (gold >= 54 and level < 6):
        level_up()

        gold = readGold()
        level = readLevel()
    
    # Roll if 6
    while (gold >= 52 and level == 6):
        purchaseUnits() 
        roll()

        gold = readGold()
        level = readLevel()

    # Skip to 8 (Janna and Veigar)
    if (gold >= 70 and level == 7):
        while (level < 8):
            level_up()

            level = readLevel()


    while (gold >= 12 and level >= 8):
        purchaseUnits()

        roll()

        gold = readGold()
        level = readLevel()


    if (stageNumber == 12):
        stageOneTwo()

    if (stageNumber == 13):
        stageOneThree()

    if (stageNumber == 14):
        stageOneFour()

    taunt()

    while stageNumber == getStageNumber():
        if (gameMode == 'pve' or gameMode == 'postpve'):
            orbPickups()

        purchaseUnits()
