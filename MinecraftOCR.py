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
        # The number of dots between lines
        self.lineSpacing = 1
        self.dotSize = 2

        # Create a matrix that will store for each coordinate all characters that have a pixel at that coordinate
        self.possibleCharsMatrix = [[[] for _ in range(self.maxCharHeight)] for _ in range(self.maxCharWidth)]

        # Create a dictionary that will store the how many pixels long each character is.
        self.charLengths = {}

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
                        lastColumnWithPixel = x + 1

            self.charLengths[char] = lastColumnWithPixel

        # Process all of the characters
        imageWidth, imageHeight = alphabetImage.size
        for index in range(len(constant.ALPHABET)):
            # Calculate the coordinates for the next character
            currentCoords = ((index * self.maxCharWidth % imageWidth),
                             (index * self.maxCharWidth // imageWidth) * self.maxCharHeight)
            # Process this character
            processCharacter(constant.ALPHABET[index], currentCoords)

        # Set the length of the space character
        self.charLengths[' '] = 4

    def recognizeLetter(self, imageArr, coords):
        print(coords)
        possibleChars = constant.ALPHABET
        colors = constant.COLORS

        # FIXME: This will have a potential error as if the letter is recognized on pixel (7, 7),
        # FIXME: there will be no chance to return it.

        # Define a function that returns true if the pixel matches on of the colors in colorArr
        def colorMatches(pixel, colorArr):
            print(pixel)
            for color in colorArr:
                if pixel == color:
                    return True
            print("No color match")
            return False

        # Iterate through every pixel in the character until we know exactly which character this is.
        for x in range(8):
            for y in range(8):
                #print("Current (x, y): " + str((x, y)))
                #print(str(len(possibleChars)) + " possible characters remaining.")
                # If there is only 1 possible character remaining, the input must be that character.
                if len(possibleChars) == 0:
                    print("Could not recognize character at " + str((coords[0], coords[1])))
                    return ' '
                elif len(possibleChars) == 1:
                    print("The answer is:")
                    print(possibleChars)
                    return possibleChars[0]
                else:
                    currentX = coords[0] + x * self.dotSize
                    currentY = coords[1] + y * self.dotSize
                    if colorMatches(imageArr[currentX, currentY], colors):
                        # NOTE: If necessary, this can be optimized by reducing the size of the color array to
                        # just the color of this pixel.
                        #print("possible letters for this pixel are:")
                        #print(self.possibleCharsMatrix[x][y])
                        possibleChars = np.intersect1d(possibleChars, self.possibleCharsMatrix[x][y])
                        #print("intersected")
                        #print(possibleChars)
                    else:  # There is no pixel of the colors we care about at the current coordinates
                        #print("possible letters for this pixel are:")
                        #print(self.possibleCharsMatrix[x][y])
                        possibleChars = np.setdiff1d(possibleChars, self.possibleCharsMatrix[x][y])
                        #print("set diffed")
                        #print(possibleChars)

        print("We got out here, and this shouldn't happen.")

    def processImage(self, image):
        imgWidth, imgHeight = image.size
        imageArr = image.load()

        coords = [0, 0]
        text = []
        currentLine = []

        emptyColumnCount = 0
        while coords[1] < imgHeight:
            nextChar = self.recognizeLetter(imageArr, coords)
            # If the next char couldn't be recognized or we think it is a space, move over 1 column because there might
            # just be some wack text formatting.
            if nextChar == ' ':
                emptyColumnCount += 1
                coords[0] += self.dotSize
            else:
                # Add however many spaces we need to.
                for _ in range(emptyColumnCount // self.charLengths[' ']):
                    currentLine.append(' ')
                emptyColumnCount = 0

                currentLine.append(nextChar)
                coords[0] = coords[0] + (self.charLengths[nextChar] + 1) * self.dotSize
                if coords[0] >= imgWidth:
                    coords[1] += (coords[0] // imgWidth) * (self.dotSize * (self.maxCharHeight + self.lineSpacing))
                    coords[0] = 0
                    text.append(currentLine)
                    currentLine = []

        return text



    # def recognizeDamage(self):
    # TODO

    def __scanForText(self, image, colors):
        imgArr = image.load()
        # The current coordinates, saved as (x, y)
        coords = (0, 0)

        # Every character will be 7 dots tall, and between 1 and 5 dots wide.
        # There is a 1 dot  gap between every character, and a space is 3 dots wide.

        # Scan this column of the input,


#a = OCR(Image.open('D:\\Python\\AnniScraper\\ascii.png'))
#img = Image.open('D:\\Python\\AnniScraper\\score.png')
#print(a.processImage(img))
