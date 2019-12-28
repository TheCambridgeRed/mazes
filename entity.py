import os, pygame

class Entity:
    def __init__(self, x, y, scale):
         self.x = x
         self.y = y
         self.scale = scale
         self.width = self.x * self.scale
         self.height = self.y * self.scale
         self.size = (self.width, self.height)


class Player(Entity):
    def __init__(self, x=0, y=0, scale=50, sprite='player.png',
                 collides=True, controllable = True):
        # sprite should be the name of an image file in the 'images' directory
        pygame.init()
        super().__init__(x, y, scale)
        if os.path.basename(os.getcwd()) != 'images':
            if os.path.basename(os.getcwd()) == 'levels':
                os.chdir('../images')
            elif os.path.basename(os.getcwd()) == 'maze_game':
                os.chdir('images')
            else:
                raise Exception('where are you??')
        self.sprite = pygame.image.load(sprite)
        self.sprite = pygame.transform.scale(self.sprite, self.size)
        if collides:
            self.collides = True
            self.rect = self.sprite.get_bounding_rect()
        if controllable:
            self.controllable = True
