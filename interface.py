"""
This file contains some key elements of the interface to be used by other files

This file handles creating visual elements and user interface
to be displayed to the screen for the user.
DisplayOption and DisplayBar should be used together.

black, isort and flake8 used for formatting
"""


import pygame


class DisplayOption:
    """
    Creates a button with an image that changes size when hovered

    This class should be used with DisplayBar
    """

    def __init__(self, image_function, display_surf, pos, size, mult, action, bg_col):
        """
        :param image_function: the function to get the image to use as the button
        :param display_surf: the surface to display the button to
        :param pos: the position to display the button from the top left
        :param size: the x length and y length of the button
        :param mult: how much to increase the image size when hovered
        :param action: the function to run when the button is clicked
        :param bg_col: the RGB value of the background colour
        :type image_function: function
        :type display_surf: pygame.Surface
        :type pos: list[int] or tuple[int, int]
        :type size: list[int]
        :type mult: float
        :type action: function
        :type bg_col: tuple[int, int, int] or list[int]
        """
        self.image_function = image_function
        self.display_surf = display_surf
        self.pos = pos
        self.size = size
        self.last_size = size
        self.mult = mult
        self.act = action
        self.bg_col = bg_col
        self.image = self.get_image()

        self.last_size = self.size
        """The last x,y size of the button. Used for checking if the button is hovered
        :type last_size: list[int]"""

    def get_image(self):
        """
        Gets the image of the button in its current state

        :return: the image of the button
        :rtype: pygame.Surface
        """
        surf = pygame.Surface(self.size)
        cube = self.image_function()
        cube = pygame.transform.smoothscale(cube, self.size)
        cube.set_colorkey(self.bg_col)
        surf.blit(cube, (0, 0))
        return surf

    def update(self, mouse_pos, offset, mouse_up):
        """
        Update the button, checking if it is hovered or clicked

        :param mouse_pos: the x,y position of the mouse
        :param offset: the width and height to offset the button ensures its enlarged
            size does not overlap anything
        :param mouse_up: whether the mouse button has been clicked
        :type mouse_pos: tuple[int, int] or list[int]
        :type offset: list[int]
        :type mouse_up: bool
        :return: whether the button is hovered
        :rtype: bool
        """
        # calculate the position of the button with its offset
        pos = [0, 0]
        pos[0] = self.pos[0] + offset[0]
        pos[1] = self.pos[1] + offset[1]

        # calculate the centre of the button accounting for possible enlargement
        # and offset
        width = self.last_size[0]
        height = self.last_size[1]
        centre = width // 2 + pos[0], height // 2 + pos[1]

        if self.image.get_rect(center=centre).collidepoint(mouse_pos):  # if hovered
            if mouse_up:  # if pressed
                self.act()
            # save same size so it can be restored
            temp = self.size.copy()
            # enlarge the button
            self.size[0], self.size[1] = (
                self.size[0] * self.mult,
                self.size[1] * self.mult,
            )
            self.last_size = self.size
            # get the enlarged image
            self.image = self.get_image()
            # restore size to the original state so it can be displayed
            self.size = temp

            self.display_surf.blit(self.image, pos)
            return True
        else:  # if not hovered
            self.image = self.get_image()
            self.last_size = self.size
            self.display_surf.blit(self.image, pos)
            return False


class DisplayBar:
    """For creating a bar of DisplayObject in a row/column"""

    def __init__(self, object_list, row):
        """
        :param object_list: list of DisplayOption in sequential order
        :param row: if the buttons are in a row(True) or column(False)
        :type object_list: list[DisplayOption]
        :type row: bool
        """
        self.object_list = object_list
        self.row = row

    def update(self, mouse_pos, mouse_up):
        """
        Updates each button in the bar and offsets then if one is hovered

        :param mouse_pos: the x,y position of the mouse
        :param mouse_up: whether the mouse button has been clicked
        :type mouse_pos: tuple[int, int] or list[int]
        :type mouse_up: bool
        :rtype: None
        """
        offset = [0, 0]
        for i in range(len(self.object_list)):
            # update the button and check if it is hovered
            if self.object_list[i].update(mouse_pos, offset, mouse_up):
                if self.row:
                    # set offset to the difference in size
                    offset[0] = (
                        self.object_list[i].last_size[0] - self.object_list[i].size[0]
                    )
                else:  # column
                    offset[1] = (
                        self.object_list[i].last_size[1] - self.object_list[i].size[1]
                    )


def text(text, font, foreground_colour, background_colour):
    """
    Returns an image of the text

    :param text: the text to display
    :param font: the font to use
    :param foreground_colour: the RGB value of the foreground colour
    :param background_colour: the RGB value of the background colour
    :type text: str
    :type font: pygame.freetype.Font
    :type foreground_colour: tuple[int, int, int] or list[int]
    :type background_colour: tuple[int, int, int] or list[int]
    :return: the image of the text
    :rtype: pygame.Surface
    """
    # render returns surface, rect so we only need surface
    surface, _ = font.render(
        text=text, fgcolor=foreground_colour, bgcolor=background_colour
    )
    image = surface.convert_alpha()  # optimisation
    return image
