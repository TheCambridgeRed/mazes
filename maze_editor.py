#! /usr/bin/env python3

from maze_cell import CellType, MazeCell
from level import Level
from render_functions import clear_screen, draw_cells, draw_all
import pygame, sys, pickle, os


def save_level(x, y, scale, cells_list):
    name = input("Enter name for level: ")
    level_to_save = Level(x, y, scale, cells_list)
    while True:
        try:
            with open(os.path.join('levels', name), 'wb') as f:
                pickle.dump(level_to_save, f, pickle.HIGHEST_PROTOCOL)
                print(f'Level saved as {name}')
                break
        except FileNotFoundError:
            print('Levels folder not found. Creating...')
            os.mkdir('levels')
            


def render_loop(screen, x, y, scale, cells_list):
    draw_all(screen, cells_list)
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_level(x, y, scale, cells_list)
                elif event.key == pygame.K_c:
                    clear_screen(cells_list)
                    draw_all(screen, cells_list)
                    pygame.display.update()

                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    sys.exit()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for line in cells_list:
                    for cell in line:
                        if cell.rect.collidepoint(pygame.mouse.get_pos()):
                            cell.toggle()
                draw_all(screen, cells_list)
                pygame.display.update()


def generate_blank_map(x, y, scale):
    cells_list = []

    j = 0

    while j < x:
        i = 0
        inner_list = []
        while i < y:
            inner_list.append(MazeCell(j, i, scale))
            i += 1
        cells_list.append(inner_list)
        j += 1

    return cells_list
            
    
if __name__ == "__main__":
    pygame.init()

    x = int(sys.argv[1])
    y = int(sys.argv[2])
    scale = int(sys.argv[3])
    
    size = width, height = x * scale, y * scale
    
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Level Editor')

    cells_list = generate_blank_map(x, y, scale)

    render_loop(screen, x, y, scale, cells_list)
        

    
