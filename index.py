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


def recognizeTeamHealth():
    img = ImageGrab.grab().crop(constant.TEAM_HEALTH_RECTANGLE)
    img.save('score.png', 'PNG')
    return ocr.processImage(img)


print(recognizeTeamHealth())