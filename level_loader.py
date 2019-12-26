#! /usr/bin/env python3

from maze_editor import draw_cells, draw_all
from level import Level
import pygame, sys, pickle

def load_level(level_string):
    with open (level_string, 'rb') as f:
        active_level = pickle.load(f)

    x = active_level.x
    y = active_level.y
    scale = active_level.scale
    cells_list = active_level.cells_list

    size = width, height = x * scale, y * scale

    return size, cells_list


def game_loop(screen, cells_list, clock):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    sys.exit()

                
        clock.tick(60)
        draw_all(screen, cells_list)


if __name__ == "__main__":
    try:
        size, cells_list = load_level(sys.argv[1])

        pygame.init()

        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Mazes')
        clock = pygame.time.Clock()

        game_loop(screen, cells_list, clock)

    except IndexError:
        print('Please enter a level file to load')
        
    except FileNotFoundError:
        print('Invalid filename for level')
