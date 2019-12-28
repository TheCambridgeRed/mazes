#! /usr/bin/env python3

import pygame

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
