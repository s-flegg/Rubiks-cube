"""
This is the file to run to execute the program

This file handles the main loop of the program, it gets images and data from the other
files and displays them. It also handles user input within the game loop.

black, isort and flake8 used for formatting
"""

import time

import cube
import interface
import pygame
from data import *
from validation import ValidateScreenPositions

# window
pygame.init()
width = 1600
height = 900
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

# validation
val = ValidateScreenPositions(width, height)

# cubes
cube_net = cube.CubeNet(screen, val.run((width // 2, height // 2)))
cube_3d = cube.Cube3D(screen, val.run((width // 2, height // 2)))
cube_guide = cube.CubeGuide(screen, val.run((width // 2, height // 2)))


class Buttons:
    """
    This class handles the rendering of the buttons

    This class is largely self-contained, the only usage should be to run
    .update as this automatically updates the buttons
    """

    cube_option = interface.DisplayOption(
        lambda: cube_3d.get_image(),
        screen,
        val.run([10, 0]),
        [100, 100],
        1.5,
        lambda: Buttons.display_swap("3d"),
        default_colour,
    )
    net_option = interface.DisplayOption(
        lambda: cube_net.get_image(),
        screen,
        val.run([10, 100]),
        [100, 100],
        1.5,
        lambda: Buttons.display_swap("net"),
        default_colour,
    )
    guide_option = interface.DisplayOption(
        lambda: cube_guide.get_image(),
        screen,
        val.run([10, 200]),
        [100, 100],
        1.5,
        lambda: Buttons.display_swap("guide"),
        BLACK,
    )  # should be default colour,
    # but this causes the background of the hovered button to be black.
    # May be an error with pygame.smoothscale in interface file
    # this works as a solution
    cube_option_bar = interface.DisplayBar(  # update with any new options
        [cube_option, net_option, guide_option], False
    )
    display_option = "3d"

    @staticmethod
    def display_swap(option):
        """
        Updates display_option variable within the class

        This provides a function for interface.DisplayOption objects
        to update the display_option variable which is saved with this class

        :param option: the new display_option: 3d, net or guide
        :type option: str
        """
        Buttons.display_option = option

    @staticmethod
    def update(mouse_pos, mouse_up):
        """
        Updates each button in the class

        :param mouse_pos: the x,y position of the mouse
        :param mouse_up: whether the mouse button has been clicked
        :type mouse_pos: tuple[int, int] or list[int, int]
        :type mouse_up: bool
        :rtype: None
        """
        Buttons.cube_option_bar.update(mouse_pos, mouse_up)


# used for solving the cube
solve_cube = False
solver = cube.Solver()

timer = cube.Timer()

# game loop
while True:
    mouse_pos = pygame.mouse.get_pos()
    mouse_up = False
    val.update_size(pygame.display.get_surface().get_size())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_up = True
        # prevent any moves made whilst on guide cube
        elif event.type == pygame.KEYDOWN and Buttons.display_option != "guide":
            # row right
            if event.key == pygame.K_t:
                cube.turn(True, 0)
            elif event.key == pygame.K_g:
                cube.turn(True, 1)
            elif event.key == pygame.K_b:
                cube.turn(True, 2)
            # row left
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

            elif event.key == pygame.K_k:  # solve
                solve_cube = True
                if timer.running:
                    timer.delete()
            elif event.key == pygame.K_m:  # scramble
                cube.scramble()
                # prevent the timer from being started whilst the solver runs
                # was achieved by scrambling whilst the timer ran
                solve_cube = False
                timer.start()  # start timer
            elif event.key == pygame.K_h:  # hint
                solver.pop_move()

    screen.fill(default_colour)  # background colour

    if solve_cube:
        # ensures each solve take 5 sections, assuming no hardware limitations
        time.sleep(solver.sleep_time)
        solve_cube = solver.solve()  # solves one move
    else:
        solver.first = True  # so next solve it is set to true

    if timer.running and solver.check_solved():  # ends timer on solve
        timer.stop()

    if Buttons.display_option == "3d":
        display_cube = cube_3d
    elif Buttons.display_option == "net":
        display_cube = cube_net
    elif Buttons.display_option == "guide":
        # also prevents cube interact as uses default
        display_cube = cube_guide
        # actions text
        screen.blit(
            interface.text(
                text="Scramble: M",
                font=guide_font,
                foreground_colour=BLACK,
                background_colour=default_colour,
            ),
            val.run((1100, 300)),
        )
        screen.blit(
            interface.text(
                text="Solve: K",
                font=guide_font,
                foreground_colour=BLACK,
                background_colour=default_colour,
            ),
            val.run((1100, 350)),
        )
        screen.blit(
            interface.text(
                text="Hint: H",
                font=guide_font,
                foreground_colour=BLACK,
                background_colour=default_colour,
            ),
            val.run((1100, 400)),
        )
    display_cube.update()  # actually update cube

    if timer.exists:  # display timer
        screen.blit(timer.display_elapsed(), val.run((1400, 200)))
        timer.update()

    # update buttons
    Buttons.update(mouse_pos, mouse_up)

    pygame.display.flip()
pygame.quit()
