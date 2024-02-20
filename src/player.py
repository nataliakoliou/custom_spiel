import torch
import torch.nn as nn
import random
from itertools import product
from copy import deepcopy
import torch.optim as optim
from collections import namedtuple, deque
#from model import *
#from utils import *

class ReplayMemory(object):
    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)
        self.Transition = namedtuple('Transition', ('state', 'action', 'next', 'reward'))

    def push(self, *args):
        self.memory.append(self.Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

class Player:
    def __init__(self, type, model, criterion, optimizer, lr, tau, batch_size, gamma, weight_decay, gain, penalty, sanction, device):
        self.type = type
        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer
        self.lr = lr
        self.tau = tau
        self.batch_size = batch_size
        self.gamma = gamma
        self.weight_decay = weight_decay
        self.gain = gain
        self.penalty = penalty
        self.sanction = sanction
        self.device = device
        self.memory = ReplayMemory(10000)
        self.policy_net = None
        self.target_net = None
        self.state = []
        self.next = []
        self.space = []
        self.action = None
        self.q = 0
        self.qvalues = 0
        self.reward = 0
        self.L = 0
    
    @property
    def features(self):
        return len(self.space)+ 2*len(self.state)  # num_blocks * num_all_colors
    
    def statistics(self, phase):
        return sorted(self.space, key=lambda action: action.times[phase], reverse=True)

    def load(self, data):
        self.update("current", data)
        for counter, (block, color) in enumerate(product(self.state, COLORS)):
            action = Action(block, color)
            action.id = counter
            self.space.append(action)
        self.policy_net = globals()[self.model](input=self.features, output=len(self.space)).to(self.device)
        self.target_net = globals()[self.model](input=self.features, output=len(self.space)).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.optimizer = getattr(optim, self.optimizer)(
            self.policy_net.parameters(), lr=self.lr, weight_decay=self.weight_decay)

    def update(self, type, data=None):
        if type == "current":
            self.state = deepcopy(data)
            for action in self.space:
                action.block = self.state[action.block.id]
        elif type == "next":
            self.next = deepcopy(data)
        elif type == "net":  # Soft update of the target network's weights: θ′ ← τθ + (1−τ)θ′
            tnsd = self.target_net.state_dict()
            pnsd = self.policy_net.state_dict()
            for key in pnsd:
                tnsd[key] = pnsd[key]*self.tau + tnsd[key]*(1-self.tau)
            self.target_net.load_state_dict(tnsd)
        else:
            raise ValueError("Invalid update type.")

    def explore(self):
        self.action = random.choice(self.space)
        with torch.no_grad():
            s = torch.tensor([[block.color.encoding for block in self.state]], dtype=torch.float32).to(self.device)
            self.q = self.policy_net(s)[0, self.action.id].item()
        self.action.increment("Exploration")

    def exploit(self):
        with torch.no_grad():
            s = torch.tensor([[block.color.encoding for block in self.state]], dtype=torch.float32).to(self.device)
            self.q, id  = self.policy_net(s).max(1)
        self.action = self.space[id]
        self.action.increment("Exploitation")

    def expand_memory(self):
        s = torch.tensor([[block.color.encoding for block in self.state]], dtype=torch.float32).to(self.device)  # [ [[0 1 0 0], ... , [0 0 1 0]] ]
        a = torch.tensor([[self.action.id]]).to(self.device)  # [[1]]
        n = torch.tensor([[block.color.encoding for block in self.next]], dtype=torch.float32).to(self.device)  # [ [[0 1 0 0], ... , [0 0 1 0]] ]
        r = torch.tensor([self.reward]).to(self.device)  # [25]
        self.memory.push(s, a, n, r)

    def optimize(self):
        if len(self.memory) < self.batch_size:
            return
        states, actions, nexts, rewards = self.get_batch()
        self.qvalues = self.policy_net(states).gather(1, actions)  # tensor([[4.3001], [4.1578], ... ])
        with torch.no_grad():
            target = rewards + self.gamma * self.target_net(nexts).max(1).values  # tensor([4.3001, 4.1578, ... ])
        loss = self.criterion(self.qvalues, target.unsqueeze(1))  # add extra dimension to target: tensor([[4.3001], [4.1578], ... ])
        self.optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)
        self.optimizer.step()
        self.L += loss.item()

    def get_batch(self):
        transitions = self.memory.sample(self.batch_size)
        batch = self.memory.Transition(*zip(*transitions))
        fields = self.memory.Transition._fields
        return tuple([torch.cat(getattr(batch, field)).to(self.device) for field in fields])
    
class Action:
    def __init__(self, block, color):
        self.block = block
        self.color = color
        self.id = None
        self.invalid = 0  # 0 means false 1 means true
        self.times = {"Exploration": 0, "Exploitation": 0, "Simulation": 0}

    def set_invalid(self):
        self.invalid = int(not self.block.is_uncolored())

    def increment(self, phase):
        self.times[phase] += 1

    def __eq__(self, other):
        return isinstance(other, Action) and self.block == other.block
    
    def __ne__(self, other):
        return not self.__eq__(other)