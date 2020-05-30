import time

import MinecraftOCR
import constant
import helpers
import numpy as np

from multiprocessing import Process

from PIL import Image
from PIL import ImageGrab

# ocr = MinecraftOCR.OCR(Image.open('D:\\Python\\AnniScraper\\ascii.png'), 8, 8, 2)
ocr = MinecraftOCR.OCR(Image.open('D:\\Python\\AnniScraper\\font.png'), 8, 8, 2)


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

    loadedImage = np.swapaxes(np.asarray(image), 0, 1)
    # Figure out where the first line of health begins
    # y = 0
    # while not helpers.colorMatches(loadedImage[0, y], constant.TEAM_COLORS):
    # y += 1

    # FIXME
    scrapedText = ocr.processLoadedImage(helpers.Coordinate2D(0, 0), loadedImage, False, False)

    #print(convertToText(scrapedText))
    # Pull out each team's health values
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
    scrapingResults = ocr.processImage(image, False, True)

    if scrapingResults:
        scrapingResults = scrapingResults[0]

        # Find the team that was damaged by checking the color of the first character
        damagedTeam = constant.COLORS_DICT[tuple(scrapingResults[0].colors[0].tolist())]

        chaffCharsCount = len(damagedTeam) + constant.HIT_MESSAGE_CHAFF_CHARS
        # Find the team that did the damage by checking the  color of the first character of the player's name
        playerTeam = constant.COLORS_DICT[tuple(scrapingResults[chaffCharsCount].colors[0].tolist())]
        # Find the player's name
        player = scrapingResults[chaffCharsCount: len(scrapingResults)]
        playerName = ''
        for char in player:
            playerName += char.character

        return helpers.DamageDealt(playerName, playerTeam, damagedTeam)

    return helpers.DamageDealt(None, None, None)


def recognizeChat(image):
    image = image.crop(constant.CHAT_RECTANGLE)
    # image.save('chat.png', 'PNG')
    scrapingResults = ocr.processImage(image, True, True)
    return convertToText(scrapingResults)


def recognizePhase(image):
    image = image.crop(constant.PHASE_RECTANGLE)
    # image.save('phase.png', 'PNG')
    scrapingResults = ocr.processImage(image, False, True)
    return convertToText(scrapingResults)


img = Image.open("D:\\Python\\AnniScraper\\testfour.png")
print("waiting...")
#time.sleep(2)
print("done waiting")

a = 0
def collectData():
    startTime = time.perf_counter()

    #img = ImageGrab.grab()
    # print('ImageGrab took ' + str(time.perf_counter() - startTime))

    #nextTime = time.perf_counter()
    #print(recognizeTeamHealth(img))
    #print('recognizeTeamHealth took ' + str(time.perf_counter() - nextTime))

    #nextTime = time.perf_counter()
    #print(recognizeDamageDealer(img))
    #print('recognizeDamageDealer took ' + str(time.perf_counter() - nextTime))

    #nextTime = time.perf_counter()
    #print(recognizeChat(img))
    #print('recognizeChat took ' + str(time.perf_counter() - nextTime))

    #nextTime = time.perf_counter()
    #print(recognizePhase(img))
    #print('recognizePhase took ' + str(time.perf_counter() - nextTime))

    recognizeTeamHealth(img)
    recognizeDamageDealer(img)
    recognizeChat(img)
    recognizePhase(img)

    endTime = time.perf_counter()

    #print('Took ' + str(endTime - startTime) + ' to process')
    if endTime - startTime > 0.5:
        print("AAAAAAAAAAAAAAA")
        global a
        a += 1


# Run collectData once to make sure it is compiled before we profile it's speed
collectData()

totalStartTime = time.perf_counter()

for _ in range(100):
    startTime = time.perf_counter()
    collectData()
    processingTime = time.perf_counter() - startTime
    if processingTime < 0.5:
        time.sleep(0.5 - processingTime)

print('recognizeLetter called ' + str(ocr.recognizeLetterCalls) + ' times.')
print('recognizeLetter used ' + str(ocr.recognizeLetterChecks / ocr.recognizeLetterCalls) + ' checks average.')

print('Took ' + str(time.perf_counter() - totalStartTime) + ' of processing time')
print(a)
