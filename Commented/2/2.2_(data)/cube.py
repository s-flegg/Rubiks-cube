# black, isort and flake8 used for formatting

import copy
import time
from random import randint

import data
import interface
import numpy
import pygame

# colours
from data import BLACK, BLUE, GREEN, GREY, ORANGE, RED, WHITE, YELLOW, default_colour

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

default_cube = [
    left,
    front,
    right,
    back,
    up,
    down,
]  # so a default cube may always be shown and to check against for solves
used_cube = copy.deepcopy(
    default_cube
)  # deepcopy passes by value, not reference, ensuring default_cube is not changed

# used for tracking moves and 'solving' the cube
moves = []


class CubeNet:  # more classes (and make update draw things)
    def __init__(self, surface, pos):
        # pos is centre
        self.screen = surface
        self.pos = pos

    def update(self):
        image = self.get_image()
        self.screen.blit(image, image.get_rect(center=self.pos))

    def get_image(self):
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
            surf.blit(face(colour_3d_array[i]), (180 * i, 180))

            surf.blit(face(colour_3d_array[4]), (180, 0))

        surf.blit(face(colour_3d_array[5]), (180, 360))
        return surf


class Cube3D:
    def __init__(self, surface, pos):
        # pos is centre
        self.screen = surface
        self.pos = pos

    def update(self):
        image = self.get_image()
        self.screen.blit(image, image.get_rect(center=self.pos))

    def get_image(self, default=False):
        """Returns the 3d cube, will be centered if blited to 0, 0"""
        surf = pygame.Surface((365, 335))
        surf.fill(default_colour)
        colour_3d_array = used_cube
        if default:
            colour_3d_array = default_cube  # TODO: check if needed

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
                pygame.draw.polygon(
                    surf, colour, ((50, 0), (100, 25), (50, 50), (0, 25))
                )
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


class CubeGuide:
    def __init__(self, surface, pos):
        # pos is centre
        self.screen = surface
        self.pos = pos

    def update(self):
        image = self.get_image()
        self.screen.blit(image, image.get_rect(center=self.pos))

    def get_image(self):
        surf = pygame.Surface((600, 600))  # 600
        surf.fill(default_colour)
        colour = data.guide_arrow_colour
        if default_colour == BLACK:
            print("BAD idea, change cube_guide colour first")

        # TODO: finnish
        def arrow_top(text, angle=0):
            surf = pygame.Surface((100, 100))
            surf.fill(default_colour)
            pygame.draw.polygon(
                surf,
                colour,
                ((13, 13), (50, 0), (63, 63), (50, 50), (50, 93), (25, 80), (25, 25)),
            )
            surf.set_colorkey(default_colour)
            # angle
            surf = pygame.transform.rotate(surf, angle)
            # letter
            surf.blit(
                interface.text(text, data.guide_font, BLACK, data.default_colour),
                (15, 0),
            )
            return surf

        def arrow_right(text, angle=0):
            surf = pygame.Surface((100, 100))
            surf.fill(default_colour)
            pygame.draw.polygon(
                surf,
                colour,
                (
                    (38, 50),
                    (63, 25),
                    (63, 38),
                    (100, 38),
                    (100, 63),
                    (63, 63),
                    (63, 75),
                ),
            )
            surf.set_colorkey(default_colour)
            # angle
            surf = pygame.transform.rotate(surf, angle)
            # letter
            surf.blit(
                interface.text(text, data.guide_font, BLACK, data.default_colour),
                (35, 25),
            )
            return surf

        def arrow_rotate(text, angle=0):
            surf = pygame.Surface((200, 100))
            surf.fill(default_colour)
            pygame.draw.polygon(
                surf,
                colour,
                (
                    (200, 50),
                    (150, 100),
                    (150, 75),
                    (0, 75),
                    (0, 25),
                    (150, 25),
                    (150, 0),
                ),
            )
            surf.set_colorkey(default_colour)
            # angle
            surf = pygame.transform.rotate(surf, angle)
            # letter
            surf.blit(
                interface.text(text, data.guide_font, BLACK, data.default_colour),
                (0, 0),
            )
            return surf

        cube_offset_x = 100
        cube_offset_y = 50
        surf.blit(Cube3D.get_image(True), (cube_offset_x, cube_offset_y))

        # up
        surf.blit(arrow_top("Q"), (cube_offset_x + 30, cube_offset_y + 13))
        surf.blit(arrow_top("W"), (cube_offset_x + 90, cube_offset_y + 45))
        surf.blit(arrow_top("E"), (cube_offset_x + 150, cube_offset_y + 73))

        # left
        surf.blit(arrow_right("R"), (cube_offset_x + 100, cube_offset_y + 150))
        surf.blit(arrow_right("F"), (cube_offset_x + 100, cube_offset_y + 200))
        surf.blit(arrow_right("V"), (cube_offset_x + 100, cube_offset_y + 250))

        # right
        surf.blit(arrow_right("T", 180), (cube_offset_x + 205, cube_offset_y + 152))
        surf.blit(arrow_right("G", 180), (cube_offset_x + 205, cube_offset_y + 202))
        surf.blit(arrow_right("B", 180), (cube_offset_x + 205, cube_offset_y + 252))

        # down
        surf.blit(arrow_top("A", 180), (cube_offset_x, cube_offset_y + 250))
        surf.blit(arrow_top("S", 180), (cube_offset_x + 50, cube_offset_y + 277))
        surf.blit(arrow_top("D", 180), (cube_offset_x + 100, cube_offset_y + 305))

        # rotate
        surf.blit(arrow_rotate("X"), (cube_offset_x + 50, cube_offset_y + 400))
        surf.blit(arrow_rotate("Y", 90), (cube_offset_x - 100, cube_offset_y + 100))
        surf.blit(arrow_rotate("Z", 335), (cube_offset_x + 250, cube_offset_y - 50))

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
    for _ in range(1):  # randint(15, 25)):
        direction = bool(randint(0, 1))
        number = randint(0, 2)
        backwards = bool(randint(0, 1))

        turn(direction, number, backwards)


# ----------------------------------------------------------------- ORIGINAL SOLVER ------------------------------------------------------------------------ #
class Solver:
    def __init__(self):
        self.first = True
        self.sleep_time = 0.2

    def solve(self):
        """
        Does the reverse of all moves in backwards order
        """
        # TODO: better comment above

        if self.first:
            if len(moves) > 0:
                self.sleep_time = 5 / len(moves)
                self.first = False
            else:
                self.sleep_time = 1

        return self.pop_move()

    def check_solved(self):
        not_solved = False
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    # checks for any square not the same colour as the middle square on the same face
                    if not numpy.all(used_cube[i][j][k] == used_cube[i][1][1]):
                        not_solved = True
        return not not_solved

    def pop_move(self):
        if self.check_solved():
            return False

        if len(moves) != 0:
            move = moves.pop()
            if "rotatiopn" in move.keys():
                for _ in range(3):
                    rotate(move["direction"], ignore_moves=True)
            else:
                turn(move["direction"], move["number"], not move["backwards"], True)
            if len(moves) == 0:
                return False
            else:
                return True  # comtinue solving
        else:
            return False


# ------------------------------------------------F2L SOLVER------------------------------------------------------------------------------------------------------- #

##class Solver:
##    def __init__(self):
##        self.y = True
##        self.sleep_time = 0.2

##    def solve(self):
##        """
##        call each game loop until it returns false, it does one move per call
##        :return: bool
##        """
##        # use of algos from: https://solvethecube.com/algorithms
##
##        def f2l():
##            # algos require top centre be yellow,
##            # front centre be blue and right centre be red
##            if not (
##                # numpy.all is needed due to issues comparing arrays,
##                # all is used to ensure a full rgb match
##                numpy.all(used_cube[4][1][1] == YELLOW)
##                and numpy.all(used_cube[1][1][1] == BLUE)
##                and numpy.all(used_cube[2][1][1] == RED)
##            ):
##                if not numpy.all(used_cube[4][1][1] == YELLOW):
##                    if self.y:  # this will eventually always place yellow at the top
##                        rotate("y")
##                    else:
##                        rotate("z")
##                    self.y = not self.y
##                    return True
##                if not (
##                    numpy.all(used_cube[1][1][1] == BLUE)
##                    and numpy.all(used_cube[2][1][1] == RED)
##                ):
##                    rotate("x") # place blue at the front
##                    return True
##
##            #if (
##            #    numpy.all(used_cube[4][1][1] == YELLOW)
##            #    and numpy.all(used_cube[1][1][1] == BLUE)
##            #    and numpy.all(used_cube[2][1][1] == RED)
##            #):
##                # add cases
##            # basic cases
##
##            # R U R'
##            if (
##
##        return f2l()
# -------------------------------------------------------------------------------------------------


class Timer:
    def __init__(self):
        self.start_time = 0
        self.end = 0
        self.elapsed = 0
        self.exists = False
        self.running = False

    def start(self):
        self.exists = True
        self.running = True
        self.start_time = time.time()

    def stop(self):
        self.update()
        self.running = False

    def delete(self):
        self.exists = False

    def update(self):
        if self.running:
            self.end = time.time()
            self.elapsed = self.end - self.start_time

    def display_elapsed(self):
        if not self.exists:  # checks if tmier has ever run
            return data.empty_image
        secs = 60  # amount of seconds before swapping to minute display, must be interval of 60
        if self.elapsed < secs:
            image = interface.text(
                str(round(self.elapsed, 3)) + " seconds",
                data.default_font,
                BLACK,
                default_colour,
            )  # pygame cannot render \n
        else:
            image = interface.text(
                str(int(self.elapsed / secs))
                + "m "
                + str(int(self.elapsed % secs))
                + "s ",
                data.default_font,
                BLACK,
                default_colour,
            )

        return image
