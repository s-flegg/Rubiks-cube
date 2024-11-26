from Login import encryption
from os.path import isfile

db = UserList("user_data.txt")


class User:
    def __init__(self, username, cube_state, timer):
        self.username = username
        self.cube_state = cube_state
        self.timer = timer
        self.data_list = [username, cube_state, timer]

class UserList:
    def __init__(self, file_name="user_data.txt"):
        self.file=file_name
        # ensure the file exists
        if not isfile(self.file):
            f = open(self.file, "w")
            f.close()

        self.users = []
        self.read
        





# TODO: load at startup, cube state, leaderboard hostpry, other stuff?
# TODO: binary searach times to place user in leaderboard
