import numpy as np
from grid import *
from player import *
from colors import *
from utils import *

class Game:
    def __init__(self, title, repeats, env, human, robot, gamma, epsilon, accuracy):
        self.title = title
        self.repeats = repeats
        self.env = env
        self.human = human
        self.robot = robot
        self.steps = repeats * env.rows * env.cols
        self.gamma = gamma
        self.epsilon = epsilon
        self.accuracy = accuracy
        self.exploration = int(0.9 * self.steps)
        self.exploitation = self.steps - self.exploration
        self.decay = 1/self.explore
    
    @property  # use: access variables from other class (change will be reflected)
    def info(self):
        return (self.env.state, self.env.space)
        
    def load(self):
        self.env.load()
        self.human.update(*self.info, load=True)
        self.robot.update(*self.info, load=True)

    def reset(self):
        self.env.reset()
        self.human.reset()
        self.robot.reset()

    def qlearning(self, dir):
        for _ in range(self.repeats):
            self.reset()
            while not self.stage_over():
                self.env.step()
                self.epsilon = round(self.epsilon - (self.decay), self.accuracy) 
                for player in [self.human, self.robot]:
                    if np.random.rand() < self.epsilon:
                        player.explore()
                    else:
                        player.expoit()
                    #TODO: self.env.apply(player.action)
                for player in [self.human, self.robot]:
                    player.update(*self.info)
                    reward = ... # env/player specific!
                    player.optimize(reward)
            #TODO: print(f"Episode {stage + 1}/{STAGES}, Total Reward: {total_reward}")

    def stage_over(self):
        for block in self.env.state:
            if block.is_hidden() or block.is_uncolored():
                return False
        return True
    
    def simulate(self, dir):
        pass

""" class MetaGame(Game):
    def __init__(self):
        super().__init__()

    def get_utilities(self):
        utilities = None
        return utilities """