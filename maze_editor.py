#! /usr/bin/env python3

# Use this to create maps for the maze game. C clears the screen, S saves
# the map in a form that can be used by the level_loader and the game. Either
# provide an int x, int y and int scale as a command line argument or provide
# the name of a level to load and edit

from maze_cell import CellType, MazeCell
from level import Level
from level_loader import load_level, level_params
from render_functions import clear_screen, draw_all
import pygame, sys, pickle, os


def validated(cells_list):
    # checks that the level you are about to save has exactly one START
    # cell and exactly one END cell.
    # TODO: make this function check whether the maze can be solved
    
    # find START cell first
    start_cells = 0
    for line in cells_list:
        for cell in line:
            if cell.cell_type == CellType.START:
                start_cells += 1

    # then find END cell
    end_cells = 0
    for line in cells_list:
        for cell in line:
            if cell.cell_type == CellType.END:
                end_cells +=1
        
    if start_cells != 1 or end_cells != 1:
        return False

    return True
    

def save_level(x, y, scale, cells_list, new_map):
    # If the level is valid, creates the ./levels subdirectory if it doesn't
    # exist, takes user input for file name if one wasn't provided on the
    # command line, then instances a Level using the parameters passed to
    # the function.
    if validated(cells_list):
        if new_map:
            name = input("Enter name for level: ")
        else:
            print(f'Overwriting {sys.argv[1]}')
            name = sys.argv[1]
    
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
    else:
        print('Invalid level. Provide exactly one START cell and exactly ' +
              'one END cell.\nLevel not saved.') 
        


def render_loop(screen, x, y, scale, cells_list, new_map=True):
    # handles rendering and input. Only updates the level when something
    # changes: when a cell is clicked (changing its state) or when the
    # map is cleared.
    draw_all(screen, cells_list)
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # is S is pressed, save the level
                if event.key == pygame.K_s:
                    save_level(x, y, scale, cells_list, new_map)

                # if C is pressed, clear the screen and redraw it
                elif event.key == pygame.K_c:
                    clear_screen(cells_list)
                    draw_all(screen, cells_list)
                    pygame.display.update()

                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    sys.exit()

            # if the user clicks on a cell, change its state to the
            # next CellState, then redraw the screen
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for line in cells_list:
                    for cell in line:
                        if cell.rect.collidepoint(pygame.mouse.get_pos()):
                            cell.toggle()
                draw_all(screen, cells_list)
                pygame.display.update()


def generate_blank_map(x, y, scale):
    # populates and returns the cells_list with a 2-dimensional array of
    # MazeCells organised into lines. 
    cells_list = []

    i = 0

    while i < x:
        j = 0
        inner_list = []
        while j < y:
            inner_list.append(MazeCell(i, j, scale))
            j += 1
        cells_list.append(inner_list)
        i += 1

    return cells_list


def main():
    pygame.init()

    # if x, y and scale are provided on command line
    if len(sys.argv) == 4:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        scale = int(sys.argv[3])

        size = width, height = x * scale, y * scale
        
        cells_list = generate_blank_map(x, y, scale)

        new_map = True

    # if the filename of a level is provided (with the extension) 
    elif len(sys.argv) == 2:
        os.chdir('levels')
        
        level = load_level(sys.argv[1])
        os.chdir('..')
        
        x = level.x
        y = level.y
        scale = level.scale
        
        size, cells_list = level_params(level)

        new_map = False
    
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Level Editor')

    render_loop(screen, x, y, scale, cells_list, new_map)
        
    
if __name__ == "__main__":
    main()
