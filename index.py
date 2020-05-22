import time

import MinecraftOCR
import constant
import numpy as np

from PIL import Image
from PIL import ImageGrab

print("waiting...")
time.sleep(5)
print("done waiting")
ocr = MinecraftOCR.OCR(Image.open('D:\\Python\\AnniScraper\\ascii.png'))


# Returns an array storing the health of each team formatted as [Blue, Green, Red, Yellow]
def recognizeTeamHealth():
    img = ImageGrab.grab().crop(constant.TEAM_HEALTH_RECTANGLE)
    img.save('score.png', 'PNG')
    scrapedText = ocr.processImage(img)

    teamHealths = [0] * 4
    switchCases = {
        'B': 0,
        'G': 1,
        'R': 2,
        'Y': 3
    }
    for team in scrapedText:
        healthVal = int(team[len(team) - 2] + team[len(team) - 1])
        teamHealths[switchCases[team[0]]] = healthVal
        
    return teamHealths


print(recognizeTeamHealth())