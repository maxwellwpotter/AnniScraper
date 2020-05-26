import time

import MinecraftOCR
import constant
import helpers
import numpy as np
from recordclass import recordclass

from PIL import Image
from PIL import ImageGrab

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
    # image.save('score.png', 'PNG')

    # Load the image, and figure out where the first line of health is
    imgWidth, imgHeight = image.size
    loadedImage = image.load()
    y = 0
    while not helpers.colorMatches(loadedImage[0, y], constant.TEAM_COLORS):
        y += 1

    scrapedText = ocr.processLoadedImage(helpers.Coordinate2D(0, y), imgWidth, imgHeight, loadedImage)

    teamHealths = [0] * 4
    switchCases = {
        'B': 0,
        'G': 1,
        'R': 2,
        'Y': 3
    }

    for line in scrapedText:
        healthVal = int(line[len(line) - 2].character + line[len(line) - 1].character)
        teamHealths[switchCases[line[0].character]] = healthVal

    return teamHealths


def recognizeDamageDealer(image):
    image = image.crop(constant.HIT_NOTIFICATION_RECTANGLE)
    # image.save('hit.png', 'PNG')
    scrapingResults = ocr.processImage(image)

    DamageDealt = recordclass('DamageDealt', 'player playerTeam damagedNexus')
    if scrapingResults:
        scrapedText = convertToText(scrapingResults)[0]

        if len(scrapedText) != 0:
            # Find the team that was damaged by checking the color of the first character
            damagedTeam = constant.COLORS_DICT[scrapingResults[0][0].colors[0]]

            chaffCharsCount = len(damagedTeam) + constant.HIT_MESSAGE_CHAFF_CHARS
            # Find the team that did the damage by checking the  color of the first character of the player's name
            playerTeam = constant.COLORS_DICT[scrapingResults[0][chaffCharsCount].colors[0]]
            # Find the player's name
            player = ''.join(scrapedText[chaffCharsCount: len(scrapedText)])

            return DamageDealt(player, playerTeam, damagedTeam)

    return DamageDealt(None, None, None)


def recognizeChat(image):
    image = image.crop(constant.CHAT_RECTANGLE)
    # image.save('chat.png', 'PNG')
    scrapingResults = ocr.processImage(image)
    return convertToText(scrapingResults)


def recognizePhase(image):
    image = image.crop(constant.PHASE_RECTANGLE)
    scrapingResults = ocr.processImage(image)
    return convertToText(scrapingResults)


img = Image.open("D:\\Python\\AnniScraper\\testtwo.png")
print("waiting...")
# time.sleep(5)
print("done waiting")

while True:
    startTime = time.perf_counter()

    # img = ImageGrab.grab()
    # print('ImageGrab took ' + str(time.perf_counter() - startTime))

    # nextTime = time.perf_counter()
    print(recognizeTeamHealth(img))
    # print('recognizeTeamHealth took ' + str(time.perf_counter() - nextTime))

    # nextTime = time.perf_counter()
    print(recognizeDamageDealer(img))
    # print('recognizeDamageDealer took ' + str(time.perf_counter() - nextTime))

    # nextTime = time.perf_counter()
    print(recognizeChat(img))
    # print('recognizeChat took ' + str(time.perf_counter() - nextTime))

    # nextTime = time.perf_counter()
    print(recognizePhase(img))
    # print('recognizePhase took ' + str(time.perf_counter() - nextTime))

    endTime = time.perf_counter()

    print('Took ' + str(endTime - startTime) + ' to process')
    time.sleep(0.5)
    break
