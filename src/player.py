import torch
import torch.nn as nn
import random
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
    def __init__(self, type, model, criterion, optimizer, lr, tau, batch_size, gamma, weight_decay, gain, penalty, sanction):
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

    def load(self, info):
        self.space = info.space
        self.state = info.state
        self.policy_net = globals()[self.model](input=self.features, output=len(self.space))
        self.target_net = globals()[self.model](input=self.features, output=len(self.space))
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.optimizer = getattr(optim, self.optimizer)(
            self.policy_net.parameters(), lr=self.lr, weight_decay=self.weight_decay)

    def update(self, info, type):
        if type=="current":
            self.state = info.state 
        elif type=="next":
            self.next = info.state
        elif type=="net":  # Soft update of the target network's weights: θ′ ← τ θ + (1 −τ )θ′
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
            s = torch.tensor([[block.color.encoding for block in self.state]], dtype=torch.float32)
            self.q = self.policy_net(s)[0, self.action.id].item()

    def exploit(self):
        with torch.no_grad():
            s = torch.tensor([[block.color.encoding for block in self.state]], dtype=torch.float32)
            self.q, id  = self.policy_net(s).max(1)
        self.action = self.space[id]

        # tensor([[0.2333, 0.2827]]).max(1) returns:
        # torch.return_types.max(
        # values=tensor([0.2827]),
        # indices=tensor([1])
        # )

    def expand_memory(self):
        s = torch.tensor([[block.color.encoding for block in self.state]], dtype=torch.float32)  # [ [[0 1 0 0], ... , [0 0 1 0]] ]
        a = torch.tensor([[self.action.id]])  # [[1]]
        n = torch.tensor([[block.color.encoding for block in self.next]], dtype=torch.float32)  # [ [[0 1 0 0], ... , [0 0 1 0]] ]
        r = torch.tensor([self.reward])  # [25]
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
        return tuple([torch.cat(getattr(batch, field)) for field in fields])
    
        #states: [ [[0 1 0 0], ... , [0 0 1 0]], ..., [[0 1 0 0], ... , [0 0 1 0]] ]
        #actions: [[1], [5], ...]
        #nexts: [ [[0 1 0 0], ... , [0 0 1 0]], ..., [[0 1 0 0], ... , [0 0 1 0]] ]
        #rewards: [25, -4, ...]