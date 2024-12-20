# black, isort and flake8 used for formatting

import time

import cube
import interface
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

default_colour = GREY


# window
pygame.init()
width = 1600
height = 900
screen = pygame.display.set_mode(
    (width, height), pygame.RESIZABLE
)  # creates screen object, allows the window to be resized


class RenderButtons:
    """
    A self-contained collection of buttons

    cube_option_bar should be .update to display all the buttons
    """
    cube_option = interface.DisplayButton(
        image_function=lambda: cube.cube_3d(default_colour),
        display_surf=screen,
        pos=[10, 0],
        size=[100, 100],
        mult=1.5,
        action=lambda: RenderButtons.display_swap("3d"),
        bg_col=default_colour,
    )
    net_option = interface.DisplayButton(
        image_function=lambda: cube.cube_net(default_colour),
        display_surf=screen,
        pos=[10, 100],
        size=[100, 100],
        mult=1.5,
        action=lambda: RenderButtons.display_swap("net"),
        bg_col=default_colour,
    )
    guide_option = interface.DisplayButton(
        image_function=lambda: cube.cube_guide(default_colour),
        display_surf=screen,
        pos=[10, 200],
        size=[100, 100],
        mult=1.5,
        action=lambda: RenderButtons.display_swap("guide"),
        bg_col=default_colour,
    )
    cube_option_bar = interface.DisplayBar(
        [cube_option, net_option, guide_option], [0, 50]
    )  # update with any new options
    """Manages the cube option buttons, it should be updated every game loop"""
    display_option = "3d"

    def display_swap(option):
        """
        Updates display_option variable within the class

        This provides a function for interface.DisplayOption objects
        to update the display_option variable which is saved with this class

        :param option: the new display_option: 3d, net or guide
        :type option: str
        """
        RenderButtons.display_option = option


# used for solving the cube
solve_cube = False
solver = cube.Solver()

# game loop
while True:
    mouse_pos = pygame.mouse.get_pos()
    mouse_up = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_up = True
        # prevent any moves made whilst on guide cube
        if event.type == pygame.KEYDOWN and RenderButtons.display_option != "guide":
            # row right
            if event.key == pygame.K_t:
                cube.turn(True, 0)
            elif event.key == pygame.K_g:
                cube.turn(True, 1)
            elif event.key == pygame.K_b:
                cube.turn(True, 2)
            #row left
            elif event.key == pygame.K_r:
                cube.turn(True, 0, True)
            elif event.key == pygame.K_f:
                cube.turn(True, 1, True)
            elif event.key == pygame.K_v:
                cube.turn(True, 2, True)
            # column up
            elif event.key == pygame.K_q:
                cube.turn(False, 0)
            elif event.key == pygame.K_w:
                cube.turn(False, 1)
            elif event.key == pygame.K_e:
                cube.turn(False, 2)
            # column down
            elif event.key == pygame.K_a:
                cube.turn(False, 0, True)
            elif event.key == pygame.K_s:
                cube.turn(False, 1, True)
            elif event.key == pygame.K_d:
                cube.turn(False, 2, True)
            # rotations
            elif event.key == pygame.K_x:
                cube.rotate("x")
            elif event.key == pygame.K_y:
                cube.rotate("y")
            elif event.key == pygame.K_z:
                cube.rotate("z")
            # features
            elif event.key == pygame.K_k: #solver
                solve_cube = True
            elif event.key == pygame.K_m: #scrambler
                cube.scramble()

    screen.fill(default_colour) #background colour

    if solve_cube:
        time.sleep(solver.sleep_time) # ensures each solve takes 5 seconds
        solve_cube = solver.solve() # solves one move
    else:
        solver.first = True # so next solve it is set to true

    if RenderButtons.display_option == "3d":
        surf = cube.cube_3d(default_colour)
    elif RenderButtons.display_option == "net":
        surf = cube.cube_net(default_colour)
    elif RenderButtons.display_option == "guide":
        # also prevents cube interact as uses default
        surf = cube.cube_guide(default_colour)
    rect = surf.get_rect(center=(width // 2, height // 2))
    screen.blit(surf, rect)

    RenderButtons.cube_option_bar.update(mouse_pos, mouse_up) #display buttons

    pygame.display.flip()
