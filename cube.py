"""
This file contains the code for the cube as well as game features that reference the cube

This file handles all the data to do with the cube: its state, moves made, etc.
It also handles features that make use of the cube such as the solver and timer.

black, isort and flake8 used for formatting
"""

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

# so a default cube may always be shown and to check against for solves
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

# used for tracking moves and 'solving' the cube
moves = []


class CubeNet:
    """Handles the display of the cube as a net to a fixed position on the screen"""

    def __init__(self, surface, pos):
        """
        :param surface: The surface that this cube is to be blitted to
        :param pos: The centre position that this cube is to be blitted to: x,y
        :type surface: pygame.Surface
        :type pos: list[int] or tuple[int, int]
        """
        # pos is centre
        self.screen = surface
        self.pos = pos

    def update(self):
        """
        Updates the cube image and re-blits it to the surface

        :rtype: None
        """
        image = self.get_image()
        self.screen.blit(image, image.get_rect(center=self.pos))

    @staticmethod
    def get_image(default=False):
        """
        Creates the image of the cube from the current state of the cube

        :param default: if True, uses the default image instead of the current state
        :type default: bool
        :return: the image of the cube as a 720x540 surface
        :rtype: pygame.Surface
        """
        surf = pygame.Surface((720, 540))
        surf.fill(default_colour)
        colour_3d_array = used_cube
        if default:
            colour_3d_array = default_cube

        def square(colour):
            """
            Creates a single square with the given colour

            :param colour: the RGB values of the colour
            :type colour: tuple[int, int, int]
            :return: the square image, 50x50
            :rtype: pygame.Surface
            """
            surf = pygame.Surface((50, 50))
            surf.fill(colour)
            return surf

        def row(colour_list):
            """
            Creates the image of a row of 3 squares

            :param colour_list: List len(3) of tuples, where each tuple is an RGB value
            :type colour_list: list[tuple[int, int, int]]
            :return: the row image, 170*50
            :rtype: pygame.Surface
            """
            surf = pygame.Surface((170, 50))
            surf.fill(default_colour)
            for i in range(3):
                # iterates alongside the list of colours,
                # getting a square with the respective colour and
                # blitting it to calculated position
                # i * 50 ensures the square is blitted after the previous one;
                # not inside it
                # i * 10 adds 10 spacing between the cubes
                surf.blit(square(colour_list[i]), (i * 50 + i * 10, 0))
            return surf

        def face(colour_array):
            """
            Creates one face (side) from 3 rows

            :param colour_array: 2D array (3x3)(row x col) of tuples,
                where each tuple is an RGB value
            :type colour_array: list[list[tuple[int, int, int]]]
            :return: the face image, 170*170
            :rtype: pygame.Surface
            """
            surf = pygame.Surface((170, 170))
            surf.fill(default_colour)
            for i in range(3):
                # iterates alongside the list of rows,
                # getting and blitting the row image to calculated position
                # i * 50 ensures the row is placed beneath,
                # and not inside, the previous row
                # i * 10 is for spacing between the rows
                surf.blit(row(colour_array[i]), (0, i * 50 + i * 10))
            return surf

        # 4 of the faces are placed next to each other so a loop can place them
        for i in range(4):
            surf.blit(
                face(colour_3d_array[i]),  # gets the image of the face
                # 180 * i includes 10 pixels spacing
                # placed 180 down to allow top to be placed above with 10 pixels spacing
                (180 * i, 180),
            )

        # 180 x val aligns with front face
        surf.blit(face(colour_3d_array[4]), (180, 0))
        # 360 is below face image with 10 pixels spacing
        surf.blit(face(colour_3d_array[5]), (180, 360))
        return surf


class Cube3D(CubeNet):
    """
    Handles the display of the 3d cube to a fixed position on the screen

    This class is a child of CubeNet, only changing the get_image method
    """

    @staticmethod
    def get_image(default=False):
        """
        Creates the image of the cube from its current state

        :param default: if True, uses the default image instead of the current state
        :type default: bool
        :return: the cube image, 365*335
        :rtype: pygame.Surface
        """
        surf = pygame.Surface((365, 335))
        surf.fill(default_colour)
        colour_3d_array = used_cube
        if default:
            colour_3d_array = default_cube

        def right():
            """
            Draws the right face of the cube to the surf, it is a slanted square

            :rtype: None
            """

            def square(colour):
                """
                Creates a slanted cube of solid colour

                :param colour: RGB values
                :type colour: tuple[int, int, int]
                :return: the square image, 50*75
                :rtype: pygame.Surface
                """
                surf = pygame.Surface((50, 75))
                surf.fill(default_colour)
                pygame.draw.polygon(surf, colour, ((0, 25), (50, 0), (50, 50), (0, 75)))
                surf.set_colorkey(default_colour)  # make background transparent
                return surf

            def row(colour_list):
                """
                Creates a slanted row of 3 squares

                :param colour_list: List len(3) of tuples of RGB values
                :type colour_list: list[tuple[int, int, int]]
                :return: the row image, 165*135
                :rtype: pygame.Surface
                """
                surf = pygame.Surface((165, 135))
                surf.fill(default_colour)
                for i in range(3):
                    # 55 includes 5 pixels spacing
                    # -30 includes 5 pixels spacing
                    surf.blit(square(colour_list[i]), (55 * i, 60 - (30 * i)))
                surf.set_colorkey(default_colour)
                return surf

            def face(colour_array):
                """
                Stacks 3 row images to create a face of 9 squares

                :param colour_array: 2D (3x3)(row x col) array of tuples of RGB values
                :type colour_array: list[list[tuple[int, int, int]]]
                :return: the row image, 165*250
                :rtype: pygame.Surface
                """
                surf = pygame.Surface((165, 250))
                surf.fill(default_colour)
                for i in range(3):
                    surf.blit(row(colour_array[i]), (0, 55 * i))
                return surf

            # positioned to the right of front face with 5 pixels spacing
            surf.blit(face(colour_3d_array[2]), (205, 90))

        def front():
            """
            Draws the front face of the cube to the surf, it s a slanted square

            :rtype: None
            """

            def square(colour):
                """
                Creates a slanted cube of solid colour

                :param colour: RGB values
                :type colour: tuple[int, int, int]
                :return: the square image
                :rtype: pygame.Surface
                """
                surf = pygame.Surface((50, 75))
                surf.fill(default_colour)
                pygame.draw.polygon(surf, colour, ((0, 0), (50, 25), (50, 75), (0, 50)))
                surf.set_colorkey(default_colour)
                return surf

            def row(colour_list):
                """
                Creates the image of a row of 3 squares

                :param colour_list: List len(3) of tuples of RGB values
                :type colour_list: list[tuple[int, int, int]]
                :return: the row image
                :rtype: pygame.Surface
                """
                surf = pygame.Surface((165, 135))
                surf.fill(default_colour)
                for i in range(3):
                    # 55 includes 5 pixels spacing
                    # 30 includes 5 pixels spacing
                    surf.blit(square(colour_list[i]), (55 * i, 30 * i))
                surf.set_colorkey(default_colour)
                return surf

            def face(colour_array):
                """
                Stacks 3 row images to create a face of 9 squares

                :param colour_array: 2D array (3x3)(row x col) of tuples of RGB values
                :type colour_array: list[list[tuple[int, int, int]]]
                :return: the face image
                :rtype: pygame.Surface
                """
                surf = pygame.Surface((165, 250))
                surf.fill(default_colour)
                for i in range(3):
                    # 55 includes 5 pixels spacing
                    surf.blit(row(colour_array[i]), (0, 55 * i))
                surf.set_colorkey(default_colour)
                return surf

            # positioned below top of front face with 5 pixels spacing
            surf.blit(face(colour_3d_array[1]), (40, 90))

        def top():
            """
            Draws the top face of the cube to the surf,
            it is a horizontally stretched square

            :rtype: None
            """

            def square(colour):
                """
                Creates a horizontally stretched cube of solid colour

                :param colour: RGB values
                :type colour: tuple[int, int, int]
                :return: the square image
                :rtype: pygame.Surface
                """
                surf = pygame.Surface((100, 50))
                surf.fill(default_colour)
                pygame.draw.polygon(
                    surf, colour, ((50, 0), (100, 25), (50, 50), (0, 25))
                )
                surf.set_colorkey(default_colour)
                return surf

            def row(colour_list):
                """
                Creates the image of a row of 3 squares

                :param colour_list: List len(3) of tuples of RGB values
                :type colour_list: list[tuple[int, int, int]]
                :return: the row image
                :rtype: pygame.Surface
                """
                surf = pygame.Surface((215, 120))
                surf.fill(default_colour)
                for i in range(3):
                    # 55 includes 5 pixels spacing
                    # 30 includes 5 pixels spacing
                    surf.blit(square(colour_list[i]), (55 * i, 30 * i))
                surf.set_colorkey(default_colour)
                return surf

            def face(colour_array):
                """
                Stacks 3 row images to create a face of 9 squares

                :param colour_array: 2D array (3x3)(row x col) of tuples of RGB values
                :type colour_array: list[list[tuple[int, int, int]]]
                :return: the face image
                :rtype: pygame.Surface
                """
                surf = pygame.Surface((370, 315))
                surf.fill(default_colour)
                for i in range(3):
                    # 150 - to place bottom to top
                    # 55 includes 5 pixels spacing
                    # 30 includes 5 pixels spacing
                    surf.blit(row(colour_array[i]), (150 - (55 * i), 30 * i))
                surf.set_colorkey(default_colour)
                return surf

            surf.blit(face(colour_3d_array[4]), (0, 0))

        right()
        front()
        top()

        return surf


class CubeGuide(Cube3D):
    """
    Class that handles the guide cube and adds instructions

    This class inherits from Cube3D and overrides the get_image method
    """

    @classmethod
    def get_image(cls):
        """
        Creates the image of the default cube with added instructions

        :return: the cube image, 600*600
        :rtype: pygame.Surface
        """
        surf = pygame.Surface((600, 600))
        surf.fill(default_colour)
        colour = data.guide_arrow_colour
        if default_colour == colour:
            # arrows will blend into background
            print("BAD idea, change guide arrow colour first")

        def arrow_top(text, angle=0):
            """
            Draws an arrow aligned with the cubes slant on the top edge

            :param text: text to draw above the arrow
            :param angle: clockwise angle to rotate the arrow, 0 is upwards
            :type text: str
            :type angle: int
            :return: the image of the arrow, 100*100
            :rtype: pygame.Surface
            """
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
                interface.text(
                    text=text,
                    font=data.guide_font,
                    foreground_colour=BLACK,
                    background_colour=data.default_colour,
                ),
                (15, 0),
            )
            return surf

        def arrow_right(text, angle=0):
            """
            Draws an arrow aligned with the cubes slant on the right edge

            :param text: text to draw above the arrow
            :param angle: clockwise angle to rotate the arrow, 0 is right
            :type text: str
            :type angle: int
            :return: the image of the arrow, 100*100
            :rtype: pygame.Surface
            """
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
                interface.text(
                    text=text,
                    font=data.guide_font,
                    foreground_colour=BLACK,
                    background_colour=data.default_colour,
                ),
                (35, 25),
            )
            return surf

        def arrow_rotate(text, angle=0):
            """
            Draws a large stright arrow

            :param text: text to draw above the arrow
            :param angle: clockwise angle to rotate the arrow, 0 is right
            :type text: str
            :type angle: int
            :return: the image of the arrow, 100*100
            :rtype: pygame.Surface
            """
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
                interface.text(
                    text=text,
                    font=data.guide_font,
                    foreground_colour=BLACK,
                    background_colour=data.default_colour,
                ),
                (0, 0),
            )
            return surf

        # offsets allow moving cube and arrows
        # whilst maintaining thier relative position to each other
        cube_offset_x = 100
        cube_offset_y = 50

        # cube
        surf.blit(super().get_image(True), (cube_offset_x, cube_offset_y))

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
    Turn 1 row or column once in a given direction, default is right/up

    :param row_col: row is True, column is False
    :param number: the number to do, left to right or top to bottom
    :param backwards: do the opposite of the move/do the move 3 times if true
    :param ignore_moves: don't add the move to the moves list
    :type row_col: bool
    :type number: int
    :type backwards: bool
    :type ignore_moves: bool
    :rtype: None
    """

    if not ignore_moves:
        # add the move to the moves list
        # ignoring is useful for solving
        moves.append({"direction": row_col, "number": number, "backwards": backwards})

    # loop to turn the row or column the correct number of times
    loop = 1
    if backwards:  # 3 right is used to achieve 1 left, 3 up to achieve 1 down
        loop = 3

    for _ in range(loop):
        # make copies of the faces of the cube so the original state isn't lost
        # deepcopy prevents pass by reference shenanigans
        # by copying the value instead of creating a reference
        face0 = copy.deepcopy(used_cube[0])
        face1 = copy.deepcopy(used_cube[1])
        face2 = copy.deepcopy(used_cube[2])
        face3 = copy.deepcopy(used_cube[3])
        face4 = copy.deepcopy(used_cube[4])
        face5 = copy.deepcopy(used_cube[5])

        n = number

        if row_col:  # turn the row
            used_cube[2][n], used_cube[3][n], used_cube[0][n], used_cube[1][n] = (
                face1[n],
                face2[n],
                face3[n],
                face0[n],
            )
            if number == 0:  # rotate the top face
                used_cube[4] = numpy.rot90(used_cube[4], k=1, axes=(0, 1))
            elif number == 2:  # rotate the bottom face
                used_cube[5] = numpy.rot90(used_cube[5], k=1, axes=(1, 0))
        else:  # turn the column
            for i in range(3):
                used_cube[1][i][n] = face5[i][n]
                # 2-i flips the row number for the back
                # 2 - n flips the column number for the back
                used_cube[5][2 - i][n] = face3[i][2 - n]
                used_cube[3][2 - i][2 - n] = face4[i][n]
                used_cube[4][i][n] = face1[i][n]

            if number == 0:  # rotate left face
                used_cube[0] = numpy.rot90(used_cube[0], k=1, axes=(0, 1))
            elif number == 2:  # rotate right face
                used_cube[2] = numpy.rot90(used_cube[2], k=1, axes=(1, 0))


def rotate(axis, ignore_moves=False):
    """
    Rotates the view of the cube without changing layout

    :param axis: x, y, z
    :type axis: str
    :param ignore_moves: whether to add the move to the moves list, defaults to False
    :type ignore_moves: bool or optional
    :rtype: None
    """
    # make copies of the faces of the cube so the original state isn't lost
    # deepcopy prevents pass by reference shenanigans
    # by copying the value instead of creating a reference
    face0 = copy.deepcopy(used_cube[0])
    face1 = copy.deepcopy(used_cube[1])
    face2 = copy.deepcopy(used_cube[2])
    face3 = copy.deepcopy(used_cube[2])
    face3 = copy.deepcopy(used_cube[3])
    face4 = copy.deepcopy(used_cube[4])
    face5 = copy.deepcopy(used_cube[5])

    if not ignore_moves:  # add the move to the moves list
        # ignoring is useful for solving
        moves.append({"rotation": True, "direction": axis})

    if axis == "x":
        for i in range(3):  # equivalent to a rotation along the x axis
            turn(True, i, ignore_moves=True)
    elif axis == "y":
        for i in range(3):  # equivalent to a rotation along the y axis
            turn(False, i, ignore_moves=True)
    elif axis == "z":  # equivalent to a rotation along the z axis
        # rotate the front and back faces
        used_cube[1] = numpy.rot90(used_cube[1], k=1, axes=(1, 0))
        used_cube[3] = numpy.rot90(used_cube[3], k=1, axes=(0, 1))

        # required a lot of manual testing
        # carefully test any changes
        for j in range(3):
            for i in range(3):
                used_cube[0][j][2 - i] = face5[i][j]
                used_cube[4][j][2 - i] = face0[i][j]
                used_cube[2][j][2 - i] = face4[i][j]
                used_cube[5][j][2 - i] = face2[i][j]


def scramble():
    """
    Randomly scrambles the cube by making between 15 and 25 moves randomly

    :rtype: None
    """
    for _ in range(randint(15, 25)):
        # randomise every aspect of the turn
        direction = bool(randint(0, 1))
        number = randint(0, 2)
        backwards = bool(randint(0, 1))

        turn(direction, number, backwards)


class Solver:
    """
    Solve the cube, one turn per game loop

    The solve function must be called once per game loop
    until it returns False
    to completely solve the cube

    The attribute first should be updated to True before each complete solve

    A solve can optionally be made to take 5 seconds. To do this, implement a
    time.sleep(this_object.sleep_time) before the this_object.solve() call
    """

    def __init__(self):
        self.first = True
        """If it is the first move of the solve
        :type: bool"""
        self.sleep_time = 0.2
        """The amount of time to wait between each move
        :type: float"""

    def solve(self):
        """
        Does the reverse of the last done move and removes it from the moves list

        :return: False if the cube is solved, True otherwise
        :rtype: bool
        """
        # guard clause
        if len(moves) == 0 or self.check_solved():
            return False

        # calculate time to wait between move
        if self.first:
            if len(moves) > 0:
                # every solve should take 5 seconds regardless of moves required,
                # although this can be affected by hardware limitations
                self.sleep_time = 5 / len(moves)
                self.first = False
            else:
                # wait upon every button press so the user knows it has 'worked'
                # even when the cube is already solved
                self.sleep_time = 1

        return self.pop_move()

    def check_solved(self):
        """
        Checks whether the cube is in a solved state

        :return: True if the cube is solved, False otherwise
        :rtype: bool
        """
        not_solved = False
        for i in range(6):  # face
            for j in range(3):  # row
                for k in range(3):  # column
                    # checks for any square not the same colour
                    # as the middle square on the same face
                    # numpy.all handles it being a tuple comparison
                    if not numpy.all(used_cube[i][j][k] == used_cube[i][1][1]):
                        not_solved = True
        return not not_solved

    @staticmethod
    def pop_move():
        """
        Removes a move from the moves list and does the reverse

        :return: False if the cube is solved, True otherwise
        :rtype: bool
        """
        # guard clause
        if len(moves) == 0:
            return False

        move = moves.pop()  # get the move dictionary
        if "rotation" in move.keys():  # check if the move was a rotation
            # rotate does not have a backwards parameter,
            # so achieve via 3 'forward' turns
            for _ in range(3):
                # ignore move as it is part of the solve, not the user or scramble
                rotate(move["direction"], ignore_moves=True)
        else:  # if not rotation must be turn
            # not move["backwards"] to always undo the move
            # ignore move as part of solve
            turn(move["direction"], move["number"], not move["backwards"], True)
        if len(moves) == 0:  # must be solved
            return False
        else:
            return True  # continue solving


class Timer:
    """This class handles timing how long it takes the user to complete a solve"""

    def __init__(self):
        self.start_time = 0.0
        """The time since epoch that the timer was started
        :type: float"""
        self.end = 0.0
        """The time since epoch that the timer was stopped
        :type: float"""
        self.elapsed = 0.0
        """The amount of time that has elapsed since the timer was started
        :type: float"""
        self.exists = False
        """Whether the timer has ever been started for this solve
        :type: bool"""
        self.running = False
        """Whether the timer is actively running
        :type: bool"""

    def start(self):
        """Starts the timer and marks it as running"""
        self.exists = True
        self.running = True
        self.start_time = time.time()

    def stop(self):
        """Gets the final time elapsed and stops the timer"""
        self.update()
        self.running = False

    def delete(self):
        """Marks the timer as not having run for the current solve"""
        self.exists = False

    def update(self):
        """Updates the time elapsed if the timer is running"""
        if self.running:
            self.end = time.time()
            self.elapsed = self.end - self.start_time

    def display_elapsed(self):
        """
        Creates a text image displaying the time elapsed

        :return: The text image
        :rtype: pygame.Surface
        """
        # if time is less than a minute
        if self.elapsed < 60:  # display time as seconds and milliseconds
            image = interface.text(
                str(round(self.elapsed, 3)) + " seconds",  # round to milliseconds
                data.default_font,
                BLACK,
                default_colour,
            )
        else:  # display time as minutes and seconds
            image = interface.text(
                str(int(self.elapsed / 60))  # minutes
                + "m "
                + str(int(self.elapsed % 60))  # seconds
                + "s ",
                data.default_font,
                BLACK,
                default_colour,
            )

        return image
