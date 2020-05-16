import time

import MinecraftOCR
import numpy as np

from PIL import Image
from PIL import ImageGrab

print("waiting...")
time.sleep(5)
print("done waiting")
ocr = MinecraftOCR.OCR(Image.open('D:\\Python\\AnniScraper\\ascii.png'))
print(ocr.recognizeTeamHealth())
