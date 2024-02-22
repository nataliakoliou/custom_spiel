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
#from settings import *

class Simulator:
    def __init__(self, repeats, env, human, robot, colors):
        self.repeats = repeats
        self.env = env
        self.human = human
        self.robot = robot
        self.colors = colors

class QLearner:
    def __init__(self, name, env, player, repeats, epsilon, cutoff):
        self.name = name
        self.env = env
        self.player = player
        self.repeats = repeats
        self.epsilon = epsilon
        self.explore = int(cutoff * repeats)
        self.decay = round(1/self.explore, ACCURACY)
        self.color = get_color(player.type)
        self.loss = []
        self.steps = 0

    def run(self):
        self.env.load()
        self.player.load(data=self.env.state)
        for repeat in range(self.repeats):
            self.env.reset()
            while not self.stage_over():
                self.env.step()
                self.player.update(type="current", data=self.env.state)
                if np.random.rand() < self.epsilon:
                    self.player.explore()
                else:
                    self.player.exploit()
                
                ###########################################################################
                block_color_before = self.env.state[self.player.action.block.id].color.name
                ###########################################################################

                self.env.apply(self.player.action)
                self.player.update(type="next", data=self.env.state)
                self.env.reward(self.player)
                self.player.expand_memory()
                self.player.update(type="current", data=self.env.state)
                self.player.optimize()
                self.player.update(type="net")
                self.steps += 1
                self.display_status(repeat, delay=0)
            self.loss.append(self.player.L / self.steps)
            self.epsilon = max(round(self.epsilon - self.decay, ACCURACY), 0)
        self.save_model()
        self.graph_loss()
        self.graph_statistics(phase="Exploitation")
       
        #####################################################################################
        self.print_state()
        print(self.player.action.block.id, block_color_before, self.player.action.color.name)
        #####################################################################################
                
    def stage_over(self):
        for block in self.env.state:
            if block.is_hidden() or block.is_uncolored():
                return False
        return True
    
    def save_model(self):
        path = get_path(dir=DIR, folder=("models", f"{self.player.type}"), name=f"{self.name}.pth")
        torch.save(self.player.policy_net.state_dict(), path)
    
    def graph_loss(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.loss, label=self.player.type, color=self.color)
        plt.title('Training Loss')
        plt.xlabel('Steps')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid(True)
        path = get_path(dir=DIR, folder='static', name='loss.png')
        plt.savefig(path)
        plt.close()
    
    def graph_statistics(self, phase, width=0.4):
        x_labels = [(action.block.id, action.color.name) for action in self.player.space]
        x = list(range(len(self.player.space)))
        y = [action.times[phase]/self.steps for action in self.player.space]
        plt.figure(figsize=(12, 12))
        plt.bar(x, y, color=self.color, width=width, label=self.player.type)
        plt.title(f'{phase} Statistics')
        plt.xlabel('Action')
        plt.ylabel('Frequency')
        plt.xticks([i + width/2 for i in x], x_labels, rotation=45, ha="right")
        plt.legend()
        plt.grid(True)
        path = get_path(dir=DIR, folder='static', name=f'{phase.lower()}_statistics.png')
        plt.savefig(path)
        plt.close()
    
    def display_status(self, repeat, delay=0):
        f = '\rRepeat: {}, Steps: {} | Loss: {:.3f})'
        sys.stdout.write(f.format(repeat + 1, self.steps, self.player.L/self.steps))
        sys.stdout.flush()
        time.sleep(delay)

    ###########################################################################################################################################
    def print_state(self):
        print()
        print("State:")
        for block in self.env.state: print(f"Block {block.id}:", (block.id, block.color.__class__.__name__, len(block.cells), block.neighbors))
    ###########################################################################################################################################