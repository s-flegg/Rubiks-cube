"""
This file contains validation functions and error handling

black, isort and flake8 used for formatting
"""

import time


class InvalidScreenPosition(Exception):
    """This exception is raised when the screen position is invalid"""

    def __init__(self, pos):
        """
        :param pos: the x,y position that is invalid
        :type pos: tuple[int, int] or list[int]
        """
        super().__init__(f"Invalid Screen Position: {pos}")
        with open("error.txt", "a") as f:
            error_time = time.time()
            f.write(f"{error_time}  Invalid Screen Position: {pos} \n")


class ValidateScreenPositions:
    """
    This class contains a screen position validation function

    It will ensure a screen position is valid based on a 4k resolution screen
    and the size of the window being displayed to
    """

    def __init__(self, width, height):
        """
        :param width: the width of the screen window
        :param height: the height of the screen window
        :type width: int
        :type height: int
        """
        self.width = width
        self.height = height

    def run(self, pos):
        """
        Ensures a position is within the confines of the screen and 4k resolution

        This function will throw an error if the position is invalid.
        An invalid position is one that is outside the confines of the screen based
        width and height, or a 4k resolution screen.

        :param pos: the x,y position to check
        :type pos: tuple[int, int] or list[int]
        :return: the x,y screen position if it is valid, else raises an exception
        :rtype: tuple[int, int] or list[int]
        """
        if (
            pos[0] < 0
            or pos[0] > self.width
            or pos[0] > 3840
            or pos[1] < 0
            or pos[1] > self.height
            or pos[1] > 2160
        ):
            raise InvalidScreenPosition(pos)
        else:
            return pos

    def update_size(self, size):
        """
        Update the screen width and height

        :param size: the width and height of the window
        :type size: tuple[int, int] or list[int]
        """
        self.width = size[0]
        self.height = size[1]
