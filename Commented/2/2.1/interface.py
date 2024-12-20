import pygame


class DisplayButton():
    """
    Creates a button with an image that changes size when hovered

    .update should be run every game loop
    """
    def __init__(self, image_function, display_surf, pos, size, mult, action, bg_col):
        """
        :param image_function: the function to get the image of the cube
        :param display_surf: the pygame surface to display to
        :param pos: the x and y postion to draw to
        :param size: the hoizontal and vertical length the button should be
        :param mult: the size multiplier that should be applied to the button when it is hovered
        :param action: the procedure to run when the button is clicked
        :param bg_col: the RGb value of the background colour

        :type image_function: function
        :type display_surf: object
        :type pos: list[int, int]
        :type size: list[int, int]
        :type mult: float
        :type action: function
        :type bg_col: tuple[int, int, int]
        """
        self.image_function = image_function
        self.display_surf = display_surf
        self.pos = pos
        self.size = size
        self.mult = mult
        self.act = action
        self.bg_col = bg_col

        self.last_size = size
        """
        The last size of the button

        Used to get an accurate centre pos
        Horizontal length, vertical length

        :type: list[int, int]
        """
        self.image = self.get_image()
        """
        The pygame.Surface image of the button

        :type: object
        """

    def get_image(self):
        surf = pygame.Surface(self.size)
        cube = self.image_function()
        cube = pygame.transform.smoothscale(cube, self.size)
        cube.set_colorkey(self.bg_col)
        surf.blit(cube, (0, 0))
        return surf

    def update(self, mouse_pos, offset, mouse_up):
        """Offset is a list, width and height"""
        pos = [0, 0]
        pos[0] = self.pos[0] + offset[0]
        pos[1] = self.pos[1] + offset[1]
        width = self.last_size[0]
        height = self.last_size[1]
        centre = width // 2 + pos[0], height // 2 + pos[1]
        if self.image.get_rect(center=centre).collidepoint(mouse_pos):
            if mouse_up:
                self.act()
            temp = self.size.copy()
            self.size[0], self.size[1] = self.size[0] * self.mult, self.size[1] * self.mult
            self.last_size = self.size
            self.image = self.get_image()
            self.size = temp
            self.display_surf.blit(self.image, pos)
            return True
        else:
            self.image = self.get_image()
            self.last_size = self.size
            self.display_surf.blit(self.image, pos)
            return False
        
            
class DisplayBar():
    """For createing a bar of display_objects with set/standard mult"""
    def __init__(self, object_list, offset):
        """
        :type object_list: object
        :param object_list: Should be DisplayOption
        :type offset: list
        :param offset: the mult
        """
        self.object_list = object_list
        self.offset = offset
        self.last = False

    def update(self, mouse_pos, mouse_up):
        for i in range(len(self.object_list)): 
            if i == 0:
                self.last = False
            if self.last:
                self.object_list[i].update(mouse_pos, self.offset, mouse_up)
            else:
                self.last = self.object_list[i].update(mouse_pos, [0, 0], mouse_up)




def text(text, font, foreground_colour, background_colour):
    """
    Returns an image of the text
    :type foreground_colour: tuple
    :type background_colour: tuple
    """
    surface = self.font.render(text=text, fgcolor=foreground_colour, bgcolor=background_colour)
    image = surface.convert_alpha() # optimisation
    return image
