"""
This file handles loading and saving user data

This file handles a user's game history, details about their current game.
as well as loading and saving data to a file

black, isort and flake8 used for formatting
"""

import game_data as gd
import tools


# game history
class History:
    """This class manages the game history of the user"""

    def __init__(self):
        # do not change these as they are used for saving
        # they are directly aquired by self.__dict__ in the add method
        # even changing thier order will break things
        self.game_state = gd.used_cube
        """The 3D array of the cube state at the last move
        :type: list"""
        self.move_count = gd.move_count
        """The amount of moves made by the user. These will be on order in the moves list,
        but will be preceded by scrambler moves
        :type: int"""
        self.moves = gd.moves.get_stack()
        """The list of moves that have been made by the user and the scrambler in order
        :type: list"""
        self.scrambler_count = gd.scrambler_count
        """The amount of moves made by the scrambler
        :type: int"""
        self.time_taken = gd.time_taken
        """The amount of time that has elapsed since the user started the solve
        :type: float"""
        self.time_started = gd.start_time
        """The time since epoch that the user started the solve/ started the scrambler
        :type: float"""
        self.solved = gd.solved
        """Whether the cube is solved
        :type: bool"""
        self.hints_used = gd.hints_used
        """Whether the user has used hints
        :type: bool"""
        self.solver_used = gd.solver_used
        """Whether the user has used the solver
        :type: bool"""

        self.history_list = []
        """The list of all history records
        :type: list"""

    def add_game(self):
        """Adds the current game to game history using the game_data"""
        self.game_state = gd.used_cube
        self.move_count = gd.move_count
        self.moves = gd.moves.get_stack()
        self.scrambler_count = gd.scrambler_count
        self.time_taken = gd.time_taken
        self.time_started = gd.start_time
        self.solved = gd.solved
        self.hints_used = gd.hints_used
        self.solver_used = gd.solver_used
        # add attributes to history list
        # excluding history list itself
        self.history_list.append(list(self.__dict__.values())[:-1])

    def replace_history(self, history_list):
        """
        Replaces the history list, useful for when initailising with user's saved data

        :param history_list: the new history list
        :type history_list: list
        """
        self.history_list = history_list

    def get_history(self):
        """
        :return: the game history list
        :rtype: list
        """
        return self.history_list


game_history = History()
"""The class containing the history of the user's game
:type: History"""


class User:
    """
    A class containing the user data and methods to update it

    Designed for use with the Manager class and tools.File
    """

    def __init__(
        self,
        username=None,
        cube_state=gd.used_cube,
        start_time=gd.start_time,
        time_taken=gd.time_taken,
        moves=gd.moves.get_stack(),
        move_count=gd.move_count,
        scrambler_count=gd.scrambler_count,
        hints_used=gd.hints_used,
        solver_used=gd.solver_used,
        history=game_history.get_history(),
    ):
        """
        :param username: the unique identifier of the user
        :type username: str
        :param cube_state: the 3D array of the cube
        :type cube_state: list[list[list]]
        :param start_time: the time since epoch when the user started the solve
        :type start_time: float
        :param time_taken: the time elapsed ruing the solve
        :type time_taken: float
        :param moves: the list of moves that have been made
        :type moves: list[dict]
        :param move_count: the amount of moves that has been made
        :type move_count: int
        :param scrambler_count: the amount of scrambler moves that have been made
        :type scrambler_count: int
        :param hints_used: whether the user has used hints
        :type hints_used: bool
        :param solver_used: whether the user has used the solver
        :type solver_used: bool
        :param history: the game history of the user
        :type history: game_data.History
        """
        # due to the way the user data is saved and loaded
        # self. must match init param and username must be first
        self.username = username
        self.cube_state = cube_state
        self.start_time = start_time
        self.time_taken = time_taken
        self.moves = moves
        self.move_count = move_count
        self.scrambler_count = scrambler_count
        self.hints_used = hints_used
        self.solver_used = solver_used
        self.history = history

    def save(self, username=None):
        """
        Updates this class's attributes to the current game data

        Optionally updates the username

        :param username: the unique identifier of the user, defaults to None (no change)
        :type username: str, optional
        """
        if username is not None:
            self.username = username
        self.cube_state = gd.used_cube
        self.start_time = gd.start_time
        self.time_taken = gd.time_taken
        self.moves = gd.moves.get_stack()
        self.move_count = gd.move_count
        self.scrambler_count = gd.scrambler_count
        self.hints_used = (gd.hints_used,)
        self.solver_used = gd.solver_used
        self.history = game_history.get_history()

    def load(self):
        """Updates the current game data to this class's attributes"""
        gd.used_cube = self.cube_state
        gd.start_time = self.start_time
        gd.time_taken = self.time_taken
        gd.moves.set_stack(self.moves)
        gd.move_count = self.move_count
        gd.scrambler_count = self.scrambler_count
        gd.hints_used = (self.hints_used,)
        gd.solver_used = self.solver_used
        game_history.replace_history(self.history)


class Manager:
    """This class handles data in a txt file"""

    user_file = tools.File("saves_data.txt", User)
    username = None
    obj = None

    @staticmethod
    def load(username):
        """
        Load the user data for the given username, or create a new user

        :param username: the unique username of the user
        :type username: str
        """
        Manager.username = username
        try:
            Manager.obj = Manager.user_file.get_object(Manager.username)
        except tools.ObjectNotFound:
            Manager.obj = User(Manager.username)
            Manager.user_file.add_object(Manager.obj)

        Manager.obj.load()

    @staticmethod
    def save(username=None):
        """
        Save the user data, and optionally change the username

        :param username: the new username, defaults to None
        :type username: str, optional
        """
        if username is not None:
            # replace the username
            Manager.obj = User(username)
            Manager.user_file.update_object(Manager.username, Manager.obj)
            Manager.username = username

        # save the data
        Manager.obj.save(Manager.username)
        Manager.user_file.update_object(Manager.username, Manager.obj)
        Manager.user_file.save()
