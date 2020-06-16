import numpy as np
from PIL import PyAccess
from PIL import Image
from PIL import ImageGrab
import time

import constant


def colorMatches(pixel, colorArr):
    # print("Pixel color: " + str(pixel))
    for color in colorArr:
        if pixel[0] == color[0] and pixel[1] == color[1] and pixel[2] == color[2]:
            return True
    # print("No color match")
    return False


class OCR:
    loadedImage = np.array([[]])
    memoizedKillLog = []
    kills = []
    chatRead = False
    bossKill = None
    bossKillTime = time.perf_counter() - 300
    recognizeKillsRepeatsBeforeTermination = 1

    def __init__(self, alphabetImage: Image, charHeight: int, charWidth: int, dotSize: int,
                 lineSpacing: int = 1, spaceLength: int = 4):
        self.maxCharHeight = charHeight
        self.maxCharWidth = charWidth
        self.dotSize = dotSize
        self.lineSpacing = lineSpacing

        # Figure out a way of telling each character apart
        # Create a matrix that will store for every coordinate all characters that have a pixel at there
        self.possibleCharsMatrix = np.zeros((self.maxCharHeight, self.maxCharWidth, len(constant.ALPHABET)), dtype=bool)

        # Dictionary to store how many dots wide every character is
        self.charLengths = {}

        # Load the image into an array for easier processing
        # This isn't the most efficient way to do this, but it should be fine for now.
        alphabetImgArr = np.swapaxes(np.asarray(alphabetImage), 0, 1)

        # Figure out how to recognize each character

        # For each character, loop through all of its pixels and if the pixel is present at a given (x, y), add
        # that letter to possibleCharsMatrix[x][y].
        # Also record for each character how many pixels wide it is.

        # Function to process the pixels of a given character
        # Takes a string representing the character and the coordinates of the top left of the character.
        def processCharacter(char: str, globalX, globalY):
            alphabetIndex = constant.ALPHABET_INDICES[char]
            lastColumnWithPixel = 0
            for x in range(self.maxCharWidth):

                for y in range(self.maxCharHeight):
                    currentX = globalX + x
                    currentY = globalY + y
                    if alphabetImgArr[currentX, currentY, 3] != 0:
                        self.possibleCharsMatrix[x, y, alphabetIndex] = True
                        lastColumnWithPixel = x + 1

            self.charLengths[char] = lastColumnWithPixel

        # Process all of the characters
        imageWidth, imageHeight = alphabetImage.size
        for i in range(len(constant.ALPHABET)):
            # Calculate the coordinates for the next character
            currentCoords = ((i * self.maxCharWidth % imageWidth),
                                                 (i * self.maxCharWidth // imageWidth) * self.maxCharHeight)

            # Process the character at these coordinates
            processCharacter(constant.ALPHABET[i], *currentCoords)

        # Set the length of the space character
        self.charLengths[' '] = spaceLength

    def loadImage(self, image: Image):
        self.loadedImage = np.swapaxes(np.asarray(image), 0, 1)
        self.chatRead = False
        self.bossKill = (None, None)

    def recognizeCharacter(self, globalX: int, globalY: int, colors=constant.COLORS):
        dotSize = self.dotSize

        possibleChars = constant.ALPHABET
        # Iterate through every pixel in the character until we know exactly which character it is.
        for dx in range(self.maxCharWidth):
            for dy in range(self.maxCharHeight):
                # print("Current (dx, dy): " + str((dx, dy)))
                # print("Possible characters:")
                # print(possibleChars)
                # print(self.possibleCharsMatrix[dx, dy])
                # print("Current colors: " + str(colors))
                # print("Current (x, y): " + str((x, y)))
                # print(str(len(possibleChars)) + " possible characters remaining.")

                # Define a function to give calculate the new possible chars after looking at this pixel
                def findNewPossibleChars():
                    newPossibleChars = np.empty(len(possibleChars), dtype=str)
                    nextIndex = 0
                    for c in possibleChars:
                        if pixelPresent == self.possibleCharsMatrix[dx, dy, constant.ALPHABET_INDICES[c]]:
                            newPossibleChars[nextIndex] = c
                            nextIndex += 1
                    return newPossibleChars[:nextIndex]

                # Check to see if a pixel is present at the current location
                currentX = globalX + dx * dotSize
                currentY = globalY + dy * dotSize
                pixelPresent = colorMatches(self.loadedImage[currentX, currentY], colors)
                if pixelPresent and len(colors) > 1:
                    colors = [self.loadedImage[currentX, currentY]]

                # Update the set of possible characters
                possibleChars = findNewPossibleChars()

                # Then, if there is only 1 possible character remaining, the input must be that character.
                if len(possibleChars) == 1:
                    # print("The answer is:" + str(possibleChars))
                    return helpers.RecognizedCharacter(possibleChars[0], colors)
                # If no character could be recognized, return the empty string
                elif len(possibleChars) == 0:
                    # print("Could not recognize character at " + str((x, y)))
                    return helpers.RecognizedCharacter('', None)

        print("We shouldn't be here!")

    def readName(self, globalX: int, globalY: int, color):
        name = ''
        nameLength = 0
        while nameLength < 16:
            nextCharacter = self.recognizeCharacter(globalX, globalY, [color]).character
            # If nextCharacter is an invalid character for a name, then we are done.
            if nextCharacter == '(' or nextCharacter == ' ' or nextCharacter == '':
                break
            name += nextCharacter
            nameLength += 1
            globalX += (self.charLengths[nextCharacter] + 1) * self.dotSize

        return name, (globalX, globalY)

    def readClass(self, globalX: int, globalY: int, color):
        classAcronym = ''
        classAcronymLength = 0
        for _ in range(3):
            nextCharacter = self.recognizeCharacter(globalX, globalY, [color]).character
            classAcronym += nextCharacter
            classAcronymLength += 1
            globalX += (self.charLengths[nextCharacter] + 1) * self.dotSize

        return classAcronym, (globalX, globalY)

    def recognizeHealth(self):
        # Read in all of the health values, then match every health value with the team that has it.

        # First, find where the nexus healths begin
        currentCoords = constant.TEAM_HEALTH_LOCATION
        while not colorMatches(self.loadedImage[currentCoords], [constant.RED, constant.WHITE]):
            currentCoords = (currentCoords[0], currentCoords[1] + self.dotSize)
        # Shift currentCoords left 2 pixels so it lines up with the tens digit.

        # Then, read in every nexus health, recording our coordinates each time
        currentRank = 0
        healthValues = [0, 0, 0, 0]
        rankCoordinates = []
        while colorMatches(self.loadedImage[currentCoords], [constant.RED, constant.WHITE]):
            # Record our current coordinates
            rankCoordinates.append((currentCoords[0] - 8, currentCoords[1]))

            # Read in the health at our current coordinates
            healthTens = self.recognizeCharacter(currentCoords[0] - 4, currentCoords[1], [constant.RED]).character
            healthOnes = self.recognizeCharacter(*currentCoords, colors=[constant.RED]).character
            healthValues[currentRank] = healthTens + healthOnes
            currentRank += 1

            # Update our coordinates to the next line of health
            currentCoords = (currentCoords[0], currentCoords[1] + (self.maxCharHeight + self.lineSpacing) * self.dotSize)

        # Finally, match up each health value to its team.
        teamHealths = [0, 0, 0, 0]
        switchCases = {
            'Blue': 0,
            'Green': 1,
            'Red': 2,
            'Yellow': 3
        }
        for i in range(len(rankCoordinates)):
            currentCoords = rankCoordinates[i]
            # Go left from the coordinates until we run into a pixel of one of the team's colors.
            while not colorMatches(self.loadedImage[currentCoords], constant.HEALTH_COLORS):
                currentCoords = (currentCoords[0] - self.dotSize, currentCoords[1])

            team = ''
            if colorMatches(self.loadedImage[currentCoords], [constant.WHITE]):
                # If the color is white, we will have to read the name of the team.
                # Shift currentCoords left past ' Nexus:'
                currentCoords = (currentCoords[0] - 16 * self.dotSize, currentCoords[1])
                # Move currentCoords left until we stop seeing characters
                while colorMatches(self.loadedImage[currentCoords], [constant.WHITE]):
                    currentCoords = (currentCoords[0] - 2 * self.dotSize, currentCoords[1])
                # Then move currentCoords back left to put it back on the nexus name
                currentCoords = (currentCoords[0] + 2 * self.dotSize, currentCoords[1])
                # We are throwing away the coords return value
                team, coords = self.readName(*currentCoords, color=constant.WHITE)
            else:
                team = constant.COLORS_DICT[tuple(self.loadedImage[currentCoords])]
            teamHealths[switchCases[team]] = healthValues[i]

        return teamHealths

    def recognizeDamage(self):
        # Read in the team who was damaged, the team who dealt the damage, and the player who dealt the damage

        # Figure out where the damage message begins, if it even exists
        currentCoords = constant.DAMAGE_LOCATION
        endLocation = constant.DAMAGE_END_LOCATION
        while currentCoords[0] < endLocation[0] and \
                not colorMatches(self.loadedImage[currentCoords], constant.TEAM_COLORS):
            currentCoords = (currentCoords[0] + self.dotSize, currentCoords[1])

        if currentCoords[0] >= endLocation[0]:
            return None, None, None

        # Find which team was damaged.
        damagedTeam = constant.COLORS_DICT[tuple(self.loadedImage[currentCoords])]

        # Find the team and player which dealt the damage.
        # First, we need to find where in the message the damaging team is.
        currentCoords = constant.DAMAGE_MID_LOCATION
        while not colorMatches(self.loadedImage[currentCoords], constant.TEAM_COLORS):
            currentCoords = (currentCoords[0] + self.dotSize, currentCoords[1])

        damagingTeamColor = tuple(self.loadedImage[currentCoords])
        damagingTeam = constant.COLORS_DICT[damagingTeamColor]

        # Then, read in the name of whoever dealt the damage. Throw away the coordinates
        playerName, coords = self.readName(*currentCoords, color=damagingTeamColor)

        return playerName, damagingTeam, damagedTeam

    def readChat(self):
        startLocation = constant.CHAT_START_LOCATION
        checkForRepeats = len(self.memoizedKillLog) >= self.recognizeKillsRepeatsBeforeTermination
        # Move currentLineStart one line below startLocation, so that on the first iteration it gets moved up to
        # the correct place.
        currentLineStart = (startLocation[0], startLocation[1] + (self.maxCharHeight + self.lineSpacing) * self.dotSize)
        kills = []

        # March through the chat log bottom up, stopping once we recognize recognizeKillsRepeatsBeforeTermination
        # repeated lines
        repeatsCount = 0

        while repeatsCount < self.recognizeKillsRepeatsBeforeTermination and \
                currentLineStart[1] > constant.CHAT_STOP_LOCATION[0]:
            # Shift currentLineStart up to the correct position.
            currentLineStart = (currentLineStart[0], currentLineStart[1] - (self.maxCharHeight + self.lineSpacing) * self.dotSize)

            # First, find the color of the first letter of the line.
            killerColor = tuple(self.loadedImage[currentLineStart])
            # If this colors is not one of the team colors, we don't care about the line unless it is a boss kill
            if not colorMatches(killerColor, constant.TEAM_COLORS):
                if colorMatches(killerColor, [constant.GOLD]):
                    # Read in the first character so we can figure out which boss this was
                    firstCharacter = self.recognizeCharacter(*currentLineStart, colors=[constant.GOLD]).character
                    boss = None
                    if firstCharacter == 'T':
                        boss = 'Wither'
                    elif firstCharacter == 'C':
                        boss = 'Celariel'
                    elif firstCharacter == 'F':
                        boss = 'Firwen'

                    if boss is not None and time.perf_counter() - self.bossKillTime  >= 300:
                        # Scan the line until we hit a character of one of the team colors
                        currentCoords = currentLineStart
                        while currentCoords[0] < constant.CHAT_STOP_LOCATION[0] and \
                                not colorMatches(self.loadedImage[currentCoords], constant.TEAM_COLORS):
                            currentCoords = (currentCoords[0] + self.dotSize, currentCoords[1])

                        team = constant.COLORS_DICT[tuple(self.loadedImage[currentCoords])]

                        self.bossKill = (boss, team)
                        self.bossKillTime = time.perf_counter()
                continue

            # Find the name and class of the killer
            killerName, currentCoords = self.readName(*currentLineStart, color=killerColor)
            # Verify that the next character is a '('
            if self.recognizeCharacter(*currentCoords, colors=[killerColor]).character != '(':
                continue
            # Shift currentCoords over one '(' character.
            currentCoords = (currentCoords[0] + (self.charLengths['('] + 1) * self.dotSize, currentCoords[1])
            killerClass, currentCoords = self.readClass(*currentCoords, color=killerColor)

            # Then, find how the kill happened.
            # Shift currentCoords over one '(' and one ' ' character.
            currentCoords = (currentCoords[0] + 6 * self.dotSize, currentCoords[1])
            meleeKill = True
            nextCharacter = self.recognizeCharacter(*currentCoords, colors=[constant.GRAY]).character
            if nextCharacter == 's':
                meleeKill = False
                # Either way, move currentCoords over the appropriate amount
                currentCoords = (currentCoords[0] + 12 * self.dotSize, currentCoords[1])
            else:
                currentCoords = (currentCoords[0] + 16 * self.dotSize, currentCoords[1])

            # Then, find the killer's team, name, and class.
            killedColor = tuple(self.loadedImage[currentCoords])
            killedName, currentCoords = self.readName(*currentCoords, color=killedColor)
            # Shift currentCoords over one '(' character.
            currentCoords = (currentCoords[0] + (self.charLengths['('] + 1) * self.dotSize, currentCoords[1])
            killedClass, currentCoords = self.readClass(*currentCoords, color=killedColor)

            # Figure out if this kill happened while attacking or defending a nexus.
            # Shift currentCoords over one '(' and one ' ' character
            currentCoords = (currentCoords[0] + 6 * self.dotSize, currentCoords[1])
            attackingNexus = None
            nextCharacter = self.recognizeCharacter(*currentCoords, colors=[constant.GRAY]).character
            # Either way, shift currentCoords over the appropriate amount.
            if nextCharacter == 'a':
                attackingNexus = True
                currentCoords = (currentCoords[0] + 22 * self.dotSize, currentCoords[1])
            elif nextCharacter == 'd':
                attackingNexus = False
                currentCoords = (currentCoords[0] + 22 * self.dotSize, currentCoords[1])

            nexusColor = None
            if attackingNexus is not None:
                nexusColor = constant.COLORS_DICT[tuple(self.loadedImage[currentCoords])]

            print(currentCoords)
            # Finally, compile all of this data into an array, and jam it into the kills array.
            result = [killerName, killerClass, constant.COLORS_DICT[killerColor], meleeKill,
                      killedName, killedClass, constant.COLORS_DICT[killedColor], attackingNexus, nexusColor]
            kills.insert(0, result)

            if checkForRepeats and result == self.memoizedKillLog[len(self.memoizedKillLog) - 1 - repeatsCount]:
                repeatsCount += 1
            else:
                repeatsCount = 0

        self.memoizedKillLog = kills
        if checkForRepeats:
            self.kills = kills[self.recognizeKillsRepeatsBeforeTermination:]
        else:
            self.kills = kills
        self.chatRead = True

    def recognizeKills(self):
        if not self.chatRead:
            self.readChat()

        return self.kills

    def recognizeBossKill(self):
        if not self.chatRead:
            self.readChat()

        return self.bossKill

    def recognizePhase(self):
        # Move currentCoords over until we hit a pixel.
        currentCoords = constant.PHASE_START_LOCATION
        while not colorMatches(self.loadedImage[currentCoords], [constant.WHITE]):
            if colorMatches(self.loadedImage[currentCoords], [constant.RED]):
                return None, None
            currentCoords = (currentCoords[0] + self.dotSize, currentCoords[1])

        # Shift currentCoords over the length of 'Phase ' (including the space at the end).
        currentCoords = (currentCoords[0] + 14 * self.dotSize, currentCoords[1])

        # Read the phase.
        phase = self.recognizeCharacter(*currentCoords, colors=[constant.WHITE]).character

        # Shift currentCoords over the length of ' - '.
        currentCoords = (currentCoords[0] + 12 * self.dotSize, currentCoords[1])

        # Read the time.
        # Read in all the characters and put them into an array.
        timeArr = []
        nextCharacter = self.recognizeCharacter(*currentCoords, colors=[constant.WHITE]).character
        while nextCharacter != ' ' and nextCharacter != '':
            timeArr.append(nextCharacter)
            currentCoords = (currentCoords[0] + (self.charLengths[nextCharacter] + 1) * self.dotSize, currentCoords[1])
            nextCharacter = self.recognizeCharacter(*currentCoords, colors=[constant.WHITE]).character

        phaseTime = ''.join(timeArr)
        if phaseTime == 'Bleed':
            return phase, None
        else:
            return phase, '00:' + phaseTime

    def recognizeMap(self):
        currentCoords = constant.MAP_START_LOCATION
        mapName = ''
        while colorMatches(self.loadedImage[currentCoords], [constant.GOLD]):
            nextChar = self.recognizeCharacter(*currentCoords, colors=[constant.GOLD]).character
            mapName = nextChar + mapName
            currentCoords = (currentCoords[0] - 3 * self.dotSize, currentCoords[1])

        return mapName

    def recognizeDisconnection(self):
        globalX, globalY = constant.FIRST_ERROR_START_LOCATION
        topLine = ''
        for _ in range(15):
            nextCharacter = self.recognizeCharacter(globalX, globalY, [constant.GRAY]).character
            topLine += nextCharacter
            globalX += (self.charLengths[nextCharacter] + 1) * self.dotSize

        globalX, globalY = constant.SECOND_ERROR_START_LOCATION
        bottomLine = ''
        for _ in range(12):
            nextCharacter = self.recognizeCharacter(globalX, globalY, [constant.GRAY]).character
            bottomLine += nextCharacter
            globalX += (self.charLengths[nextCharacter] + 1) * self.dotSize

        if topLine == 'Connection Lost' and bottomLine == 'Disconnected':
            return True
        else:
            return

    def recognizeLobby(self):
        return colorMatches(self.loadedImage[constant.COMPASS_LOCATION], [constant.COMPASS_COLOR])

    def readErrorMessage(self, img):
        self.loadImage(img)
        colors = [constant.WHITE, constant.GRAY]
        globalX, globalY = (900, 487)
        topLine = ''
        topLineLength = 0
        for _ in range(100):
            nextCharacter = self.recognizeCharacter(globalX, globalY, colors).character
            topLine += nextCharacter
            topLineLength += 1
            globalX += (self.charLengths[nextCharacter] + 1) * self.dotSize

        globalX, globalY = (900, 523)
        bottomLine = ''
        bottomLineLength = 0
        for _ in range(100):
            nextCharacter = self.recognizeCharacter(globalX, globalY, colors).character
            bottomLine += nextCharacter
            bottomLineLength += 1
            globalX += (self.charLengths[nextCharacter] + 1) * self.dotSize

        print(topLine)
        print(bottomLine)

# a = OCR(Image.open('D:\\Python\\AnniScraper\\ascii.png'))
# img = Image.open('D:\\Python\\AnniScraper\\score.png')
# print(a.processImage(img))
