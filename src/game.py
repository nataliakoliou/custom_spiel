from itertools import chain
from environment import *
from player import *
from algorithm import *
from utils import *
from settings import *

class Game:
    def __init__(self):
        self.env = Grid()
        self.human = Player('human').create()
        self.robot = Player('robot').create()
        self.state = []
        
    def load(self):
        self.env.configure()
        self.define_colors()

        """
        self.env.display()
        self.display_colors()
        self.env.grid[0][1].display_neighbors()
        self.env.display_hidden_cells()
        self.env.display_blocks()
        """
    
    def define_colors(self):
        global COLORS
        max_neighbors = get_max(len(cell.neighbors) for cell in chain.from_iterable(self.env.grid))
        num_colors = max_neighbors + 1
        COLORS[:] = COLORS[:num_colors]

    """def reset(self):
        self.state = [-1 for _ in range(get_size(self.env.blocks))] #-1 indicates NC
        for cells in self.env.blocks.values():
            for cell in cells:
                cell.colour = NC

    def stage_over(self):
        ...

    def apply(self, action):
        ..."""


    def display_colors(self):
        print("Number of colors:", get_size(COLORS))
        print("Colors:", [color.name for color in COLORS])
        
""" class MetaGame(Game):
    def __init__(self):
        super().__init__()

    def get_utilities(self):
        utilities = None
        return utilities """