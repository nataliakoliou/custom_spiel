import random
import torch.optim as optim
from environment import *
from utils import *
from settings import *

class Player:
    def __init__(self, type):
        self.type = type
        self.model = None
        self.optimizer = None
        self.space = []
        self.action = None
    
    def load(self):
        for counter, (block, color) in enumerate(product(range(BLOCKS.value), COLORS)):
            action = Action(block, color)
            action.id = counter
            self.space.append(action)

    def play(self, random=False):
        if random:
            self.action = random.choice(self.space)
            self.action.increment("exploration")
        else:
            pass

class Human(Player):
    def __init__(self):
        super().__init__('human')
        #self.model = globals().get(HUMAN_MODEL)(in_channels=1, output=get_size(COLORS))
        #self.optimizer = optim.AdamW(self.model.parameters(), **HUMAN_PARAMETERS)
        self.space = []
        self.action = None

class Robot(Player):
    def __init__(self):
        super().__init__('robot')
        #self.model = globals().get(ROBOT_MODEL)(in_channels=1, output=get_size(COLORS))
        #self.optimizer = optim.AdamW(self.model.parameters(), **ROBOT_PARAMETERS)
        self.space = []
        self.action = None

class Action:
    def __init__(self, block, color):
        self.block = block
        self.color = color
        self.id = None
        self.counter = {"exploration": 0, "exploitation": 0}

    def increment(self, phase):
        self.counter[phase] += 1