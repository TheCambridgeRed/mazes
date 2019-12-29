#! /usr/bin/env python3

from render_functions import draw_all
from level import Level
import pygame, sys, pickle, os

def load_level(level_string):
    # masks pickling
    with open (level_string, 'rb') as f:
        active_level = pickle.load(f)
        
    return active_level


def level_params(level):
    # extracts some parameters from the level and returns them for use
    # in rendering
    x = level.x
    y = level.y
    scale = level.scale
    cells_list = level.cells_list

    size = width, height = x * scale, y * scale

    return size, cells_list


def view_loop(screen, cells_list, clock):
    # simple render loop to show the loaded level
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    sys.exit()

                
        clock.tick(60)
        draw_all(screen, cells_list)
        pygame.display.update()


if __name__ == "__main__":
    try:
        # ensure we're in the right directory to load a level. The Exception
        # should never be raised
        if os.path.basename(os.getcwd()) != 'levels':
            if os.path.basename(os.getcwd()) == 'maze_game':
                os.chdir('levels')
            elif os.path.basename(os.getcwd()) == 'images':
                os.chdir('../levels')
            else:
                raise Exception('where are you??')

        # the level to load should be entered on the command line
        level = load_level(sys.argv[1])

        size, cells_list = level_params(level)
        
        pygame.init()

        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Mazes')
        clock = pygame.time.Clock()

        view_loop(screen, cells_list, clock)

    except IndexError:
        # raised if there are no command line arguments
        print('Please enter a level file to load')

    except FileNotFoundError as e:
        # raised if the filename given is invalid
        print(f'{e.filename} does not exist or is an invalid filename')
