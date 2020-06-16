from PIL import Image
import numpy as np
import helpers

TEAM_HEALTH_LOCATION = (1914, 483)
DAMAGE_LOCATION = (840, 897)
DAMAGE_MID_LOCATION = (962, 897)
DAMAGE_END_LOCATION = (1070, 897)
CHAT_START_LOCATION = (4, 945)
CHAT_STOP_LOCATION = (651, 601)
PHASE_START_LOCATION = (900, 29)

MAP_START_LOCATION = (1908, 465)
FIRST_ERROR_START_LOCATION = (928, 487)
SECOND_ERROR_START_LOCATION = (936, 523)
BACK_TO_SERVERS_LOCATION = (956, 575)
SHOTBOW_LOCATION = (952, 127)

COMPASS_LOCATION = (799, 1026)
COMPASS_COLOR = (127, 127, 127)


ANNI_LOBBY_LOCATION = (815, 431)
ANNI_HUB_ONE_LOCATION = (815, 450)
SERVERS_START_LOCATION = (815, 450)
SERVERS_END_LOCATION = (1103, 450)
SERVERS_PHASE_OFFSET = (43, 41)
SERVERS_SPACING = (36, 0)

# Rectangles for optimized resource pack
TEAM_HEALTH_RECTANGLE = (1746 + 70, 483, 1746 + 170, 483 + 70)
HIT_NOTIFICATION_RECTANGLE = (927, 897, 927 + 65, 897 + 15)
PHASE_RECTANGLE = (922, 29, 922 + 74, 29 + 16)

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
HEALTH_COLORS = (BLUE, GREEN, RED, YELLOW, WHITE)
COLORS_DICT = {WHITE: 'White', GRAY: 'Gray', BLUE: 'Blue', GREEN: 'Green', RED: 'Red', YELLOW: 'Yellow', PINK: 'Pink',
               GOLD: 'Gold', PURPLE: 'Purple'}

HIT_MESSAGE_CHAFF_CHARS = 33

MINECRAFT_IMAGE_WIDTH = 8
MINECRAFT_IMAGE_DOT = 8
MINECRAFT_DOT_SIZE = 2
MINECRAFT_MAX_NAME_LENGTH = 16
