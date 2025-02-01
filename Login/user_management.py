from os.path import isfile

from .encryption import string as estr

# used to maintain consistent in separating user attributes
# newlines separate users
seperator = "///"

class User:
    """The class that holds info about users"""

    def __init__(self, username, password, question, answer):
        """
        :param username: should be unique and encrypted
        :param password: should be encrypted
        :param question: security question, should be encrypted
        :param answer: answer to question, should be encrypted
        """
        self.username = username
        self.password = password
        self.question = question
        self.answer = answer

    # accessors
    def get_username(self):
        """
        :return: decrypted username
        :rtype: str
        """
        return estr(self.username, False)

    def get_password(self):
        """
        :rtype: str
        :return: encrypted username, compare encryption to check
        """
        return self.password

    def get_question(self):
        """
        :rtype: str
        :return: decrypted question
        """
        return estr(self.question, False)

    def get_answer(self):
        """
        :rtype: str
        :return: encrypted answer, compare encryptions to check
        """
        return self.answer

    # modifiers
    def set_username(self, u):
        """
        :param u: username is encrypted
        :type u: str
        """
        self.username = u

    def set_password(self, p):
        """
        :param p: password is encrypted
        :type p: str
        """
        self.password = p

    def set_question(self, q):
        """
        :param q: question is encrypted
        :type q: str

        """
        self.question = q

    def set_answer(self, a):
        """
        :param a: answer is encrypted
        :type a: str
        """
        self.answer = a

    # behaviours
    def check_password(self, to_check):
        """
        :rtype: bool
        """
        return self.password == to_check

    def check_answer(self, to_check):
        """
        :rtype: bool
        """
        return self.answer == to_check

    # comparison operators
    # used for comparing objects of class
    def __eq__(self, arg):
        return self.get_username() == arg.get_username()

    def __lt__(self, arg):
        return self.get_username() < arg.get_username()

    def __gt__(self, arg):
        return self.get_username() > arg.get_username()

    def __str__(self):
        return (
            self.username
            + seperator
            + self.password
            + seperator
            + self.question
            + seperator
            + self.answer
        )


class UserList:
    """Manages list of all Users, data about them, interactions with them, stores in a file"""

    def __init__(self, file_name="users.txt"):
        self.file = file_name
        # ensure the file exists
        if not isfile(self.file):
            f = open(self.file, "w")
            f.close()

        self.list = []
        self.read()
        self.sort()

    def read(self):
        """Updates self.list"""
        f = open(self.file, "r")
        file_str = f.read()
        f.close()

        # check file isn't empty
        if file_str != "":
            users = file_str.split("\n")
            users.pop()  # get rid of newline at end of file
            for i in range(len(users)):
                attrs = users[i].split(seperator)
                user = User(attrs[0], attrs[1], attrs[2], attrs[3])
                self.list.append(user)

    def sort(self):
        """
        Merge sort list, compares User directly
        :rtype: None

        """
        lst = self.list

        def merge_sort(lst):
            """
            Recursive merge sort
            :rtype: None
            """
            # split into lists of 1
            if len(lst) > 1:
                # split list
                mid = len(lst) // 2
                left = lst[:mid]
                right = lst[mid:]

                # recursively sort list
                merge_sort(left)
                merge_sort(right)

                # combine lists
                # left, right, sorted
                i, j, k = 0, 0, 0
                # while unsorted elements remain
                while i < len(left) and j < len(right):
                    # if left is lower add left to sorted list
                    if left[i] < right[j]:
                        lst[k] = lst[i]
                        # increase i as position i has been added to sorted list
                        i += 1
                    # else add right to sorted list
                    else:
                        lst[k] = right[j]
                        # increase j as j has been added to sorted list
                        j += 1
                    # increase k as position k is now filled
                    k += 1
                # cleanup
                while i < len(left):
                    lst[k] = left[i]
                    i += 1
                    k += 1
                while j < len(right):
                    j += 1
                    k += 1

        merge_sort(lst)

    def search(self, username):
        """
        :return: position in list or False is not found
        :type username: str
        :rtype int or bool
        """
        lst = self.list

        def binary(lst, pos=0):
            """
            Recursive binary search
            :param lst: list to sort
            :param pos: current position in list
            :rtype: int or bool
            """
            mid = len(lst) // 2

            # check if it doesn't exist
            if len(lst) == 0:
                return False

            elif len(lst) == 1 and lst[0].get_username() != username:
                return False

            elif username == lst[mid].get_username():
                return pos + mid
            elif username > lst[mid].get_username():
                return binary(lst[mid:], mid + pos)
            elif username < lst[mid].get_username():
                return binary(lst[:mid], pos)

        return binary(lst)

    def check_password(self, username, password):
        """
        :type username: str
        :param username: should be plaintext
        :type password: str
        :param password: should be plaintext
        :rtype: bool
        """
        pos = self.search(username)
        # prevents error on empty file
        if pos is not False:
            return self.list[pos].check_password(estr(password, True))

    def change_password(self, username, password):
        """
        :type username: str
        :param username: account to change password for
        :type password: str
        :param password: new password
        """
        pos = self.search(username)
        if pos is not False:
            self.list[pos].set_password(estr(password, True))

    def get_question(self, username):
        """
        Returns question or false if user doesn't exist
        :type username: str
        :param username: username to get question for
        :rtype: str or bool
        """
        pos = self.search(username)
        if pos is not False:
            return self.list[pos].get_question()
        else:
            return False

    def check_answer(self, username, answer):
        """
        :type username: str
        :param username: should be plaintext
        :type answer: str
        :param answer: should be plaintext
        :rtype: bool
        """
        pos = self.search(username)
        # prevents error on empty file
        if pos is not False:
            return self.list[pos].check_answer(estr(answer, True))

    def add_user(self, username, password, question, answer):
        """
        Creates new User and adds to the list, will ensure valid username
        :type username: str
        :param username: unencrypted
        :type password: str
        :param password: unencrypted
        :type question: str
        :param question: unencrypted
        :type answer: str
        :param answer: unencrypted
        :return: True if successful, False if invalid username
        :rtype: bool
        """
        if self.search(username) is not False:
            return False
        else:
            user = User(
                estr(username, True),
                estr(password, True),
                estr(question, True),
                estr(answer, True),
            )
            self.list.append(user)
            self.sort()
            self.save()
            return True

    def remove(self, username):
        """
        :type username: str
        :param username: user to be removed
        """
        pos = self.search(username)
        # prevents error if user doesn't exist
        if pos is not False:
            self.list.remove(pos)

    def save(self):
        """Overwrites file with updated list"""
        with open(self.file, "w") as f:
            for i in range(len(self.list)):
                f.write(str(self.list[i]) + "\n")


if __name__ == "__main__":
    u = UserList()
    # u.add_user("dev", "dev", "dev", "dev")
    print(u.list[0])
    print(u.check_password("dev", "dev"))
    # print(estr("dev", True))
