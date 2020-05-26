import time

import MinecraftOCR
import constant
import numpy as np
from recordclass import recordclass

from PIL import Image
from PIL import ImageGrab

# print("waiting...")
# time.sleep(5)
# print("done waiting")
ocr = MinecraftOCR.OCR(Image.open('D:\\Python\\AnniScraper\\ascii.png'), 8, 8, 2)


def convertToText(scrapedText):
    processedText = []
    for line in scrapedText:
        processedLine = []
        for char in line:
            processedLine.append(char.character)
        processedText.append(processedLine)
    return processedText


# Returns an array storing the health of each team formatted as [Blue, Green, Red, Yellow]
def recognizeTeamHealth(image):
    image = image.crop(constant.TEAM_HEALTH_RECTANGLE)
    image.save('score.png', 'PNG')
    scrapedText = ocr.processImage(image)

    teamHealths = [0] * 4
    switchCases = {
        'B': 0,
        'G': 1,
        'R': 2,
        'Y': 3
    }
    print(convertToText(scrapedText))
    for line in scrapedText:
        healthVal = int(line[len(line) - 2].character + line[len(line) - 1].character)
        teamHealths[switchCases[line[0].character]] = healthVal

    return teamHealths


def recognizeDamageDealer(image):
    image = image.crop(constant.HIT_NOTIFICATION_RECTANGLE)
    image.save('hit.png', 'PNG')
    scrapingResults = ocr.processImage(image)
    scrapedText = convertToText(scrapingResults)[0]
    print(scrapedText)

    DamageDealt = recordclass('DamageDealt', 'player playerTeam damagedNexus')

    # Find the team that was damaged by checking the color of the first character
    damagedTeam = constant.COLORS_DICT[scrapingResults[0][0].colors[0]]

    chaffCharsCount = len(damagedTeam) + constant.HIT_MESSAGE_CHAFF_CHARS
    # Find the team that did the damage by checking the  color of the first character of the player's name
    playerTeam = constant.COLORS_DICT[scrapingResults[0][chaffCharsCount].colors[0]]
    # Find the player's name
    player = ''.join(scrapedText[chaffCharsCount: len(scrapedText)])\

    return DamageDealt(player, playerTeam, damagedTeam)


img = Image.open("D:\\Python\\AnniScraper\\test.png")

print(recognizeTeamHealth(img))
print(recognizeDamageDealer(img))
