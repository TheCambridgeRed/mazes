import os, pygame


class Entity:
    # general Entity class to be inherited by different Entities
    def __init__(self, x, y, scale):
         self.x = x
         self.y = y
         self.scale = scale
         self.width = self.scale
         self.height = self.scale
         self.size = (self.width, self.height)


class Player(Entity):
    # controllable Entity with a sprite to move around the maze. A Player is
    # instanced relative to a particular level so that the Player is the
    # the right size for the level
    def __init__(self, x, y, scale, sprite,
                 collides=True, controllable = True):
        # sprite should be the name of an image file in the 'images' directory
        super().__init__(x, y, scale)

        # ensure we're in the right directory to load the player sprite. The
        # Exception should never be raised
        if os.path.basename(os.getcwd()) != 'images':
            if os.path.basename(os.getcwd()) == 'levels':
                os.chdir('../images')
            elif os.path.basename(os.getcwd()) == 'maze_game':
                os.chdir('images')
            else:
                raise Exception('where are you??')
            
        self.sprite = pygame.image.load(sprite)

        # make sure the player sprite is the right size for the level we're on
        self.sprite = pygame.transform.scale(self.sprite, self.size)

        # none of this is strictly necessary at the moment but may become so
        # in future
        if collides:
            self.collides = True
            self.rect = self.sprite.get_bounding_rect()
        if controllable:
            self.controllable = True
