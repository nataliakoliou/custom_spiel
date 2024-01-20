import random
import torch.nn as nn
from utils import *

class Player:
    def __init__(self, type, model, optimizer, lr, weight_decay):
        self.type = type
        self.model = model
        self.optimizer = optimizer
        self.lr = lr
        self.weight_decay = weight_decay
        self.state = []
        self.space = []
        self.action = None
        self.q = 0
        self.loss = 0
        self.rewards = 0

    @property
    def estimates(self):
        return self.model(self.state)
    
    def reset(self):
        self.rewards = 0

    def update(self, state, space, load=False):
        self.space = space if load else self.space
        self.state = state

    def explore(self):
        self.action = random.choice(self.space)
        q_values = self.estimates
        self.q = q_values[self.action.id]
        self.action.increment("explore")

    def exploit(self):
        q_values = self.estimates
        id = get_id(list=q_values, value=max(q_values))
        self.q = q_values[id]
        self.action = self.space[id]
        self.action.increment("exploit")

    def optimize(self, reward):
        self.rewards += reward
        target = reward + self.gamma * max(self.estimates)
        self.loss = nn.MSELoss()(self.q, target)
        self.optimizer.zero_grad()
        self.loss.backward()
        self.optimizer.step()