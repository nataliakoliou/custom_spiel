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
        self.env.load()
        self.human.load()
        self.robot.load()

    def begin(self):
        self.env.init_state()

    def stage_over(self):
        for block in self.env.blocks:
            if block.is_hidden() or block.is_uncolored():
                return False
        return True

""" class MetaGame(Game):
    def __init__(self):
        super().__init__()

    def get_utilities(self):
        utilities = None
        return utilities """