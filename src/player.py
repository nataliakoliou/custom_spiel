import torch.optim as optim
from utils import *
from settings import *

class Player:
    def __init__(self, type):
        self.type = type
        self.model = None
        self.optimizer = None
        self.action = None
    
    def perform(self):
        if self.action:
            block, color = self.action
            block.set_color(color)
        else:
            # Handle the case when self.action is None
            pass

class Human(Player):
    def __init__(self):
        super().__init__('human')
        self.model = globals().get(HUMAN_MODEL)(in_channels=1, output=get_size(COLORS))
        self.optimizer = optim.AdamW(self.model.parameters(), **HUMAN_PARAMETERS)
        self.action = (Block(2), Red())

class Robot(Player):
    def __init__(self):
        super().__init__('robot')
        self.model = globals().get(ROBOT_MODEL)(in_channels=1, output=get_size(COLORS))
        self.optimizer = optim.AdamW(self.model.parameters(), **ROBOT_PARAMETERS)
        self.action = None