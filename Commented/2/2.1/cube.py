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


def cube_net(default_colour):
    """
    Returns image of cube net
    
    :param default_colour: the RGB background colour to use
    :type default_colour: tuple[int, int, int]
    :return: the pygame.Surface image of the cube net
    :rtype: object
    """
    surf = pygame.Surface((720, 540))
    surf.fill(default_colour)
    colour_3d_array = used_cube

    def square(colour):
        """
        Creates the image of a single square
        
        :param colour: RGB value
        :type colour: tuple[int, int, int]
        :return: the pygame.Surface square image
        :rtype: object
        """
        surf = pygame.Surface((50, 50))
        surf.fill(colour)
        return surf

    def row(colour_list):
        """
        Creates the image of a row of 3 squares
        
        :param colour_list: List len(3) of RGB values
        :type colour_list: list[tuple[int, int, int],
                                tuple[int, int, int],
                                tuple[int, int, int]
                                ]
        :return: the pygame.Surface row image
        :rtype: object
        """
        surf = pygame.Surface((170, 50))  # 170, 50
        surf.fill(default_colour)
        for i in range(3):
            # iterates alongside the list of colours,
            # getting a square with the respective colour and blitting it to calculated position
            # i * 50 ensures the square is blitted after the previous one; not inside it
            # i * 10 adds 10 spacing between the cubes
            surf.blit(square(colour_list[i]), (i * 50 + i * 10, 0))
        return surf

    def face(colour_array):
        """
        Creates one face (side) from 3 rows
        
        :param colour_array: 2D array of RGB values [row1, row2, row3]
        :type colour_array: list[list[
                                    tuple[int, int, int],
                                    tuple[int, int, int],
                                    tuple[int, int, int]
                                    ],
                                list[
                                    tuple[int, int, int],
                                    tuple[int, int, int],
                                    tuple[int, int, int]
                                ],
                                list[
                                    tuple[int, int, int],
                                    tuple[int, int, int],
                                    tuple[int, int, int]
                                ]
                            ]
        :return: the pygame.Surface face image
        :rtype: object
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


def cube_3d(default_colour, default=False):
    """
    Returns the 3d cube image, will be centered if blitted to 0,0
    Uses slanted images/optical illusions to appear 3d
    
    :param default_colour: the RGB background colour to be used
    :type default_colour: tuple[int, int, int]
    :param default: whether the default solved cube should be used for the image
    :type default: bool
    :return: the pygame.Surface cube image
    :rtype: object
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
            :return: the pygame.Surface square image
            :rtype: object
            """
            surf = pygame.Surface((50, 75))
            surf.fill(default_colour)
            pygame.draw.polygon(surf, colour, ((0, 25), (50, 0), (50, 50), (0, 75)))
            return surf

        def row(colour_list):
            """
            Creates a slanted row of 3 squares
            
            :param colour_list: List 3 of RGB values
            :type colour_list: list[tuple[int, int, int],
                                    tuple[int, int, int],
                                    tuple[int, int, int]
                                    ]
            :return: the pygame.Surface row image
            :rtype: object
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
            
            :param colour_array: 2D array of RGB values
            :type colour_array: list[list[
                                        tuple[int, int, int],
                                        tuple[int, int, int],
                                        tuple[int, int, int]
                                        ],
                                    list[
                                        tuple[int, int, int],
                                        tuple[int, int, int],
                                        tuple[int, int, int]
                                        ],
                                    list[
                                        tuple[int, int, int],
                                        tuple[int, int, int],
                                        tuple[int, int, int]
                                        ]
                                    ]
            :return: the pygame.Surface row image
            :rtype: object
            """
            surf = pygame.Surface((165, 250))
            surf.fill(default_colour)
            for i in range(3):
                # 55 includes 5 pixels spacing
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
            :return: the pygame.Surface square image
            :rtype: object
            """
            surf = pygame.Surface((50, 75))
            surf.fill(default_colour)
            pygame.draw.polygon(surf, colour, ((0, 0), (50, 25), (50, 75), (0, 50)))
            return surf

        def row(colour_list):
            """
            Creates the image of a row of 3 squares
            
            :param colour_list: List of RGB values
            :type colour_list: list[tuple[int, int, int],
                                    tuple[int, int, int],
                                    tuple[int, int, int]
                                    ]
            :return: the pygame.Surface row image
            :rtype: object
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
            
            :param colour_array: 2D array of RGB values
            :type colour_array: list[list[
                                        tuple[int, int, int],
                                        tuple[int, int, int],
                                        tuple[int, int, int]
                                        ],
                                    list[
                                        tuple[int, int, int],
                                        tuple[int, int, int],
                                        tuple[int, int, int]
                                        ],
                                    list[
                                        tuple[int, int, int],
                                        tuple[int, int, int],
                                        tuple[int, int, int]
                                        ]
                                    ]
            :return: the pygame.Surface face image
            :rtype: object
            """
            surf = pygame.Surface((165, 250))
            surf.fill(default_colour)
            for i in range(3):
                # 55 includes 5 pixels spacing
                surf.blit(row(colour_array[i]), (0, 55 * i))
            return surf

        # positioned below top of front face with 5 pixels spacing
        surf.blit(face(colour_3d_array[1]), (40, 90))

    def top():
        """
        Draws the top face of the cube to the surf, it s a horizontally stretched square
        
        :rtype: None
        """

        def square(colour):
            """
            Creates a horizontally stretched cube of solid colour
            
            :param colour: RGB values
            :type colour: tuple[int, int, int]
            :return: the pygame.Surface square image
            :rtype: object
            """
            surf = pygame.Surface((100, 50))
            surf.fill(default_colour)
            pygame.draw.polygon(surf, colour, ((50, 0), (100, 25), (50, 50), (0, 25)))
            surf.set_colorkey(default_colour)
            return surf

        def row(colour_list):
            """
            Creates the image of a row of 3 squares
            
            :param colour_list: List of RGB values
            :type colour_list: list[tuple[int, int, int],
                                    tuple[int, int, int],
                                    tuple[int, int, int]
                                    ]
            :return: the pygame.Surface row image
            :rtype: object
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
            
            :param colour_array: 2D array of RGB values
            :type colour_array: list[list[
                                        tuple[int, int, int],
                                        tuple[int, int, int],
                                        tuple[int, int, int]
                                        ],
                                    list[
                                        tuple[int, int, int],
                                        tuple[int, int, int],
                                        tuple[int, int, int]
                                        ],
                                    list[
                                        tuple[int, int, int],
                                        tuple[int, int, int],
                                        tuple[int, int, int]
                                        ]
                                    ]
            :return: the pygame.Surface face image
            :rtype: object
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


def cube_guide(default_colour):
    """
    Draws the cube guide using the default image of the cube
    
    :param default_colour: the RGB background colour to use
    :type default_colour: tuple[int, int, int]
    :return: the pygame.Surface cube guide image
    :rtype: object
    """
    surf = pygame.Surface((500, 500))
    surf.fill(default_colour)
    colour_3d_array = used_cube
    colour = BLACK  # bad idea if default_colour is black
    if default_colour == BLACK:  # simple error check
        print("BAD idea, change cube_guide colour first")
        # TODO: implement better error check

    def arrow(colour):
        """
        Draws an arrow
        
        :param colour: RGB colour of the arrow
        :type colour: tuple[int, int, int]
        :return: the pygame.Surface arrow image
        :rtype: object
        """
        surf = pygame.Surface((100, 100))
        surf.fill(default_colour)

        pygame.draw.polygon(
            surf,
            colour,
            ((13, 13), (50, 0), (63, 63), (50, 50), (50, 95), (25, 80), (25, 25)),
        )
        surf.set_colorkey(default_colour)  # remove the default colour
        # so it can be seen through
        return surf

    # draw the default cube
    surf.blit(cube_3d(default_colour, True), (50, 50))

    # top arrows
    # positioned through trial and error
    surf.blit(arrow(BLACK), (80, 63))
    surf.blit(arrow(BLACK), (140, 95))
    surf.blit(arrow(BLACK), (190, 123))

    # right arrows - undfinished
    arrow = pygame.transform.rotate(arrow(BLACK), 90)
    surf.blit(arrow, (200, 200))

    return surf


def turn(row_col, number, backwards=False, ignore_moves=False):
    """
    Turn 1 row or column once, default is row to the right, column goes up
    
    :type row_col: bool
    :type number: int
    :type backwards: bool
    :type ignore_moves: bool
    :param row_col: True=row, False=column
    :param number: the number to do, left to right or top to bottom
    :param backwards: do the opposite of the move/do the move 3 times if true
    :param ignore_moves: whether to add the move to the moves list
    :rtype: None
    """
    if not ignore_moves:
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

        if row_col:
            # turn the row
            used_cube[2][n], used_cube[3][n], used_cube[0][n], used_cube[1][n] = (
                face1[n],
                face2[n],
                face3[n],
                face0[n],
            )
            if number == 0:
                used_cube[4] = numpy.rot90(
                    used_cube[4], k=1, axes=(0, 1)
                )  # rotate the top face
            elif number == 2:
                used_cube[5] = numpy.rot90(
                    used_cube[5], k=1, axes=(1, 0)
                )  # rotate the bottom face
        else:
            # turn the column
            for i in range(3):
                used_cube[1][i][n] = face5[i][n]
                # 2-i flips the row number for the back
                # 2 - n flips the column number for the back
                used_cube[5][2 - i][n] = face3[i][2 - n]
                used_cube[3][2 - i][2 - n] = face4[i][n]
                used_cube[4][i][n] = face1[i][n]

            if number == 0:
                used_cube[0] = numpy.rot90(
                    used_cube[0], k=1, axes=(0, 1)
                )  # rotate left face
            elif number == 2:
                used_cube[2] = numpy.rot90(
                    used_cube[2], k=1, axes=(1, 0)
                )  # rotate right face


def rotate(axis, ignore_moves=False):
    """
    Rotates the view of the cube without changing layout
    
    :param axis: x, y, z
    :type axis: str
    :param ignore_moves: whether to add the move to the moves list
    :type ignore_moves: bool
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

    if not ignore_moves:
        moves.append({"rotation": True, "direction": axis})

    if axis == "x":
        for i in range(3): # equivalent to a rotation along the x axis
            turn(True, i, ignore_moves=True)
    elif axis == "y":
        for i in range(3): # equivalent to a rotation along the y axis
            turn(False, i, ignore_moves=True)
    elif axis == "z": # equivalent to a rotation along the z axis
        # rotate the front and back faces
        used_cube[1] = numpy.rot90(used_cube[1], k=1, axes=(1, 0))
        used_cube[3] = numpy.rot90(used_cube[3], k=1, axes=(0, 1))

        for j in range(3): #required a lot of manual testing
            # carefully test any changes
            for i in range(3):
                used_cube[0][j][2 - i] = face5[i][j]
                used_cube[4][j][2 - i] = face0[i][j]
                used_cube[2][j][2 - i] = face4[i][j]
                used_cube[5][j][2 - i] = face2[i][j]


def scramble():
    """
    Randomly scramble the cube by making between 15 and 25 moves
    
    :rtype: None
    """
    for _ in range(randint(15, 25)):
        # randomise every aspect of each turn
        direction = bool(randint(0, 1))
        number = randint(0, 2)
        backwards = bool(randint(0, 1))

        turn(direction, number, backwards)


class Solver: # TODO: comments from here on ish = should param be attr or something?
    """
    Solve the cube, one turn per game loop

    The solve function must be called once per game loop
    until it returns False
    to completely solve the cube

    The attribute first should be updated to True before each complete solve
    """
    def __init__(self):
        self.first = True
        """
        If it is the first move of the solve
        
        :type: bool"""
        self.sleep_time = 0.2
        """
        The amount of time to wait between each move

        :type: float
        """

    def solve(self):
        """
        Does the reverse of the last done move
        
        :return: False if the cube is solved
        :rtype: bool
        """

        # guard clauses
        if self.check_solved():
            return False
        if len(moves) == 0:
            return False

        # calculate time to wait between move
        if self.first:
            if len(moves) > 0:
                # every solve should take 5 seconds regarless of moves required, although this can be affected by hardware limitations
                self.sleep_time = 5 / len(moves)
                self.first = False
            else:
                # wait upon every button press so the user knows it has 'worked'
                # even when the cube is aready solved
                self.sleep_time = 1


        move = moves.pop() # get the move dictionary
        if "rotation" in move.keys(): # check if the move was a rotation
            for _ in range(3): #rotate does not have a backwards parameter, so achieve via 3 'forward' turns
                rotate(move["direction"], ignore_moves=True) #ignore move as it is part of the solve, not the user or scramble
        else: # if not rotation must be turn
            # not move["backwards"] to always undo the move
            # ignore move as part of solve
            turn(move["direction"], move["number"], not move["backwards"], ignore_moves=True)

        if len(moves) == 0: # must be solved
            return False
        else:
            return True  # continue solving

    def check_solved(self):
        """
        Checks whether the cube is in a solved state
        
        :return: If the cube is solved
        :rtype: bool
        """
        not_solved = False
        for i in range(6): # face
            for j in range(3): # row
                for k in range(3): # column
                    # checks for any square not the same colour as the middle square on the same face
                    # numpy.all handles it being a tuple comparison
                    if not numpy.all(used_cube[i][j][k] == used_cube[i][1][1]):
                        not_solved = True
        return not not_solved

