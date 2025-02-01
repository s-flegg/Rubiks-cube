"""
This file contains useful tools for any program

As this file has been designed to work with any program all its functions are generic.

black, isort and flake8 used for formatting
"""

from os.path import isfile


class ObjectNotFound(Exception):
    """Indicates that an object was not found when searched for within a file"""

    def __init__(self, identifier, file):
        """
        :param identifier: the identifier of the object that was not found
        :type identifier: any
        :param file: the file that was searched
        :type file: str
        """
        super().__init__(f"Object not found | Identifier: {identifier} | File: {file}")


class File:
    """
    This class manages a list of objects in a file

    The list should be updated using the get_list and update_list functions.
    It should be saved with the save function.
    It contains the class objects.

    Individual objects can be got with the get_object function.
    Objects can be replaced with the update_object function.
    Objects can de removed with the remove_object function.

    Either the entire list should be modified or only single objects should be modified.
    These should not be sued together.
    """

    def __init__(self, file, cls):
        """
        :param file: the name of the file to store the data in, must be .txt
        :type file: str
        :param cls: the class of the data stored in the file, not an object
            cls(arg0, arg1, etc.) must call the constructor
            arg0 must be a unique identifier.
            the attributes self.'s must be the exact same as the parameters
        :type cls: class
        """
        self.name = file
        self.cls = cls

        self.list = []
        """The list of all data in the file
        :type list: list[object]"""

        # check file exists, create if it doesn't
        if not isfile(self.name):
            f = open(self.name, "w")
            f.close()
        self.read()

    @staticmethod
    def get_identifier(obj):
        """
        Returns the first key in the object's dictionary as a string

        The first key is considered the identifier, it is converted to a string to
        ensure thier are no errors during comparison

        :param obj: the object to get the identifier of
        :type obj: object

        :return: the identifier of the object
        :rtype: str
        """
        keys = list(obj.__dict__.keys())
        identifier = obj.__dict__[keys[0]]
        return str(identifier)

    def read(self):
        """
        Reads the file and updates self.list

        :rtype: None
        """
        f = open(self.name, "r")
        file_str = f.read()
        f.close()

        # check file isn't empty
        if file_str == "":
            return

        objects = file_str.split("\n")
        objects.pop()  # get rid of newline at end of file
        for obj in objects:
            self.list.append(
                self.cls(**eval(obj))  # convert string to dict and pass as kwargs
            )

    def sort(self):
        """
        Sorts the list

        :rtype: None
        """
        self.list.sort(key=lambda obj: self.get_identifier(obj))

    def search(self, target):
        """
        Finds the position of the target in the list, automatically orders the list

        :param target: the target to search for
        :type target: object
        :return: the position of the target, -1 if not found
        :rtype: int
        """

        def binary_search(lst, start_pos=0):
            """
            Recursive binary search using the identifier

            :param lst: the list section to search
            :type lst: list
            :param start_pos: the start position of the list section
            :type start_pos: int
            :return: the position of the target, -1 if not found
            :rtype: int
            """
            # empty list
            if len(lst) == 0:
                return -1

            mid = len(lst) // 2
            identifier = self.get_identifier(lst[mid])

            if identifier == target:
                return mid + start_pos
            elif identifier > target:
                return binary_search(lst[:mid], start_pos)
            else:
                return binary_search(lst[mid + 1 :], start_pos + mid + 1)

        self.sort()  # order the list
        target = str(target)  # for comparison to prevent errors
        return binary_search(self.list)

    def get_list(self):
        """Returns the list of objects"""
        return self.list

    def replace_list(self, lst):
        """
        Replaces the list of objects

        :param lst: the new list
        :type lst: list
        :rtype: None
        """
        self.list = lst

    def save(self):
        """Sorts self.list then replaces the file with it."""
        self.sort()
        f = open(self.name, "w")
        for obj in self.list:
            f.write(str(obj.__dict__) + "\n")
        f.close()

    def get_object(self, identifier):
        """
        Gets the object with the given identifier

        :param identifier: a unique identifier
        :type identifier: any
        :return: the object or raises exception ObjectNotFound if the object is not found
        :rtype: object
        """
        pos = self.search(identifier)
        if pos == -1:
            raise ObjectNotFound(identifier, self.name)
        return self.list[pos]

    def add_object(self, obj):
        """
        Adds the object to the list

        :param obj: the object to add
        :type obj: object
        :rtype: None
        """
        self.list.append(obj)
        self.sort()

    def update_object(self, identifier, obj):
        """
        Replaces the object with identifier with the given object.

        :param identifier: the identifier of the object to replace
        :type identifier: any
        :param obj: the new object to replace the old one
        :type obj: object
        :return: None or raises exception ObjectNotFound if the object is not found
        :rtype: None
        """
        pos = self.search(identifier)
        if pos == -1:
            raise ObjectNotFound(identifier, self.name)
        self.list[pos] = obj

    def remove_object(self, identifier):
        """
        Removes the object with the given identifier

        :param identifier: the identifier of the object to remove
        :type identifier: any
        :return: None or raises exception ObjectNotFound if the object is not found
        :rtype: None
        """
        pos = self.search(identifier)
        if pos == -1:
            raise ObjectNotFound(identifier, self.name)
        self.list.pop(pos)


# testing
if __name__ == "__main__":

    class Test:
        def __init__(self, arg0=None, arg1=None, arg2=None):
            self.arg0 = arg0
            self.arg1 = arg1
            self.arg2 = arg2

        def output(self):
            return str(self.arg0) + " " + str(self.arg1) + " " + str(self.arg2)

    file = File("test.txt", Test)
    file.sort()
    lst = file.get_list()
    # lst.append(Test('{a: b}', 3, 5))
    file.update_list(lst)
    file.save()
    print(lst)
    for cls in file.get_list():
        print(cls.output())
    pos = file.search("{")
    print(pos)
