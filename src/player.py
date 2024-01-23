import os
import torch
import random
import torch.optim as optim
from model import *
from utils import *

class Player:
    def __init__(self, type, model, criterion, optimizer, lr, weight_decay, bG, bP, wS):
        self.type = type
        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer
        self.lr = lr
        self.weight_decay = weight_decay
        self.bG = bG
        self.bP = bP
        self.wS = wS
        self.state = []
        self.space = []
        self.action = None
        self.q = 0
        self.reward = 0
        self.loss = 0
        self.R = 0
        self.L = 0

    @property
    def gain(self):
        return self.bG
    
    @property
    def penalty(self):
        suboptimal = len(self.action.block.neighbors) - 1
        return self.bP - suboptimal * self.gain
    
    @property
    def sanction(self):
        optimal = len(self.action.block.neighbors)
        return self.wS * optimal * self.gain

    @property
    def estimates(self):
        return self.model(self.state)

    def load(self, info):
        self.space = info.space
        self.state = info.state
        self.model = globals()[self.model](in_channels=1, output=len(self.space))
        self.optimizer = getattr(optim, self.optimizer)(
            self.model.parameters(), lr=self.lr, weight_decay=self.weight_decay)

    def update(self, info):
        self.state = info.state

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

    def optimize(self):
        target = self.reward + self.gamma * max(self.estimates)
        self.loss = self.criterion(self.q, target)
        self.optimizer.zero_grad()
        self.loss.backward()
        self.optimizer.step()
        self.R += self.reward
        self.L += self.loss

    def save_model(self, repeat):
        save_dir = f"{self.dir}/models"
        os.makedirs(save_dir, exist_ok=True)
        path = f"{save_dir}/repeat_{repeat}/{self.type}.pth"
        torch.save(self.model.state_dict(), path)