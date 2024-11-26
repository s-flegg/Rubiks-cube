# black, isort and flake8 used for formatting

import copy

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

default_cube = [left, front, right, back, up, down]
used_cube = copy.deepcopy(default_cube)


# window
width = 1600
height = 900
screen = pygame.display.set_mode((width, height))
default_colour = BLACK


def cube(colour_3d_array):
    """
    blits cube net to screen
    :param colour_3d_array: cube colour array
    """

    def square(colour):
        surf = pygame.Surface((50, 50))
        surf.fill(colour)
        return surf

    def row(colour_list):
        surf = pygame.Surface((170, 50))  # 170, 50
        surf.fill(default_colour)
        for i in range(3):
            surf.blit(square(colour_list[i]), (i * 50 + i * 10, 0))
        return surf

    def face(colour_array):
        surf = pygame.Surface((170, 170))
        surf.fill(default_colour)
        for i in range(3):
            surf.blit(row(colour_array[i]), (0, i * 50 + i * 10))
        return surf

    for i in range(4):
        screen.blit(
            face(colour_3d_array[i]),
            (int((width / 2) + 10 + ((i - 2) * 200)), int(height / 2 - 170 / 2)),
        )

    screen.blit(
        face(colour_3d_array[4]),
        (int(width / 2 - 200 + 10), int(height / 2 - 170 - 170 / 2 - 20) - 10),
    )
    screen.blit(
        face(colour_3d_array[5]),
        (int(width / 2 - 200 + 10), int(height / 2 + 170 / 2 + 20) + 10),
    )


def rotate(row_col, number, backwards=False):
    """
    Turn 1 row or column once
    :type row_col: bool
    :type number: int
    :param row_col: row is True, column is False
    :param number: the number to do, left to right or top to bottom
    """

    loop = 1
    if backwards: # 3 right is used to achieve 1 left, 3 up to achieve 1 down
        loop = 3
    for j in range(loop):
        face0 = copy.deepcopy(used_cube[0])
        face1 = copy.deepcopy(used_cube[1])  # prevents pass by reference shenanigans
        face2 = copy.deepcopy(used_cube[2])
        face3 = copy.deepcopy(used_cube[2])
        face3 = copy.deepcopy(used_cube[3])
        face4 = copy.deepcopy(used_cube[4])
        face5 = copy.deepcopy(used_cube[5])

        n = number

        if row_col:
            used_cube[0][n], used_cube[1][n], used_cube[2][n], used_cube[3][n] = (
                face1[n],
                face2[n],
                face3[n],
                face0[n],
            )
            if number == 0:
                used_cube[4] = numpy.rot90(used_cube[4], k=1, axes=(1, 0))
            elif number == 2:
                used_cube[5] = numpy.rot90(used_cube[5], k=1, axes=(0, 1))
        else:
            for i in range(3):
                used_cube[1][i][n] = face5[i][n]
                used_cube[5][2 - i][n] = face3[i][2 - n]
                used_cube[3][2 - i][2 - n] = face4[i][n]
                used_cube[4][i][n] = face1[i][n]

            if number == 0:
                used_cube[0] = numpy.rot90(used_cube[0], k=1, axes=(1, 0))
            elif number == 2:
                used_cube[2] = numpy.rot90(used_cube[2], k=1, axes=(1, 0))


pygame.init()

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                rotate(True, 0)
            elif event.key == pygame.K_h:
                rotate(True, 1)
            elif event.key == pygame.K_n:
                rotate(True, 2)
            elif event.key == pygame.K_t:
                rotate(True, 0, True)
            elif event.key == pygame.K_g:
                rotate(True, 1, True)
            elif event.key == pygame.K_b:
                rotate(True, 2, True)

            elif event.key == pygame.K_q:
                rotate(False, 0)
            elif event.key == pygame.K_w:
                rotate(False, 1)
            elif event.key == pygame.K_e:
                rotate(False, 2)
            elif event.key == pygame.K_a:
                rotate(False, 0, True)
            elif event.key == pygame.K_s:
                rotate(False, 1, True)
            elif event.key == pygame.K_d:
                rotate(False, 2, True)

    screen.fill(BLACK)

    cube(used_cube)

    pygame.display.flip()
