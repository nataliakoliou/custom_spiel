from itertools import chain
from environment import *
from player import *
from algorithm import *
from colors import *
from utils import *
from settings import *

class Game:
    def __init__(self):
        self.env = Grid()
        self.human = Human()
        self.robot = Robot()
        
    def load(self):
        self.env.configure()
        self.define_colors()

        """
        self.env.display()
        self.display_colors()
        self.env.grid[0][0].display_neighbors()
        self.env.blocks[0].display_neighbors()
        self.env.display_hidden_cells()
        self.env.display_blocks()
        """
    
    def define_colors(self):
        global COLORS
        max_neighbors = get_max(len(cell.neighbors) for cell in chain.from_iterable(self.env.grid))
        num_colors = max_neighbors + 1
        COLORS[:] = COLORS[:num_colors]

    def reset(self):
        self.env.reset()
        #self.human.reset()
        #self.robot.reset()

    def stage_over(self):
        for block in self.env.blocks:
            if block.is_hidden() or block.is_uncolored():
                return False
        return True



    """
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