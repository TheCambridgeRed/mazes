#! /usr/bin/env python3

import pygame

def clear_screen(cells_list):
    for line in cells_list:
        for cell in line:
            if cell.cell_type != CellType.FLOOR:
                cell.cell_type = CellType.FLOOR


def draw_cells(screen, cells_list):
    for line in cells_list:
        for cell in line:
            cell.draw_me(screen)


def draw_all(screen, cells_list):
    draw_cells(screen, cells_list)
    
