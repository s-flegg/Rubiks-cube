##import matplotlib.pyplot as plt
##from mpl_toolkits.mplot3d import Axes3D
##import numpy
##
### create axis
##axes = [3, 3, 3] # dimesions
##
### create data
##data = numpy.ones(axes)
##
### control transparency
##alpha = 0.9
##
### colour
##colours = numpy.empty(axes + [4])
##
##colours[0] = [1, 0, 0, alpha] # red
##colours[1] = [0, 1, 0, alpha] # green
##colours[2] = [0, 0, 1, alpha] # blue
###colours[3] = [1, 1, 0, alpha] # yellow
###colours[4] = [1, 1, 1, alpha] # grey
##
####colours = numpy.empty(axes + [4], dtype=numpy.float32)
####
####colours[:] = [1, 0, 0, alpha]  # red
##
### plot figure
##fig = plt.figure() # create figure
##ax = fig.add_subplot(111, projection='3d') # add 3d axis
##
### voxels is used to customiise of the
### sizes, positions and colors.
##ax.voxels(data, facecolors=colours, edgecolors='grey')
##
### it can be used to change the axes view
##ax.view_init(100, 0)
##
##
##plt.show()


# https://www.glowscript.org/docs/VPythonDocs/index.html#
# https://matter-interactions.trinket.io/00_welcome_to_vpython#/welcome-to-vpython/getting-started
# https://stackoverflow.com/questions/49153057/how-to-color-every-face-of-a-box-in-vpython
# import vpython

# def cubelet(): # a "factory function"
# #create a list of the 6 pyramids with different colors; suppose its name is L
#
#     L = [
#         pyramid(color=color.red,pos=vec(),axis=vec()),
#         pyramid(color=color.green,pos=vec(),axis=vec()),
#         pyramid(color=color.blue,pos=vec(),axis=vec()),
#         pyramid(color=color.white,pos=vec(),axis=vec()),
#         pyramid(color=color.yellow,pos=vec(),axis=vec()),
#         pyramid(color=color.orange,pos=vec(),axis=vec())
#          ]
#     return compound(L)
#
# c = cubelet()

import pygame

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((1600, 900))

# right = pygame.draw.polygon(screen, RED, (
#         (800, 450),
#         (850, 825),
#         (800, 750),
#         (850, 775)
#     ))


def square():
    surf = pyga, e.Surface.polygon((0, 50), (50, 75), (0, 75))  #            (50, 25),


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    right = pygame.draw.polygon(
        screen,
        RED,
        (
            (800, 450),
            (850, 425),
            (850, 475),
            (800, 500),
        ),
    )
    left = pygame.draw.polygon(
        screen, GREEN, ((800, 450), (750, 425), (750, 475), (800, 500))
    )
    top = pygame.draw.polygon(
        screen, WHITE, ((800, 450), (850, 425), (800, 400), (750, 425))
    )

    # line = pygame.draw.line(screen, BLUE, (0, 500), (1600, 5))

    pygame.display.flip()
