# black, isort and flake8 used for formatting
import copy
import sys

import numpy
import pygame

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# cube design
# split into sides as easier to write
up = [
    [WHITE, WHITE, WHITE],
    [WHITE, WHITE, WHITE],
    [WHITE, WHITE, WHITE],
]
down = [
    [YELLOW, YELLOW, YELLOW],
    [YELLOW, YELLOW, YELLOW],
    [YELLOW, YELLOW, YELLOW],
]

left = [
    [ORANGE, ORANGE, ORANGE],
    [ORANGE, ORANGE, ORANGE],
    [ORANGE, ORANGE, ORANGE],
]

right = [
    [RED, RED, RED],
    [RED, RED, RED],
    [RED, RED, RED],
]

front = [
    [GREEN, GREEN, GREEN],
    [GREEN, GREEN, GREEN],
    [GREEN, GREEN, GREEN],
]

back = [
    [BLUE, BLUE, BLUE],
    [BLUE, BLUE, BLUE],
    [BLUE, BLUE, BLUE],
]

# default cube may always be shown and used to check against for solves
default_cube = [
    left,
    front,
    right,
    back,
    up,
    down,
]
# deepcopy passes by value, not reference, ensuring default_cube is not changed
used_cube = copy.deepcopy(default_cube)


# window
width = 1600
height = 900
screen = pygame.display.set_mode((width, height))  # creates screen object
default_colour = BLACK


def validate_screen_positions(pos):
    """
    Ensures a position is within the confines of a standard 4k resolution screen

    This function is designed so that it can be used
    in the same place as the pos parameter.
    It should simply be placed where the pos wants to be used.
    It will quit the program if the pos is invalid.

    :param pos: the position to check
    :type pos: tuple[int, int]
    :return: tuple[int, int]
    """
    if pos[0] < 0 or pos[0] > 3840 or pos[1] < 0 or pos[1] > 2160:
        print("Error: invalid x or y value has been calculated.")
        pygame.quit()
        sys.exit()
    else:
        return pos


def cube(colour_3d_array):
    """
    Blits cube net to screen
    :param colour_3d_array: cube colour
    :type colour_3d_array: 3d array of tuples
    """

    def square(colour):
        """
        Creates the image of a single square
        :param colour: RGB value
        :type colour: tuple
        :return: pygame.Surface
        """
        surf = pygame.Surface((50, 50))
        surf.fill(colour)
        return surf

    def row(colour_list):
        """
        Creates the image of a row of 3 squares
        :param colour_list: List of RGB values
        :type colour_list: List len(3) of Tuples
        :Return: pygame.Surface
        """
        surf = pygame.Surface((170, 50))
        surf.fill(default_colour)
        for i in range(3):
            # iterates alongside the list of colours,
            # getting a square with the respective colour and
            # blitting it to calculated position
            # i * 50 ensures the square is blitted after the previous one; not inside it
            # i * 10 adds 10 spacing between the cubes
            surf.blit(square(colour_list[i]), (i * 50 + i * 10, 0))
        return surf

    def face(colour_array):
        """
        Creates one face (side) from 3 rows
        :param colour_array: Array of RGB values [row1 row2, row3]
        :type colour_array: 2D array of tuples
        :return: pygame.Surface
        """
        surf = pygame.Surface((170, 170))
        surf.fill(default_colour)
        for i in range(3):
            # iterates alongside the list of rows,
            # getting and blitting the row image to calculated position
            # i * 50 ensures the row is placed beneath, and not inside, the previous row
            # i * 10 is for spacing between the rows
            surf.blit(row(colour_array[i]), (0, i * 50 + i * 10))
        return surf

    # 4 of the faces are placed next to each other so a loop can place them
    for i in range(4):
        screen.blit(
            face(colour_3d_array[i]),  # gets the image of the face
            # width / 2, height / 2, i - 2 are for centering, -2 as 4 faces total
            # * 200 for moving past the previous face and 30 spacing
            # - 170 / 2 for centering
            validate_screen_positions(
                (int((width / 2) + 10 + ((i - 2) * 200)), int(height / 2 - 170 / 2))
            ),
        )

    screen.blit(
        face(colour_3d_array[4]),
        validate_screen_positions(
            (int(width / 2 - 200 + 10), int(height / 2 - 170 - 170 / 2 - 20) - 10)
        ),
    )
    screen.blit(
        face(colour_3d_array[5]),
        validate_screen_positions(
            (int(width / 2 - 200 + 10), int(height / 2 + 170 / 2 + 20) + 10)
        ),
    )


def rotate(row_col, number, backwards=False):
    """
    Turn 1 row or column once
    :type row_col: bool
    :type number: int
    :type backwards: bool
    :param row_col: True=row, False=column
    :param number: the number to do, left to right or top to bottom
    :param backwards: do the opposite of the move/co the move 3 times if true
    """

    loop = 1
    if backwards:  # 3 right is used to achieve 1 left, 3 up to achieve 1 down
        loop = 3
    for j in range(loop):
        face0 = copy.deepcopy(used_cube[0])
        face1 = copy.deepcopy(used_cube[1])  # prevents pass by reference shenanigans
        face2 = copy.deepcopy(
            used_cube[2]
        )  # copy the value instead of creating a reference
        face3 = copy.deepcopy(used_cube[2])
        face3 = copy.deepcopy(used_cube[3])
        face4 = copy.deepcopy(used_cube[4])
        face5 = copy.deepcopy(used_cube[5])

        n = number

        if row_col:  # rotate row
            used_cube[0][n], used_cube[1][n], used_cube[2][n], used_cube[3][n] = (
                face1[n],
                face2[n],
                face3[n],
                face0[n],
            )
            if number == 0:  # rotate the top face
                used_cube[4] = numpy.rot90(used_cube[4], k=1, axes=(1, 0))
            elif number == 2:  # rotate the bottom face
                used_cube[5] = numpy.rot90(used_cube[5], k=1, axes=(0, 1))
        else:  # column
            for i in range(3):  # each loop only moves 1 square
                used_cube[1][i][n] = face5[i][n]
                # 2-i flips the row number for the back
                # 2 - n flips the column number for the back
                used_cube[5][2 - i][n] = face3[i][2 - n]
                used_cube[3][2 - i][2 - n] = face4[i][n]
                used_cube[4][i][n] = face1[i][n]

            if number == 0:  # rotate left face
                used_cube[0] = numpy.rot90(used_cube[0], k=1, axes=(1, 0))
            elif number == 2:  # rotate right face
                used_cube[2] = numpy.rot90(used_cube[2], k=1, axes=(1, 0))


pygame.init()

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            # row left
            if event.key == pygame.K_r:
                rotate(True, 0)
            elif event.key == pygame.K_f:
                rotate(True, 1)
            elif event.key == pygame.K_v:
                rotate(True, 2)
            # row right
            elif event.key == pygame.K_t:
                rotate(True, 0, True)
            elif event.key == pygame.K_g:
                rotate(True, 1, True)
            elif event.key == pygame.K_b:
                rotate(True, 2, True)
            # column up
            elif event.key == pygame.K_q:
                rotate(False, 0)
            elif event.key == pygame.K_w:
                rotate(False, 1)
            elif event.key == pygame.K_e:
                rotate(False, 2)
            # column down
            elif event.key == pygame.K_a:
                rotate(False, 0, True)
            elif event.key == pygame.K_s:
                rotate(False, 1, True)
            elif event.key == pygame.K_d:
                rotate(False, 2, True)

    screen.fill(BLACK)

    cube(used_cube)

    pygame.display.flip()
