import torch
import torch.nn as nn
import numpy as np
from game import *
from settings import *

class DQN(nn.Module):
    def __init__(self, input_channels, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_channels, 64)
        self.fc2 = nn.Linear(64, 128)             
        self.fc3 = nn.Linear(128, output_size)  # output_size = num_blocks * num_colors
        self.relu = nn.ReLU()

    def forward(self, x):  # x: (batch, channels, height, width) = (batch, 1, 1, b)
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

"""class TQ():  # tabular qlearning (implements only the qtable)
..."""

class Learner:
    def __init__(self, game):
        self.game = game
        self.epsilon = EPSILON

    def run(self):
        for stage in range(STAGES):
            state = self.game.reset()
            total_reward = 0

            while not self.game.is_over():

                self.epsilon = round(self.epsilon - (DECAY), ACCURACY)

                action = self.explore(state) if np.random.rand() < self.epsilon else self.exploit(state)

                next_state, reward = self.game.step(action)

                target = reward + self.gamma * torch.max(self.forward(torch.FloatTensor(next_state).unsqueeze(0)))
                q_value = self.forward(torch.FloatTensor(state).unsqueeze(0))[0, action]
                loss = loss(q_value, target)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                total_reward += reward
                state = next_state

            print(f"Episode {stage + 1}/{STAGES}, Total Reward: {total_reward}")

    def explore(self, state):
        return self.game.sample_random_action()

    def exploit(self, state):
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        q_values = self.forward(state_tensor)
        return q_values.argmax().item()

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