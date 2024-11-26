# black, isort and flake8 used for formatting

import pygame
import time

import interface 
import cube
from data import *


# window
pygame.init()
width = 1600
height = 900
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

# cubes
cube_net = cube.CubeNet(screen, (width//2, height//2))
cube_3d = cube.Cube3D(screen, (width//2, height//2))
cube_guide = cube.CubeGuide(screen, (width//2, height//2))

class RenderButtons:
    cube_option = interface.DisplayOption(lambda: cube_3d.get_image(), screen, [10, 0], [100, 100], 1.5, lambda: RenderButtons.display_swap("3d"), default_colour)
    net_option = interface.DisplayOption(lambda: cube_net.get_image(), screen, [10, 100], [100, 100], 1.5, lambda: RenderButtons.display_swap("net"), default_colour)
    guide_option = interface.DisplayOption(lambda: cube_guide.get_image(), screen, [10, 200], [100, 100], 1.5, lambda: RenderButtons.display_swap("guide"), BLACK) # should be default colour, but bg gets changed to bacl somewhere. MAy be an error with pygame.smoothscale in interface file
    cube_option_bar = interface.DisplayBar([cube_option, net_option, guide_option], [0, 50]) # update with any new options
    display_option = "3d"
 # TODO: cube_guide doesnt move when cube is hovered
    def display_swap(option):
        RenderButtons.display_option = option



solve_cube = False
solver = cube.Solver()
timer = cube.Timer()

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
                if timer.running: # decreased perfromance signoificantly TODO: fix?
                    timer.delete()
            elif event.key == pygame.K_m:
                cube.scramble()
                timer.start()# start timer
            elif event.key == pygame.K_h:
                solver.pop_move()

    screen.fill(default_colour)

    if solve_cube:
        time.sleep(solver.sleep_time)
        solve_cube = solver.solve()
    else:
        solver.first = True

    if timer.running and solver.check_solved():
        timer.stop()

    if RenderButtons.display_option == "3d":
        display_cube = cube_3d
    elif RenderButtons.display_option == "net":
        display_cube = cube_net
    elif RenderButtons.display_option == "guide":
        # also prevents cube interact as uses default
        display_cube = cube_guide
        # actions text
        screen.blit(interface.text("Scramble: M", guide_font, BLACK, default_colour), (1100, 300))
        screen.blit(interface.text("Solve: K", guide_font, BLACK, default_colour), (1100, 350))
        screen.blit(interface.text("Hint: H", guide_font, BLACK, default_colour), (1100, 400))
    display_cube.update()

    if timer.exists:
        screen.blit(timer.display_elapsed(), (1400, 200))
        timer.update()
    
    RenderButtons.cube_option_bar.update(mouse_pos, mouse_up)

    pygame.display.flip()
pygame.quit()
