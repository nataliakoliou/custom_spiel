import copy
import torch
import numpy as np
from game import *
from settings import *

class Algorithm:
    def __init__(self, game):
        self.game = game
        self.human_action = None
        self.robot_action = None

    def qlearning(self):
        self.game.env.init_state()

        for repeat in range(REPEATS):
            self.game.reset()
            total_reward = 0

            while not self.game.stage_over():
                global EPSILON
                EPSILON = round(EPSILON - (DECAY), ACCURACY)
                self.game.env.prev_state = copy.deepcopy(self.game.env.state)

                for player in [self.game.human, self.game.robot]:
                    player.action = self.explore(player) if np.random.rand() < EPSILON else self.exploit(player)
                    player.reward = self.game.step(player.action)

                target = reward + self.gamma * torch.max(self.forward(torch.FloatTensor(next_state).unsqueeze(0)))
                q_value = self.forward(torch.FloatTensor(state).unsqueeze(0))[0, action]
                loss = loss(q_value, target)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                total_reward += reward
                state = next_state

            print(f"Episode {stage + 1}/{STAGES}, Total Reward: {total_reward}")

    def explore(self, player):
        return self.game.sample_random_action()

    def exploit(self, player):
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        q_values = self.forward(state_tensor)
        return q_values.argmax().item()