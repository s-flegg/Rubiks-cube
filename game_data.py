"""
This file contains global data and settings information

This data is used by multiple files in the program. It may be edited here, or it may be
provided to the user as settings for them to change.

black, isort and flake8 used for formatting
"""
import copy

import pygame
from pygame import freetype

pygame.font.init()
pygame.freetype.init()

# colours
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
YELLOW = [255, 255, 0]
ORANGE = [255, 165, 0]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
GREY = [169, 169, 169]

default_colour = GREY
guide_arrow_colour = BLACK


# fonts
default_font = pygame.freetype.SysFont("calibri", 20)
guide_font = pygame.freetype.SysFont("calibri", 20, bold=True)


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
class MoveStack:
    """A stack for managing the moves made by the user and scrambler"""

    def __init__(self):
        self.stack = []

    def push(self, move):
        """
        Pushes a move onto the stack

        :param move: move should be in the format
            {
                "direction": True for row, False for column,
                "number": row or column number,
                "backwards": If the move was backwards (left or down)
            }
            for a turn or the following for a rotation:
            {
                "rotation": True,
                "direction": "x" or "y" or "z"
            }
        :type move: dict
        """
        if move.keys() == {"direction", "number", "backwards"} or move.keys() == {
            "rotation",
            "direction",
        }:
            self.stack.append(move)
        else:
            raise ValueError("Invalid dict keys")

    def pop(self):
        """
        Pops a move off the stack

        :return: move
        :rtype: dict
        """
        return self.stack.pop()

    def clear(self):
        """Clears the stack"""
        self.stack = []

    def size(self):
        """
        :return: size of the stack
        :rtype: int
        """
        return len(self.stack)

    def get_stack(self):
        """
        :return: the list of moves stored as dictionaries
        :rtype: list[dict]
        """
        return self.stack

    def set_stack(self, stack):
        """
        Replaces the current stack with the one provided

        :param stack: the list of moves stored as dictionaries
        :type stack: list[dict]
        """
        self.stack = stack


moves = MoveStack()
"""The MoveStack of moves that have been made by the user and the scrambler in order
:type: MoveStack"""
move_count = 0
"""The amount of moves made by the user and scrambler.
These will be on order in the moves list, but will be preceded by scrambler moves
:type: int"""
scrambler_count = 0
"""The amount of moves made by the scrambler
:type: int"""

# used for tracking time
start_time = 0.0
"""The time since epoch that the user started the solve/ started the scrambler
:type: float"""
time_taken = 0.0
"""The amount of time that has elapsed since the user started the solve
:type: float"""

# used for seeing if the solve is eligible for the leaderboard and for users knowledge
hints_used = False
"""Whether the user has used hints
:type: bool"""
solver_used = False
"""Whether the user has used the solver
:type: bool"""
solved = False
"""Whether the cube is solved
:type: bool"""
