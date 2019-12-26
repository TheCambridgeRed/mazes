#! /usr/bin/env python3

from maze_cell import CellType, MazeCell
from level import Level
import pygame, sys, pickle, os


def clear_screen(cells_list):
    for cell in cells_list:
        if cell.cell_type != CellType.FLOOR:
            cell.cell_type = CellType.FLOOR


def draw_cells(screen, cells_list):
    for cell in cells_list:
        cell.draw_me(screen)


def draw_all(screen, cells_list):
    draw_cells(screen, cells_list)
    pygame.display.update()


def save_level(x, y, scale, cells_list):
    name = input("Enter name for level: ")
    level_to_save = Level(x, y, scale, cells_list)
    while True:
        try:
            with open(f"levels/{name}", 'wb') as f:
                pickle.dump(level_to_save, f, pickle.HIGHEST_PROTOCOL)
                print(f'Level saved as {name}')
                break
        except FileNotFoundError:
            print('Levels folder not found. Creating...')
            os.mkdir('levels')
            


def render_loop(screen, x, y, scale, cells_list):
    draw_all(screen, cells_list)
    
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

                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    sys.exit()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for cell in cells_list:
                    if cell.rect.collidepoint(pygame.mouse.get_pos()):
                        cell.toggle()
                draw_all(screen, cells_list)


def generate_blank_map(x, y, scale):
    cells_list = []
    for i in range(0, x):
        for j in range(0, y):
            cells_list.append(MazeCell(i, j, scale))

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
        

    
