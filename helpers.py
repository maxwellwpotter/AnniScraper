from recordclass import recordclass


# Define a function that returns true if the pixel matches on of the colors in colorArr.
def colorMatches(pixel, colorArr):
    # print("Pixel color: " + str(pixel))
    for color in colorArr:
        if pixel == color:
            # print("Color match")
            return True

    # ("No color match")
    return False


Coordinate2D = recordclass('Coordinate2D', 'x y')
RecognizedCharacter = recordclass('RecognizedCharacter', 'character colors')
