"""
This file contains all the features of the program available to the user

These provide additional functionality
beyond the basic turn and rotation functions of the cube

black, isort and flake8 used for formatting
"""

import copy
import time
from random import randint

import game_data as gd
import interface
import numpy
import pygame
import tools
import user_data as ud
from cube import rotate, turn
from game_data import BLACK, default_colour, default_cube, default_font
from validation import ValidateScreenPositions

val = ValidateScreenPositions(1600, 900)


def scramble():
    """
    Randomly scrambles the cube by making between 15 and 25 moves randomly

    :rtype: None
    """
    # reset the cube
    gd.used_cube = copy.deepcopy(default_cube)

    count = randint(15, 25)
    gd.scrambler_count = count
    for _ in range(count):
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
        if gd.moves.size() == 0 or self.check_solved():
            return False

        # calculate time to wait between move
        if self.first:
            if gd.moves.size() > 0:
                # every solve should take 5 seconds regardless of moves required,
                # although this can be affected by hardware limitations
                self.sleep_time = 5 / gd.moves.size()
                self.first = False
            else:
                # wait upon every button press so the user knows it has 'worked'
                # even when the cube is already solved
                self.sleep_time = 1

        return self.pop_move()

    @staticmethod
    def check_solved():
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
                    if not numpy.all(gd.used_cube[i][j][k] == gd.used_cube[i][1][1]):
                        not_solved = True
        # sys.exit()
        return not not_solved

    @staticmethod
    def pop_move():
        """
        Removes a move from the moves list and does the reverse

        :return: False if the cube is solved, True otherwise
        :rtype: bool
        """
        # guard clause
        if gd.moves.size() == 0:
            return False

        move = gd.moves.pop()  # get the move dictionary
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
        if gd.moves.size() == 0:  # must be solved
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
        gd.start_time = self.start_time

    def stop(self):
        """Gets the final time elapsed and stops the timer"""
        self.update()
        self.running = False

    def delete(self):
        """Marks the timer as not having run for the current solve"""
        self.exists = False
        self.running = False
        gd.time_taken = 0.0
        gd.start_time = 0.0

    def update(self):
        """Updates the time elapsed if the timer is running"""
        if self.running:
            self.end = time.time()
            self.elapsed = self.end - self.start_time
            gd.time_taken = self.elapsed

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
                gd.default_font,
                BLACK,
                default_colour,
            )
        else:  # display time as minutes and seconds
            image = interface.text(
                str(int(self.elapsed / 60))  # minutes
                + "m "
                + str(int(self.elapsed % 60))  # seconds
                + "s ",
                gd.default_font,
                BLACK,
                default_colour,
            )

        return image


class DisplayHistory:
    """This class manages fetching and displaying the user's game history"""

    def __init__(self, screen, pos):
        """
        :param screen: The screen that this is to be blitted to
        :param pos: The top-left position that this is to be blitted to: x,y
        :type screen: pygame.Surface
        :type pos: list[int] or tuple[int, int]
        """
        self.screen = screen
        self.pos = pos

        self.history = []
        """A 2D array where each row is a game and each column is text to display
        :type: list[list]"""

        self.y_offset = 0
        """The amount the image should be offset vertically 
        - the amount it has been scrolled
        :type: int"""

    def format_history(self):
        """Formats the user's game history into a 2D array
        that contains elements to be displayed"""
        history_data = ud.game_history.get_history()
        self.history = []

        for i in range(len(history_data)):  # one game
            game = history_data[i]
            game_array = []

            # date of solve
            game_array.append(str(time.strftime("%d/%m/%Y", time.localtime(game[5]))))

            # solved or unsolved
            if game[6]:
                game_array.append("SOLVED")
            else:
                game_array.append("UNSOLVED")

            # move count for the user
            game_array.append(str(game[1] - game[3]))

            # time taken
            game_array.append(str(time.strftime("%H:%M:%S", (time.gmtime(game[4])))))

            # hints used
            game_array.append(str(game[7]))

            self.history.append(game_array)

    def get_image(self):
        """
        Creates a text image displaying the user's game history

        This will get and format the user's game history before creating the image
        """
        self.format_history()

        img_height = 0  # will vary on size of history
        img_list = []  # will vary on size of history, to be added to returned surf

        # header
        img = interface.text(
            "  DATE  |  STATE  |  MOVES  |  TIME  |  HINTS USED  ",
            default_font,
            BLACK,
            default_colour,
        )
        img_height += img.get_height()
        img_width = img.get_width()
        img_list.append(img)

        for i in range(len(self.history)):
            img = interface.text(
                self.history[i][0]
                + " | "
                + self.history[i][1]
                + " | "
                + self.history[i][2]
                + " | "
                + self.history[i][3]
                + " | "
                + self.history[i][4],
                default_font,
                BLACK,
                default_colour,
            )
            img_height += img.get_height()
            img_list.append(img)

        surf = pygame.Surface((img_width, img_height))
        surf.fill(default_colour)
        for i in range(len(img_list)):
            surf.blit(img_list[i], (0, i * img_list[i].get_height()))

        return surf

    def update(self):
        """
        Updates the history image and blits it to the screen

        This takes into account the y_offset (amount scrolled) and adjusts it vertically
        """
        img = self.get_image()
        self.screen.blit(
            img, [self.pos[0] - img.get_width() // 2, self.pos[1] + self.y_offset]
        )

    def scroll(self, amount):
        """
        Changes the y position the image is blitted to,
        which allows it to be scrolled

        :param amount: The amount to scroll by, positive or negative
        :type amount: int
        """
        self.y_offset += amount


class Leaderboard:
    """This class manages creating and displaying the leaderboard"""

    class Entry:
        """
        This class represents an entry in the leaderboard

        This is deigned to be used by tools.File
        and as such all its attributes must also be parameters
        """

        def __init__(self, id, name, time, moves):
            """
            :param id: a unique identifier for each object
            :type id: int
            :param name: the username of the player
            :type name: str
            :param time: the time taken to solve the cube
            :type time: float
            :param moves: the number of moves the user did to solve the cube
            :type moves: int
            """
            self.id = id
            self.name = name
            self.time = time
            self.moves = moves

    leaderboard_file = tools.File("leaderboard.txt", Entry)

    def __init__(self, screen, pos):
        """
        :param screen: the screen that this is to be blitted to
        :type screen: pygame.Surface
        :param pos: the centre position that this is to be blitted to: x,y
        :type pos: list[int] or tuple[int, int]
        """
        self.screen = screen
        self.pos = pos

        self.entries = self.leaderboard_file.get_list()
        """The top ten quickest solve times, should be kept in in order
        :type: list[Entry]"""
        self.sort()

    def update_list(self, time, moves):
        """
        Checks if the user has a leaderboard worthy time and updates the ordered list

        :param time: the time taken to solve the cube
        :type time: float
        :param moves: the number of moves the user did to solve the cube
        :type moves: int
        """
        if len(self.entries) < 10:  # add new entry
            self.entries.append(
                Leaderboard.Entry(len(self.entries), ud.Manager.username, time, moves)
            )
        elif self.entries[-1].time <= time:  # if no new entry, stop
            return

        elif self.entries[-1].time > time:  # if new entry replace slowest
            self.entries[-1] = Leaderboard.Entry(
                self.entries[-1].id, ud.Manager.username, time, moves
            )

        self.sort()
        self.leaderboard_file.replace_list(self.entries)
        self.leaderboard_file.save()

    def sort(self):
        """Sorts the entries list by time"""
        self.entries.sort(key=lambda Entry: Entry.time)

    def update(self):
        """Updates the leaderboard image and blits it to the screen"""
        img = self.get_image()
        self.screen.blit(img, img.get_rect(center=self.pos))

    def get_image(self):
        """Creates the image of the leaderboard"""
        img_height = 0
        img_list = []

        # header
        img = interface.text(
            "  POSITION  |  NAME  |  TIME  |  MOVES  ",
            default_font,
            BLACK,
            default_colour,
        )
        img_height += img.get_height()  # ensures the surd isn't too small
        img_width = img.get_width()
        img_list.append(img)

        for i in range(len(self.entries)):
            img = interface.text(
                str(i + 1)
                + " | "
                + self.entries[i].name
                + " | "
                + str(round(self.entries[i].time, 3))
                + " | "
                + str(self.entries[i].moves),
                default_font,
                BLACK,
                default_colour,
            )
            img_height += img.get_height()
            img_list.append(img)

        surf = pygame.Surface((img_width, img_height))
        surf.fill(default_colour)
        for i in range(len(img_list)):
            surf.blit(img_list[i], (0, i * img_list[i].get_height()))

        return surf
