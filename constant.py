from PIL import Image
import numpy as np

# Rectangles for optimized resource pack
TEAM_HEALTH_RECTANGLE = (1746+70, 483, 1746+170, 483+70)
HIT_NOTIFICATION_RECTANGLE = (927, 897, 927+65, 897+15)
PHASE_RECTANGLE = (922, 29, 922+74, 29+16)

# Rectangle for default resource pack
# TEAM_HEALTH_RECTANGLE = (1746, 483, 1746 + 170, 483 + 70)
# HIT_NOTIFICATION_RECTANGLE = (652, 897, 652 + 614, 897 + 16)
# PHASE_RECTANGLE = (832, 29, 832 + 261, 29 + 16)

CHAT_RECTANGLE = (4, 603, 4 + 648, 603 + 358)

# CHAT_TOP_RECTANGLE = (4, 603, 4 + 648, 603+178)
# CHAT_BOTTOM_RECTANGLE = (4, 783, 4 + 648, 603+178)

ALPHABET = np.array(
    (' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4',
     '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
     'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^',
     '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
     't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'Δ'), dtype=str)
ALPHABET_INDICES = dict(zip(ALPHABET, range(len(ALPHABET))))

WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
BLUE = (85, 85, 255)
GREEN = (85, 255, 85)
RED = (255, 85, 85)
YELLOW = (255, 255, 85)
PINK = (255, 85, 255)
GOLD = (255, 170, 0)
PURPLE = (170, 0, 170)
COLORS = (WHITE, GRAY, BLUE, GREEN, RED, YELLOW, PINK, GOLD, PURPLE)
TEAM_COLORS = (BLUE, GREEN, RED, YELLOW)
COLORS_DICT = {WHITE: 'White', GRAY: 'Gray', BLUE: 'Blue', GREEN: 'Green', RED: 'Red', YELLOW: 'Yellow', PINK: 'Pink',
               GOLD: 'Gold', PURPLE: 'Purple'}

HIT_MESSAGE_CHAFF_CHARS = 33

MINECRAFT_ASCII_IMAGE_PATH = Image.open('D:\\Python\\AnniScraper\\ascii.png')
MINECRAFT_IMAGE_WIDTH = 8
MINECRAFT_IMAGE_DOT = 8
MINECRAFT_DOT_SIZE = 2
