from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np
import sys
import torch
import time
#from grid import *
#from player import *
#from colors import *
#from utils import *

class Game:
    def __init__(self, title, repeats, env, human, robot, epsilon, cutoff, accuracy, saves, dir):
        self.title = title
        self.repeats = repeats
        self.env = env
        self.human = human
        self.robot = robot
        self.epsilon = epsilon
        self.acc = accuracy
        self.dir = dir
        self.explore = int(cutoff * repeats)
        self.decay = round(1/self.explore, accuracy)
        self.freq = repeats//saves
        self.losses = {'human': [], 'robot': []}
        self.load()

    @property
    def players(self):
        return [self.human, self.robot]
    
    @property
    def actions(self):
        Actions = namedtuple('Actions', ['former', 'latter'])
        return Actions(self.human.action, self.robot.action)
        
    def load(self):
        self.env.load()
        [player.load(data=self.env.state) for player in self.players]

    def qlearning(self):
        steps = 0
        for repeat in range(self.repeats):
            self.env.reset()
            while not self.stage_over():
                self.env.step()
                for player in self.players:
                    player.update(type="current", data=self.env.state)
                    if np.random.rand() < self.epsilon:
                        player.explore()
                    else:
                        player.exploit()
                self.env.apply(self.actions)
                for player in self.players:
                    player.update(type="next", data=self.env.state)
                    self.env.reward(player)
                    player.expand_memory()
                    player.update(type="current", data=self.env.state)
                    player.optimize()
                    player.update(type="net")
                steps += 1
                self.display_status(repeat, steps, delay=0)
            for type in ['human', 'robot']:
                player = getattr(self, type)
                self.save_model(player, repeat) if repeat % self.freq == 0 else None
                self.losses[type].append(player.L / steps)
            self.epsilon = max(round(self.epsilon - self.decay, self.acc), 0)
        self.graph_losses()
        self.graph_statistics(phase="Exploitation", steps=steps)
                
    def stage_over(self):
        for block in self.env.state:
            if block.is_hidden() or block.is_uncolored():
                return False
        return True
    
    def save_model(self, player, repeat):
        path = get_path(dir=self.dir, folder=("models", f"repeat_{repeat}"), name=f"{player.type}.pth")
        torch.save(player.policy_net.state_dict(), path)
    
    def graph_losses(self):
        yh = self.losses['human']
        yr = self.losses['robot']
        plt.figure(figsize=(10, 6))
        plt.plot(yh, label='Human', color='red')
        plt.plot(yr, label='Robot', color='blue')
        plt.title('Training Losses')
        plt.xlabel('Steps')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid(True)
        path = get_path(dir=self.dir, folder='static', name='losses.png')
        plt.savefig(path)
        plt.close()
    
    def graph_statistics(self, phase, steps, width=0.4):
        x_labels = [(action.block.id, action.color.name) for action in self.human.space]
        x = list(range(len(self.human.space)))
        yh = [action.times[phase]/steps for action in self.human.space]
        yr = [action.times[phase]/steps for action in self.robot.space]
        plt.figure(figsize=(12, 12))
        plt.bar(x, yh, color='red', width=width, label='Human')
        plt.bar([id + width for id in x], yr, color='blue', width=width, label='Robot')
        plt.title(f'{phase} Statistics')
        plt.xlabel('Action')
        plt.ylabel('Frequency')
        plt.xticks([i + width/2 for i in x], x_labels, rotation=45, ha="right")  # Added x-axis labels
        plt.legend()
        plt.grid(True)
        path = get_path(dir=self.dir, folder='static', name=f'{phase.lower()}_statistics.png')
        plt.savefig(path)
        plt.close()
    
    def display_status(self, repeat, steps, delay=0):
        f = '\rRepeat: {}, Steps: {} | Loss: (h={:.3f}, r={:.3f})'
        sys.stdout.write(f.format(repeat + 1, steps, self.human.L/steps, self.robot.L/steps))
        sys.stdout.flush()
        time.sleep(delay)