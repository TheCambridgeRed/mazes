class Level:
    # a Level is defined by its width, height, scale (for drawing) and
    # a list of MazeCells which have their own state information
    def __init__(self, x, y, scale, cells_list):
        self.x = x
        self.y = y
        self.scale = scale
        self.cells_list = cells_list
    
