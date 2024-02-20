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

class QLearner:
    def __init__(self, repeats, env, player, epsilon, cutoff, accuracy, saves, color, dir):
        self.repeats = repeats
        self.env = env
        self.player = player
        self.epsilon = epsilon
        self.acc = accuracy
        self.dir = dir
        self.explore = int(cutoff * repeats)
        self.decay = round(1/self.explore, accuracy)
        self.color = color
        self.freq = repeats//saves
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
            self.save_model(repeat) if repeat % self.freq == 0 else None
            self.loss.append(self.player.L / self.steps)
            self.epsilon = max(round(self.epsilon - self.decay, self.acc), 0)
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
    
    def save_model(self,repeat):
        path = get_path(dir=self.dir, folder=("models", f"repeat_{repeat}"), name=f"{self.player.type}.pth")
        torch.save(self.player.policy_net.state_dict(), path)
    
    def graph_loss(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.loss, label=self.player.type, color=self.color)
        plt.title('Training Loss')
        plt.xlabel('Steps')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid(True)
        path = get_path(dir=self.dir, folder='static', name='loss.png')
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
        path = get_path(dir=self.dir, folder='static', name=f'{phase.lower()}_statistics.png')
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