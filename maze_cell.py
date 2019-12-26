from cell import Cell
from enum import Enum, auto
import pygame


class CellType(Enum):
    FLOOR = auto()
    WALL = auto()
    START = auto()
    END = auto()


class MazeCell(Cell):
    def __init__(self, x, y, scale, cell_type=CellType.FLOOR):
        super().__init__(x, y)
        self.scale = scale
        self.rect = pygame.Rect(self.x * self.scale, self.y * self.scale, self.scale, self.scale)
        self.cell_type = cell_type


    def draw_me(self, screen):
        if self.cell_type == CellType.FLOOR:
            colour = (179, 89, 0)
        elif self.cell_type == CellType.WALL:
            colour = (92, 92, 92)
        elif self.cell_type == CellType.START:
            colour = (255, 213, 0)
        elif self.cell_type == CellType.END:
            colour = (255, 64, 25)
        pygame.draw.rect(screen, colour, self.rect)

        
    def toggle(self):
        try:
            self.cell_type = CellType(self.cell_type.value + 1)
        except ValueError:
            self.cell_type = CellType(1)
