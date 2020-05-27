from recordclass import recordclass


# Define a function that returns true if the pixel matches on of the colors in colorArr.
def colorMatches(pixel, colorArr):
    # print("Pixel color: " + str(pixel))
    for color in colorArr:
        if pixel[0] == color[0] and pixel[1] == color[1] and pixel[2] == color[2]:
            return True
    # print("No color match")
    return False


Coordinate2D = recordclass('Coordinate2D', 'x y')
RecognizedCharacter = recordclass('RecognizedCharacter', 'character colors')
DamageDealt = recordclass('DamageDealt', 'player playerTeam damagedNexus')
