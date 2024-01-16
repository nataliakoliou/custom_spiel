import torch
import numpy as np
from game import *
from settings import *

class Algorithm:
    def __init__(self, game):
        self.game = game

    def qlearning(self):
        for repeat in range(REPEATS):
            state = self.game.reset()
            total_reward = 0

            while not self.game.stage_over():
                global EPSILON
                EPSILON = round(EPSILON - (DECAY), ACCURACY)

                action = self.explore(state) if np.random.rand() < EPSILON else self.exploit(state)

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