from typing import Tuple

import constant

import numpy as np
from PIL import Image
from PIL import ImageGrab


class OCR:

    def __init__(self, alphabetImage):

        # For the given alphabet, figure out how to recognize each character.

        # TODO: Figure out how to make dynamic
        self.maxCharHeight = 8
        self.maxCharWidth = 8
        self.dotSize = 2

        # Create a matrix that will store for each coordinate all characters that have a pixel at that coordinate
        self.possibleCharsMatrix = [[[] for _ in range(self.maxCharHeight)] for _ in range(self.maxCharWidth)]

        # Create a dictionary that will store the how many pixels long each character is.
        self.charLength = {}

        # Load the image into an array for easier processing
        # This isn't the most efficient way to do this, but it should be fine for now.
        alphabetImgArr = alphabetImage.load()

        # Begin processing the alphabet.
        # For each character, loop through all of its pixels and if the pixel is present at a given (x, y), add
        # that letter to possibleCharsMatrix[x][y].
        # Also record for each character how many pixels wide it is.

        # Function to process the pixels of a given character
        # Takes a string representing the character and the coordinates of the top left of the character.
        def processCharacter(char: str, coords: Tuple[int, int]):
            lastColumnWithPixel = 0
            for x in range(0, self.maxCharWidth):
                for y in range(0, self.maxCharHeight):
                    currentX = coords[0] + x
                    currentY = coords[1] + y
                    if alphabetImgArr[currentX, currentY][3] != 0:
                        self.possibleCharsMatrix[x][y].append(char)
                        lastColumnWithPixel = y

            self.charLength[char] = lastColumnWithPixel

        # Process all of the characters
        imageWidth, imageHeight = alphabetImage.size
        for index in range(len(constant.ALPHABET)):
            # Calculate the coordinates for the next character
            currentCoords = ((index * self.maxCharWidth % imageWidth),
                             (index * self.maxCharWidth // imageWidth) * self.maxCharHeight)
            # Process this character
            processCharacter(constant.ALPHABET[index], currentCoords)

    def recognizeLetter(self, imageArr, coords):
        chars = constant.ALPHABET
        colors = constant.COLORS
        # This will have a potential error as if the letter is recognized on pixel (7, 7),
        # there will be no chance to return it.
        for x in range(8):
            for y in range(8):
                print((x, y))
                if len(chars) == 1:
                    print("The answer is:")
                    print(chars)
                    return chars[0]
                elif len(chars) == 0:
                    print("0 possible characters remaining")
                else:
                    # times 2 to account for the size of each dot
                    if imageArr[coords[0] + x * 2, coords[1] + y * 2][3] != 0:
                        # if len(colors) != 1:
                        # figure out how to match colors here
                        print("possible letters for this pixel are:")
                        print(self.possibleCharsMatrix[x][y])
                        chars = np.intersect1d(chars, self.possibleCharsMatrix[x][y])
                        print("intersected")
                        print(chars)
                    else:
                        print("possible letters for this pixel are:")
                        print(self.possibleCharsMatrix[x][y])
                        chars = np.setdiff1d(chars, self.possibleCharsMatrix[x][y])
                        print("set diffed")
                        print(chars)

        print("Checked all pixels, and idk what letter it is.")

    def processImage(self, imageArr):
        coords = (0, 0)
        chars = []
        # for y in range(0, len(imageArr[0], 9*2):
        chars.append(self.recognizeLetter(imageArr, coords))
        chars.append(self.recognizeLetter(imageArr, (6 * 2, 0)))
        return chars

    def recognizeTeamHealth(self):
        img = ImageGrab.grab().crop(constant.TEAM_HEALTH_RECTANGLE)
        img.save('score.png', 'PNG')

    # def recognizeDamage(self):
    # TODO

    def __scanForText(self, image, colors):
        imgArr = image.load()
        # The current coordinates, saved as (x, y)
        coords = (0, 0)

        # Every character will be 7 dots tall, and between 1 and 5 dots wide.
        # There is a 1 dot  gap between every character, and a space is 3 dots wide.

        # Scan this column of the input,


a = OCR(Image.open('D:\\Python\\AnniScraper\\ascii.png'))
img = Image.open('D:\\Python\\AnniScraper\\test.png').load()
print(a.recognizeLetter(img, (0, 0)))
