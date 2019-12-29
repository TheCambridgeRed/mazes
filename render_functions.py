#! /usr/bin/env python3

import pygame
from maze_cell import CellType

def clear_screen(cells_list):
    # turns the map back to how it starts when it's 'blank', with each
    # Cell as a WALL. This allows the user to 'carve out' the map
    for line in cells_list:
        for cell in line:
            if cell.cell_type != CellType.WALL:
                cell.cell_type = CellType.WALL


def draw_all(screen, cells_list):
    # goes through each cell in the map and runs its draw_me() function
    for line in cells_list:
        for cell in line:
            cell.draw_me(screen)

            
def x_centered_blit(screen, font, text, colour, y_pos):
    # calculates x_position to blit text so it is centered on a screen.
    # Returns x_pos for later use if necessary
    text_size = font.size(text)
    text_width, text_height = text_size
    x_pos = screen.get_width() / 2 - text_width / 2
    text_surface = font.render(text, True, colour)
    screen.blit(text_surface, (x_pos, y_pos))
    return x_pos
