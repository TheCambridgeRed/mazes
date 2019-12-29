class Cell:
    # basic cell class with a position and a representation for debugging
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        
    def __repr__(self):
        return f'Cell [{self.x}],[{self.y}]'
