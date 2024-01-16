import torch.nn as nn
from game import *
from settings import *

class DQN(nn.Module):
    def __init__(self, in_channels, output):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(in_channels, 64)
        self.fc2 = nn.Linear(64, 128)             
        self.fc3 = nn.Linear(128, output)  # output_size = num_blocks * num_colors
        self.relu = nn.ReLU()

    def forward(self, x):  # x: (batch, channels, height, width) = (batch, 1, 1, b)
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

"""class TQ():  # tabular qlearning (implements only the qtable)
...
"""

#############################################################################################################

""" class DQN(nn.Module):
    def __init__(self, game, input_channels, output_size):
        super(DQN, self).__init__()
        self.game = game
        self.num_blocks = get_size(self.game.env.blocks)

        self.conv1 = nn.Conv2d(input_channels, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)

        self.fc1 = nn.Linear(128 * 1 * self.num_blocks, 256)  # channels * height * width
        self.fc2 = nn.Linear(256, output_size)  # output_size = num_blocks * num_colors
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.relu(self.conv3(x))
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x"""