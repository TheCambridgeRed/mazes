#! /usr/bin/env python3

import pygame, sys, os, re
from entity import Entity, Player
from maze_cell import CellType
from render_functions import clear_screen, draw_cells, draw_all
from level_loader import load_level, level_params

class Menu:
    def __init__(self):
        self.level_rect_list = []
        self.levels_list = []
        self.new_level = None
        self.arrow_position = 0
        
    def handle_all(self, clock):
        next_scene = self.handle_input()

        if next_scene == scenes['menu']:
            self.render(clock)

        return next_scene
        
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.arrow_position < len(self.levels_list) - 1: 
                        self.arrow_position += 1
                elif event.key == pygame.K_UP:
                    if self.arrow_position > 0:
                        self.arrow_position -= 1
                elif event.key == pygame.K_RETURN:
                    self.new_level = load_level(self.levels_list[self.arrow_position] + '.lvl')
                    return scenes['game']

        return scenes['menu']
                        
        

    def render(self, clock):
        screen = pygame.display.set_mode((500, 500))
        
        # fill screen with black
        screen.fill((0, 0, 0))

        # title text
        title_font = pygame.font.SysFont('liberationsans', 72)
        title_string = 'MAZES'
        title_size = title_font.size(title_string)
        title_width = title_size[0]
        title_height = title_size[1]
        title_y_padding = 50
        centered_x_pos = screen.get_width() / 2 - title_width / 2
        title = title_font.render(title_string, True, (255, 255, 255))
        screen.blit(title, (centered_x_pos, title_y_padding))

        # list of levels text
        self.levels_list = []
        self.level_rect_list = []
        
        list_font = pygame.font.SysFont('liberationsans', 36)
        
        if os.path.basename(os.getcwd()) != 'levels':
            os.chdir('levels')
           
        files_list = os.listdir()
        level_regexp = re.compile('(\d-\d{2})(\.lvl)')
        
        for filename in files_list:
            match = level_regexp.findall(filename)
            if match:
                self.levels_list.append(match[0][0])
        
        for i, level_name in enumerate(self.levels_list):
            level_name_size = list_font.size(level_name)
            level_name_width = level_name_size[0]
            level_name_height = level_name_size[1]
            level_name_x_pos = screen.get_width() / 2 - level_name_width / 2
            level_name_text = list_font.render(level_name, True, (255,255,255))
            self.level_rect_list.append(screen.blit(level_name_text, (level_name_x_pos,
                                                                      title_y_padding * 2 + title_height +
                                                                      level_name_height * i)))

        # selection arrow
        arrow_surface = pygame.Surface((level_name_height, level_name_height))
        arrow = pygame.draw.polygon(arrow_surface, (255, 255, 255), [(10, 10), (10, 31), (31, 21)])

        screen.blit(arrow_surface, (level_name_x_pos - level_name_height, title_y_padding * 2 +
                                    title_height + level_name_height * self.arrow_position))
        
        clock.tick(60)
        pygame.display.update()

        
class Game:
    def __init__(self):
        self.size = (0, 0)
        self.maze = []
        self.player = Player()
    
    def handle_all(self, clock):
        next_scene = self.handle_input()
        if next_scene == scenes['game']:
            self.render(clock)
            return scenes['game']
        else:
            return scenes['menu']

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return scenes['menu']
                
        return scenes['game']
        
    def render(self, clock):
        screen = pygame.display.set_mode(self.size)

        for cell in self.maze:
            if cell.cell_type == CellType.START:
                self.player.x = cell.x
                self.player.y = cell.y

        self.player.size = self.player.width, self.player.height = self.size
        screen.blit(self.player.sprite, (self.player.x, self.player.y))
        
        clock.tick(60)
        draw_all(screen, self.maze)

    
scenes = {'menu': Menu(),
          'game': Game()}


if __name__ == '__main__':
    pygame.init()
    
    clock = pygame.time.Clock()

    scene = scenes['menu']
    
    while True:
        next_scene = scene.handle_all(clock)
        if scene == scenes['menu'] and next_scene == scenes['game']:
            next_scene.size, next_scene.maze = level_params(scene.new_level)
        scene = next_scene
        
