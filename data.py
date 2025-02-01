"""
This file contains global data and settings information

This data is used by multiple files in the program. It may be edited here or it could be
provided to the user as settings for them to change.

black, isort and flake8 used for formatting
"""

import pygame
from pygame import freetype

pygame.font.init()
pygame.freetype.init()

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (169, 169, 169)

default_colour = GREY
guide_arrow_colour = BLACK


# fonts
default_font = pygame.freetype.SysFont("calibri", 20)
guide_font = pygame.freetype.SysFont("calibri", 20, bold=True)
