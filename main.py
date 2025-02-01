"""
This is the file to run to execute the program

This file handles the main loop of the program, it gets images and data from the other
files and displays them. It also handles user input within the game loop.

black, isort and flake8 used for formatting
"""

import sys
import time

import cube
import features
import game_data  # for changing variables in data file
import interface
import pygame
import user_data
from game_data import *
from Login import login_window
from validation import ValidateScreenPositions

# window
pygame.init()
width = 1600
height = 900
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Rubik's Cube")

# validation
val = ValidateScreenPositions(width, height)

# cubes and visuals
cube_net = cube.CubeNet(screen, val.run((width // 2, height // 2)))
cube_3d = cube.Cube3D(screen, val.run((width // 2, height // 2)))
cube_guide = cube.CubeGuide(screen, val.run((width // 2, height // 2)))
display_history = features.DisplayHistory(screen, val.run((width // 2, height // 2)))
display_leaderboard = features.Leaderboard(screen, val.run((width // 2, height // 2)))


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

    history_option = interface.DisplayOption(
        lambda: interface.text(
            "HISTORY",
            default_font,
            BLACK,
            default_colour
        ),
        screen,
        val.run([10, 300]),
        [100, 25],
        1.5,
        lambda: Buttons.display_swap("history"),
        BLACK,  # same problem as guide
    )

    leaderboard_option = interface.DisplayOption(
        lambda: interface.text(
            "LEADERBOARD",
            default_font,
            BLACK,
            default_colour
        ),
        screen,
        val.run([10, 325]),
        [100, 25],
        1.5,
        lambda: Buttons.display_swap("leaderboard"),
        BLACK,  # same problem as guide
    )

    cube_option_bar = interface.DisplayBar(  # update with any new options
        [cube_option, net_option, guide_option, history_option, leaderboard_option],
        False,
    )
    display_option = "3d"

    @staticmethod
    def display_swap(option):
        """
        Updates display_option variable within the class

        This provides a function for interface.DisplayOption objects
        to update the display_option variable which is saved with this class

        :param option: the new display_option: 3d, net, guide, history or leaderboard
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
"""If the cube is being solved
:type solve_cube: bool"""
solver = features.Solver()

timer = features.Timer()
last_save = time.time()
"""The timestamp of the last save, used for calculating time since last save
:type last_save: float"""


# login
def load(username):
    """Desgined to be called by the login window, this function will load the users data

    Uses Manager.load to load the users data and then checks the game state, updating
    details about the timer and solver is nessesary

    :param username: the unique username of the user
    :type username: str
    """
    user_data.Manager.load(username)

    if game_data.time_taken > 0:  # timer is running
        # manually start timer to avoid changing start time
        timer.exists = True
        timer.running = True
        timer.start_time = (
            time.time() - game_data.time_taken
        )  # act as if timer has just started
    if game_data.solver_used: # solver is runnning
        # finish solving cube
        solver.first = False
        solve_cube = True


login_window.Window(lambda u: load(u))


# game loop
while True:
    mouse_pos = pygame.mouse.get_pos()
    mouse_up = False
    val.update_size(pygame.display.get_surface().get_size())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_up = True
        elif event.type == pygame.MOUSEWHEEL and Buttons.display_option == "history":
            display_history.scroll(event.y * 25)
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
                game_data.solver_used = True
                if timer.running:  # ensures the attempt was started
                    # failed attempts should be recorded
                    game_data.solved = False
                    user_data.game_history.add_game()
                    timer.delete()

                solve_cube = True
            elif event.key == pygame.K_m:  # scramble
                if timer.running:  # ensures the attempt was started
                    # failed attempts should be recorded
                    user_data.game_history.add_game()

                # reset key data
                game_data.moves.clear()
                game_data.move_count = 0
                game_data.scrambler_count = 0
                game_data.hints_used = False
                game_data.solver_used = False
                game_data.solved = False
                game_data.time_taken = 0
                game_data.start_time = time.time()

                features.scramble()
                # prevent the timer from being started whilst the solver runs
                # was achieved by scrambling whilst the timer ran
                solve_cube = False
                timer.start()  # start timer
            elif event.key == pygame.K_h:  # hint
                game_data.hints_used = True
                solver.pop_move()

    screen.fill(default_colour)  # background colour

    if solve_cube:
        # ensures each solve take 5 sections, assuming no hardware limitations
        time.sleep(solver.sleep_time)
        solve_cube = solver.solve()  # solves one move
    else:
        solver.first = True  # so next solve it is set to true

    if timer.running and solver.check_solved():  # on a solve
        timer.stop()
        game_data.solved = True
        user_data.game_history.add_game()
        display_leaderboard.update_list(
            game_data.time_taken,
            game_data.move_count
        )

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
    elif Buttons.display_option == "history":
        display_cube = display_history
    elif Buttons.display_option == "leaderboard":
        display_cube = display_leaderboard
    display_cube.update()  # actually update cube

    if timer.exists:  # display timer
        screen.blit(timer.display_elapsed(), val.run((1400, 200)))
        timer.update()

    # update buttons
    Buttons.update(mouse_pos, mouse_up)

    # save every 5 seconds
    if time.time() - last_save > 5:
        time_since_save = time.time()
        user_data.Manager.save()

    pygame.display.flip()
