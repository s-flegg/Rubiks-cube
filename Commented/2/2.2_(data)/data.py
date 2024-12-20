  # this file contains global data and settings information
# settings information are all the variables that the
# user is able given as a setting
# e.g. default_colour

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

# empty image for returning, ineffecient
empty_image = pygame.Surface((1, 1))# .set_colorkey(BLACK)

