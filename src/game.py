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
        self.human_actions = []
        self.robot_actions = []
        
    def load(self):
        self.env.configure()
        self.define_colors()
        self.define_actions()

        """
        #NOTE: DISPLAYS ENVIRONMENT
        for row in self.env.grid:
            print('\t'.join(str(cell.id) for cell in row))
        """
            
        """
        #NOTE: DISPLAYS COLORS
        print("Number of colors:", get_size(COLORS))
        print("Colors:", [color.name for color in COLORS])
        """

        """
        #NOTE: DISPLAYS CELL'S NEIGHBORS
        cell = self.env.grid[0][0]
        print(f"Neighbors of cell ({cell.row}, {cell.col}) with id {cell.id}: {','.join(str(neighbor.id) for neighbor in cell.neighbors)}.")
        """

        """
        #NOTE: DISPLAYS BLOCK'S NEIGHBORS
        block = self.env.blocks[0]
        print(f"Neighbors of block with id {block.id}: {','.join(str(neighbor.id) for neighbor in block.neighbors)}.")
        """

        """
        #NOTE: DISPLAYS COLORS
        print("Number of blocks:", get_size(self.env.blocks))
        """
    
    def define_colors(self):
        global COLORS
        max_neighbors = get_max(len(cell.neighbors) for cell in chain.from_iterable(self.env.grid))
        num_colors = max_neighbors + 1
        COLORS[:] = COLORS[:num_colors]

    def define_actions(self):
        for player, actions in [(self.human, self.human_actions), (self.robot, self.robot_actions)]:
            for counter, (block, color) in enumerate(product(self.env.blocks, COLORS)):
                action = Action(player, block, color)
                action.id = counter
                actions.append(action)

    def reset(self):
        self.env.reset()
        #self.human.reset()
        #self.robot.reset()

    def stage_over(self):
        for block in self.env.blocks:
            if block.is_hidden() or block.is_uncolored():
                return False
        return True

class Action:
    def __init__(self, player, block, color):
        self.player = player
        self.block = block
        self.color = color
        self.id = None
        self.explore = 0
        self.exploit = 0

    def explore(self):
        self.explore += 1

    def exploit(self):
        self.exploit += 1

    def apply(self):
        return

""" class MetaGame(Game):
    def __init__(self):
        super().__init__()

    def get_utilities(self):
        utilities = None
        return utilities """