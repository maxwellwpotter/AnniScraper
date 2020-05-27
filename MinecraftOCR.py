import numpy as np
from PIL import PyAccess
from PIL import Image
from PIL import ImageGrab
import time

import constant
import helpers


class OCR:
    __lineSpacing = 1
    __spaceLength = 4

    def __init__(self, alphabetImage: Image, charHeight: int, charWidth: int, dotSize: int):
        self.maxCharHeight = charHeight
        self.maxCharWidth = charWidth
        self.dotSize = dotSize

        # Figure out a way of telling each character apart
        # Create a matrix that will store for every coordinate all characters that have a pixel at there
        self.possibleCharsMatrix = [[[] for _ in range(self.maxCharHeight)] for _ in range(self.maxCharWidth)]

        # Dictionary to store how many dots wide every character is
        self.charLengths = {}

        # Load the image into an array for easier processing
        # This isn't the most efficient way to do this, but it should be fine for now.
        alphabetImgArr = alphabetImage.load()

        # For the given alphabet, figure out how to recognize each character.

        # For each character, loop through all of its pixels and if the pixel is present at a given (x, y), add
        # that letter to possibleCharsMatrix[x][y].
        # Also record for each character how many pixels wide it is.

        # Function to process the pixels of a given character
        # Takes a string representing the character and the coordinates of the top left of the character.
        def processCharacter(char: str, coords: helpers.Coordinate2D):
            lastColumnWithPixel = 0
            for x in range(0, self.maxCharWidth):

                for y in range(0, self.maxCharHeight):

                    currentX = coords.x + x
                    currentY = coords.y + y
                    if alphabetImgArr[currentX, currentY][3] != 0:
                        self.possibleCharsMatrix[x][y].append(char)
                        lastColumnWithPixel = x + 1

            self.charLengths[char] = lastColumnWithPixel

        # Process all of the characters
        imageWidth, imageHeight = alphabetImage.size
        for i in range(len(constant.ALPHABET)):
            # Calculate the coordinates for the next character
            currentCoords = helpers.Coordinate2D((i * self.maxCharWidth % imageWidth),
                                                 (i * self.maxCharWidth // imageWidth) * self.maxCharHeight)

            # Process the character at these coordinates
            processCharacter(constant.ALPHABET[i], currentCoords)

        # Set the length of the space character
        self.charLengths[' '] = self.__spaceLength

    def recognizeLetter(self, loadedImage, coords: helpers.Coordinate2D):
        possibleChars = constant.ALPHABET
        colors = constant.COLORS

        # FIXME: This will have a potential error as if the letter is recognized on pixel (7, 7),
        # FIXME: there will be no chance to return it.

        # Iterate through every pixel in the character until we know exactly which character it is.
        for x in range(8):
            for y in range(8):
                # print("Possible characters:")
                # print(possibleChars)
                # print("Current colors: " + str(colors))
                # print("Current (x, y): " + str((x, y)))
                # print(str(len(possibleChars)) + " possible characters remaining.")
                # If there is only 1 possible character remaining, the input must be that character.
                if len(possibleChars) == 1:
                    # print("The answer is:" + str(possibleChars))
                    return helpers.RecognizedCharacter(possibleChars[0], colors)
                # If no character could be recognized, return the empty string
                elif len(possibleChars) == 0:
                    # print("Could not recognize character at " + str((coords[0], coords[1])))
                    return helpers.RecognizedCharacter('', None)
                else:
                    currentX = coords.x + x * self.dotSize
                    currentY = coords.y + y * self.dotSize
                    # print(currentX)
                    # print(currentY)
                    if helpers.colorMatches(loadedImage[currentX, currentY], colors):
                        colors = [loadedImage[currentX, currentY]]
                        possibleChars = np.intersect1d(possibleChars, self.possibleCharsMatrix[x][y])
                    else:  # There is no pixel of the colors we care about at the current coordinates
                        possibleChars = np.setdiff1d(possibleChars, self.possibleCharsMatrix[x][y])

        if len(possibleChars) == 1:
            # ("The answer is:")
            # print(possibleChars)
            return helpers.RecognizedCharacter(possibleChars[0], colors)
        else:  # If no character could be recognized, return the empty string
            # print("Could not recognize character at " + str((coords[0], coords[1])))
            return helpers.RecognizedCharacter('', None)

    def processLoadedImage(self, coords: helpers.Coordinate2D, loadedImage: PyAccess, endEarly: bool = True):
        imageWidth, imageHeight, bandCount = np.shape(loadedImage)
        text = []
        currentLine = []

        emptyColumnCount = 0
        while coords.y < imageHeight:
            # print(coords)
            nextChar = self.recognizeLetter(loadedImage, coords)
            # print(nextChar)
            # If the next char couldn't be recognized or we think it is a space, move over 1 column because there
            # might be some wack text formatting.
            if nextChar.character == ' ' or nextChar.character == '':
                emptyColumnCount += 1
                coords.x += self.dotSize
            else:  # Otherwise, we recognized the character
                # Add however many spaces we need to.
                # If there is no text in the line yet, we don't add any spaces.
                if len(currentLine) != 0:
                    for _ in range(emptyColumnCount // self.charLengths[' ']):
                        # print("Added space")
                        currentLine.append(helpers.RecognizedCharacter(' ', []))
                emptyColumnCount = 0

                currentLine.append(nextChar)
                coords.x += (self.charLengths[nextChar.character] + 1) * self.dotSize

            if coords.x >= imageWidth or (len(currentLine) == 0 and emptyColumnCount > 15) or (endEarly and emptyColumnCount > 10):
                coords.y += (self.dotSize * (self.maxCharHeight + self.__lineSpacing))
                coords.x = 0
                if len(currentLine) != 0:
                    text.append(currentLine)
                currentLine = []

        return text

    def processImage(self, image: Image, endEarly: bool = True):
        imgWidth, imgHeight = image.size
        loadedImage = np.swapaxes(np.asarray(image), 0, 1)
        coords = helpers.Coordinate2D(0, 0)
        return self.processLoadedImage(coords, loadedImage, endEarly)

# a = OCR(Image.open('D:\\Python\\AnniScraper\\ascii.png'))
# img = Image.open('D:\\Python\\AnniScraper\\score.png')
# print(a.processImage(img))
