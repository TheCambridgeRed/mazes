import pygame, sys, os
from render_functions import draw_all, x_centered_blit
from maze_cell import CellType
from entity import Player
from level_loader import load_level

class BadLevelException(Exception):
    # for validating levels
    def __init__(self, text):
        self.what = text

        
class Menu:
    # this class handles input and rendering for the menu screen
    
    def __init__(self, levels_list):
        # variables for title
        self.title_font = pygame.font.SysFont('liberationsans', 72)
        self.title_string = 'MAZES'
        self.title_size = self.title_font.size(self.title_string)
        self.title_y_padding = 50
        self.title_colour = (0, 0, 0)

        # variables for levels list
        self.levels_list = levels_list
        self.list_font = pygame.font.SysFont('liberationsans', 36)
        level_string_example = '0-00'
        self.list_size = self.list_font.size(level_string_example)
        self.list_colour = (0, 0, 0)

        # variables for selection arrow
        self.arrow_surface = pygame.Surface((self.list_size[1],
                                            self.list_size[1]))
        self.arrow_surface.fill((255, 255, 255))
        self.arrow_points = [(10, 10), (10, 31), (31, 21)]
        self.arrow_colour = (0, 0, 0)
        self.arrow_position = 0

        
    def handle_all(self, clock, scenes):
        next_scene = self.handle_input(scenes)

        # if the next scene isn't 'menu', then we don't know what we
        # want to render, so only render when we're seeing the menu again
        if next_scene == scenes['menu']:
            self.render(clock)

        return next_scene
        
    def handle_input(self, scenes):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

                # if the down key is pressed, move the arrow down the
                # list, unless it's at the bottom of the list, in which
                # case wrap around to the top
                elif event.key == pygame.K_DOWN:
                    if self.arrow_position < len(self.levels_list) - 1: 
                        self.arrow_position += 1
                    else:
                        self.arrow_position = 0

                # if the up key is pressed, move the arrow up the
                # list, unless it's at the top of the list, in which
                # case wrap around to the bottom
                elif event.key == pygame.K_UP:
                    if self.arrow_position > 0:
                        self.arrow_position -= 1
                    else:
                        self.arrow_position = len(self.levels_list) - 1

                # if Enter is pressed, load the level which the arrow was
                # pointing at
                elif event.key == pygame.K_RETURN:
                    return scenes[self.levels_list[self.arrow_position]]

        # if we didn't load a level, we want to stay on the menu
        return self
                        
    def render(self, clock):
        screen = pygame.display.set_mode((500, 500))
        
        # fill screen with white
        screen.fill((255, 255, 255))

        # render title in center of screen
        x_centered_blit(screen, self.title_font, self.title_string,
                        self.title_colour, self.title_y_padding)

        # render list of levels in center of screen
        for i, level_name in enumerate(self.levels_list):
            list_x_pos = x_centered_blit(screen, self.list_font, level_name,
                            self.list_colour, (self.title_y_padding * 2 +
                                               self.title_size[1] +
                                               self.list_size[1] * i))
            

        # selection arrow - drawn to the left of the levels list on par with levels
        arrow = pygame.draw.polygon(self.arrow_surface, self.arrow_colour,
                                    self.arrow_points)

        screen.blit(self.arrow_surface, (list_x_pos - self.list_size[1],
                                    self.title_y_padding * 2 +
                                    self.title_size[1] +
                                    self.list_size[1] * self.arrow_position))

        # render everything
        clock.tick(60)
        pygame.display.update()

        
class Game:
    # this class handles input and rendering during gameplay. It loads the
    # level from file and handles a Player, placing the Player on the start
    # square on the map during initialisation.
    
    def __init__(self, level):
        # make sure we're in the levels directory to load a level. The
        # Exception should never be raised.
        if os.path.basename(os.getcwd()) != 'levels':
            if os.path.basename(os.getcwd()) == 'maze_game':
                os.chdir('levels')
            elif os.path.basename(os.getcwd()) == 'images':
                os.chdir('../levels')
            else:
                raise Exception('where are you??')

        self.level_name = level
        self.level = load_level(self.level_name)
        
        # x and y are for the logic of the cells, independent of
        # the size the cells are drawn
        self.x = self.level.x
        self.y = self.level.y
        
        # need this scale factor and derived variables for drawing
        self.scale = self.level.scale
        self.width = self.x * self.scale
        self.height = self.y * self.scale
        self.size = (self.width, self.height)

        # establish where the player should start in the level
        self.maze = self.level.cells_list
        for line in self.maze:
            for cell in line:
                if cell.cell_type == CellType.START:
                    self.player_x = cell.x
                    self.player_y = cell.y
                    break
            else:
                continue
            break
        else:
            raise BadLevelException(f'{self.level_name} does not have a start square!')

        # load a Player at the right position and scaled to the size of the map
        self.player = Player(self.player_x, self.player_y,
                             self.scale, 'player.png')
    
    def handle_all(self, clock, scenes):
        next_scene = self.handle_input(clock, scenes)

        # we only want to render using Game.render() if we are staying
        # on this level
        if next_scene == self:
            self.render(clock)
            
        return next_scene

    def handle_input(self, clock, scenes):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                # if Esc is pressed, we want to return to the menu but also
                # to forget where the player got to on the current level.
                # So we reinitialise the level before returning to the menu.
                if event.key == pygame.K_ESCAPE:
                    self.__init__(self.level_name)
                    return scenes['menu']

                # for all arrow key presses, check whether the player is about 
                # to walk intoa wall. only if they aren't can we let them move.
                
                # if down is pressed, only check for walls if the Player isn't
                # at the lower edge of the screen
                elif event.key == pygame.K_DOWN and self.player.y < self.y - 1:
                    if (self.maze[self.player.x][self.player.y + 1].cell_type
                        != CellType.WALL):
                        self.player.y += 1

                # if up is pressed, only check for walls if the Player isn't
                # at the upper edge of the screen
                elif event.key == pygame.K_UP and self.player.y > 0:
                    if (self.maze[self.player.x][self.player.y - 1].cell_type
                        != CellType.WALL):
                        self.player.y -= 1

                # if left is pressed, only check for walls if the Player isn't
                # at the left edge of the screen
                elif event.key == pygame.K_LEFT and self.player.x > 0:
                    if (self.maze[self.player.x - 1][self.player.y].cell_type
                        != CellType.WALL):
                        self.player.x -= 1

                # if right is pressed, only check for walls if the Player isn't
                # at the right edge of the screen
                elif event.key == pygame.K_RIGHT and self.player.x < self.x - 1:
                    if (self.maze[self.player.x + 1][self.player.y].cell_type
                        != CellType.WALL):
                        self.player.x += 1

        # if, after moves are made, the Player is on an end tile, then
        # the player wins. We render once so that the WinScreen shows the
        # Player on the end tile, because we will need to initialise before
        # we change scene; without the extra call to render() here the Player
        # ends up on the start tile during the WinScreen. the print() statement
        # will be replaced by whatever will happen when the player wins.
        if self.maze[self.player.x][self.player.y].cell_type == CellType.END:
            self.render(clock)
            print('Winner!')
            self.__init__(self.level_name)
            return scenes['win_screen']

        # if the player neither won nor exited, we assume that we are staying
        # on this level
        return self
            
    def render(self, clock):
        screen = pygame.display.set_mode(self.size)

        # all we have to do here is draw the map and draw the Player
        # in the right position each cycle
        clock.tick(60)
        draw_all(screen, self.maze)
        screen.blit(self.player.sprite,
                    (self.player.x * self.scale, self.player.y * self.scale))
        pygame.display.update()


class WinScreen:
    # handles input and rendering after the player has won. Currently just
    # takes away player control.
    
    def handle_all(self, clock, scenes):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return scenes['menu']
        return self
