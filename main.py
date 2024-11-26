# black, isort and flake8 used for formatting

import pygame
import time

import interface 
import cube


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
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)


class RenderButtons:
    cube_option = interface.DisplayOption(lambda: cube.cube_3d(default_colour), screen, [10, 0], [100, 100], 1.5, lambda: RenderButtons.display_swap("3d"), default_colour)
    net_option = interface.DisplayOption(lambda: cube.cube_net(default_colour), screen, [10, 100], [100, 100], 1.5, lambda: RenderButtons.display_swap("net"), default_colour)
    guide_option = interface.DisplayOption(lambda: cube.cube_guide(default_colour), screen, [10, 200], [100, 100], 1.5, lambda: RenderButtons.display_swap("guide"), default_colour)
    cube_option_bar = interface.DisplayBar([cube_option, net_option, guide_option], [0, 50]) # update with any new options
    display_option = "3d"
 # TODO: cube_guide doesnt move when cube is hovered
    def display_swap(option):
        RenderButtons.display_option = option


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
        if event.type == pygame.KEYDOWN and RenderButtons.display_option != "guide":
            if event.key == pygame.K_t:
                cube.turn(True, 0)
            elif event.key == pygame.K_g:
                cube.turn(True, 1)
            elif event.key == pygame.K_b:
                cube.turn(True, 2)
            elif event.key == pygame.K_r:
                cube.turn(True, 0, True)
            elif event.key == pygame.K_f:
                cube.turn(True, 1, True)
            elif event.key == pygame.K_v:
                cube.turn(True, 2, True)

            elif event.key == pygame.K_q:
                cube.turn(False, 0)
            elif event.key == pygame.K_w:
                cube.turn(False, 1)
            elif event.key == pygame.K_e:
                cube.turn(False, 2)
            elif event.key == pygame.K_a:
                cube.turn(False, 0, True)
            elif event.key == pygame.K_s:
                cube.turn(False, 1, True)
            elif event.key == pygame.K_d:
                cube.turn(False, 2, True)

            elif event.key == pygame.K_x:
                cube.rotate("x")
            elif event.key == pygame.K_y:
                cube.rotate("y")
            elif event.key == pygame.K_z:
                cube.rotate("z")

            elif event.key == pygame.K_k:
                solve_cube = True
            elif event.key == pygame.K_m:
                cube.scramble()

    screen.fill(default_colour)

    if solve_cube:
        time.sleep(solver.sleep_time)
        solve_cube = solver.solve()
    else:
        solver.first = True

    if RenderButtons.display_option == "3d":
        surf = cube.cube_3d(default_colour)
    elif RenderButtons.display_option == "net":
        surf = cube.cube_net(default_colour)
    elif RenderButtons.display_option == "guide":
        # also prevents cube interact as uses default
        surf = cube.cube_guide(default_colour)
    rect = surf.get_rect(center=(width//2, height//2))
    screen.blit(surf, rect)
    
    RenderButtons.cube_option_bar.update(mouse_pos, mouse_up)

    pygame.display.flip()
