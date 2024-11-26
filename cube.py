# black, isort and flake8 used for formatting

import copy
from random import randint

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
GREY = (169, 169, 169)

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

# moves
moves = []


def cube_net(default_colour):
    """
    blits cube net to screen
    :param colour_3d_array: cube colour array
    """
    surf = pygame.Surface((720, 540))
    surf.fill(default_colour)
    colour_3d_array = used_cube

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
        surf.blit(
            face(colour_3d_array[i]),
            (180 * i, 180)
            )

        surf.blit(
            face(colour_3d_array[4]),
            (180, 0)
            )

    surf.blit(
        face(colour_3d_array[5]),
        (180, 360)
        )
    return surf


def cube_3d(default_colour, default=False):
    """Returns the 3d cube, will be centered if blited to 0, 0"""
    surf = pygame.Surface((365, 335))
    surf.fill(default_colour)
    colour_3d_array = used_cube
    if default:
        colour_3d_array = default_cube

    def right():  
        def square(colour):
            surf = pygame.Surface((50, 75))  
            surf.fill(default_colour)
            pygame.draw.polygon(surf, colour, ((0, 25), (50, 0), (50, 50), (0, 75)))
            return surf

        def row(colour_list):
            surf = pygame.Surface((165, 135))  
            surf.fill(default_colour)
            for i in range(3):
                surf.blit(square(colour_list[i]), (55 * i, 60 - (30 * i)))
            surf.set_colorkey(default_colour)
            return surf

        def face(colour_array):
            surf = pygame.Surface((165, 250))  
            surf.fill(default_colour)
            for i in range(3):
                surf.blit(row(colour_array[i]), (0, 55 * i))
            return surf

        surf.blit(face(colour_3d_array[2]), (205, 90))

    def front():
        def square(colour):
            surf = pygame.Surface((50, 75))
            surf.fill(default_colour)
            pygame.draw.polygon(surf, colour, ((0, 0), (50, 25), (50, 75), (0, 50)))
            return surf

        def row(colour_list):
            surf = pygame.Surface((165, 135))
            surf.fill(default_colour)
            for i in range(3):
                surf.blit(square(colour_list[i]), (55 * i, 30 * i))
            surf.set_colorkey(default_colour)
            return surf

        def face(colour_array):
            surf = pygame.Surface((165, 250))
            surf.fill(default_colour)
            for i in range(3):
                surf.blit(row(colour_array[i]), (0, 55 * i))
            return surf

        surf.blit(face(colour_3d_array[1]), (40, 90))

    def top():
        def square(colour):
            surf = pygame.Surface((100, 50))
            surf.fill(default_colour)
            pygame.draw.polygon(surf, colour, ((50, 0), (100, 25), (50, 50), (0, 25)))
            surf.set_colorkey(default_colour)
            return surf

        def row(colour_list):
            surf = pygame.Surface((215, 120))
            surf.fill(default_colour)
            for i in range(3):
                surf.blit(square(colour_list[i]), (55 * i, 30 * i))
            surf.set_colorkey(default_colour)
            return surf

        def face(colour_array):
            surf = pygame.Surface((370, 315))
            surf.fill(default_colour)
            for i in range(3):
                surf.blit(row(colour_array[i]), (150 - (55 * i), 30 * i))
            surf.set_colorkey(default_colour)
            return surf

        surf.blit(face(colour_3d_array[4]), (0, 0))

    right()
    front()
    top()

    return surf

def cube_guide(default_colour):
    surf = pygame.Surface((500, 500))
    surf.fill(default_colour)
    colour_3d_array = used_cube
    colour = BLACK # bad idea if default_colour is black
    if default_colour == BLACK:
        print("BAD idea, change cube_guide colour first")
    #TODO: finnish
    def arrow(colour):
        surf = pygame.Surface((100, 100))
        surf.fill(default_colour)
        # pygame.draw.polygon(surf, colour, ((25, 0), (50, 0), (75, 25), (68, 13), (38, 25), (25, 50), (25, 75), (0, 75), (0, 50), (13, 25), (38, 13), (0, 0))) #TODO: arrow
        # pygame.draw.arc(surf, colour
        pygame.draw.polygon(surf, colour, ((13, 13), (50, 0), (63, 63), (50, 50), (50, 95), (25, 80), (25, 25)))
        surf.set_colorkey(default_colour)
        return surf

    surf.blit(cube_3d(default_colour, True), (50, 50))

    # top
    surf.blit(arrow(BLACK), (80, 63))
    surf.blit(arrow(BLACK), (140, 95))
    surf.blit(arrow(BLACK), (190, 123))

    # right
    arrow = pygame.transform.rotate(arrow(BLACK), 90)
    surf.blit(arrow, (200, 200))
    
    return surf


def turn(row_col, number, backwards=False, ignore_moves=False):
    """
    Turn 1 row or column once
    :type row_col: bool
    :type number: int
    :param row_col: row is True, column is False
    :param number: the number to do, left to right or top to bottom
    """

    if not ignore_moves:
        moves.append({"direction": row_col, "number": number, "backwards": backwards})

    loop = 1
    if backwards:  # 3 right is used to achieve 1 left, 3 up to achieve 1 down
        loop = 3
    for _ in range(loop):
        face0 = copy.deepcopy(used_cube[0])
        face1 = copy.deepcopy(used_cube[1])  # prevents pass by reference shenanigans
        face2 = copy.deepcopy(used_cube[2])
        face3 = copy.deepcopy(used_cube[3])
        face4 = copy.deepcopy(used_cube[4])
        face5 = copy.deepcopy(used_cube[5])

        n = number

        if row_col:
            used_cube[2][n], used_cube[3][n], used_cube[0][n], used_cube[1][n] = (
                face1[n],
                face2[n],
                face3[n],
                face0[n],
            )
            if number == 0:
                used_cube[4] = numpy.rot90(used_cube[4], k=1, axes=(0, 1))
            elif number == 2:
                used_cube[5] = numpy.rot90(used_cube[5], k=1, axes=(1, 0))
        else:
            for i in range(3):
                used_cube[1][i][n] = face5[i][n]
                used_cube[5][2 - i][n] = face3[i][2 - n]
                used_cube[3][2 - i][2 - n] = face4[i][n]
                used_cube[4][i][n] = face1[i][n]

            if number == 0:
                used_cube[0] = numpy.rot90(used_cube[0], k=1, axes=(0, 1))
            elif number == 2:
                used_cube[2] = numpy.rot90(used_cube[2], k=1, axes=(1, 0))


def rotate(axis, ignore_moves=False):
    """
    rotates the view of the cube without changing layout
    :param axis: x, y, z
    """
    face0 = copy.deepcopy(used_cube[0])
    face1 = copy.deepcopy(used_cube[1])  # prevents pass by reference shenanigans
    face2 = copy.deepcopy(used_cube[2])
    face3 = copy.deepcopy(used_cube[2])
    face3 = copy.deepcopy(used_cube[3])
    face4 = copy.deepcopy(used_cube[4])
    face5 = copy.deepcopy(used_cube[5])

    if not ignore_moves:
        moves.append({"rotation": True, "direction": axis})

    if axis == "x":
        for i in range(3):
            turn(True, i, ignore_moves=True)
    elif axis == "y":
        for i in range(3):
            turn(False, i, ignore_moves=True)
    elif axis == "z":
        used_cube[1] = numpy.rot90(used_cube[1], k=1, axes=(1, 0))
        used_cube[3] = numpy.rot90(used_cube[3], k=1, axes=(0, 1))

        for j in range(3):
            for i in range(3):
                used_cube[0][j][2 - i] = face5[i][j]
                used_cube[4][j][2 - i] = face0[i][j]
                used_cube[2][j][2 - i] = face4[i][j]
                used_cube[5][j][2 - i] = face2[i][j]


def scramble():
    for _ in range(randint(15, 25)):
        direction = bool(randint(0, 1))
        number = randint(0, 2)
        backwards = bool(randint(0, 1))

        turn(direction, number, backwards)


class Solver:
    def __init__(self):
        self.first = True
        self.sleep_time = 0.2

    def solve(self):
        """
        Does the reverse of all moves in backwards order
        """
        # TODO: better comment above

        if self.check_solved():
            return False

        if self.first:
            if len(moves) > 0:
                self.sleep_time = 5 / len(moves)
                self.first = False
            else:
                self.sleep_time = 1

        if len(moves) != 0:
            move = moves.pop()
            if "rotation" in move.keys():
                for _ in range(3):
                    rotate(move["direction"], ignore_moves=True)
            else:
                turn(move["direction"], move["number"], not move["backwards"], True)
            if len(moves) == 0:
                return False
            else:
                return True # comtinue solving
        else:
            return False

    def check_solved(self):
        not_solved = False
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    # checks for any square not the same colour as the middle square on the same face
                    if not numpy.all(used_cube[i][j][k] == used_cube[i][1][1]): 
                        not_solved = True
        return not not_solved



