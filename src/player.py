import torch.optim as optim
from utils import *
from settings import *

class Player:
    def __init__(self, type):
        self.type = type
        self.model = None
        self.optimizer = None

    def create(self):
        return Human() if self.type == "human" else Robot()
    
    def assign(block, color):
        return

class Human(Player):
    def __init__(self):
        super().__init__('human')
        #self.model = globals().get(HUMAN_MODEL)(in_channels=1, output=get_size(COLORS))
        #self.optimizer = optim.AdamW(self.model.parameters(), **HUMAN_PARAMETERS)

class Robot(Player):
    def __init__(self):
        super().__init__('robot')
        #self.model = globals().get(ROBOT_MODEL)(in_channels=1, output=get_size(COLORS))
        #self.optimizer = optim.AdamW(self.model.parameters(), **ROBOT_PARAMETERS)