from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np
import sys
import torch
import time
import os
#from grid import *
#from player import *
#from colors import *
#from utils import *

class Game:
    def __init__(self, title, repeats, env, human, robot, epsilon, accuracy, saves, dir):
        self.title = title
        self.repeats = repeats
        self.env = env
        self.human = human
        self.robot = robot
        self.epsilon = epsilon
        self.acc = accuracy
        self.saves = saves
        self.dir = dir
        self.explore = int(0.98 * repeats)
        self.decay = round(1/self.explore, accuracy)
        self.freq = round(repeats/saves)
        self.losses = {'human': [], 'robot': []}

    @property
    def players(self):
        return [self.human, self.robot]
    
    @property
    def info(self):
        Info = namedtuple('Info', ['state', 'space'])
        return Info(self.env.state, self.env.space)
    
    @property
    def actions(self):
        Actions = namedtuple('Actions', ['former', 'latter'])
        return Actions(self.human.action, self.robot.action)
        
    def load(self):

        ########################
        #self.print_exploration()
        #self.print_decay()
        #self.print_dir()
        ########################

        self.env.load()

        #######################
        #self.print_num_blocks()
        #self.print_state()
        #######################

        self.human.load(self.info)
        self.robot.load(self.info)

        ####################
        #self.print_actions()
        ####################

    def qlearning(self):
        steps = 0
        for repeat in range(self.repeats):
            self.env.reset()

            while not self.stage_over():
                self.env.step()

                ##################
                #self.print_state()
                ##################

                for player in self.players:
                    if np.random.rand() < self.epsilon:
                        player.explore()

                        ###########################################################################
                        #print(player.type, ":", (player.action.block.id, player.action.color.name))
                        ###########################################################################

                    else:
                        player.exploit()

                        ###########################################################################
                        #print(player.type, ":", (player.action.block.id, player.action.color.name))
                        ###########################################################################

                self.env.apply(self.actions)

                for player in self.players:
                    player.update(self.info, type="next")
                    self.env.reward(player)
                    player.expand_memory()
                    player.update(self.info, type="current")
                    player.optimize()
                    player.update(self.info, type="net")

                steps += 1
                self.display_status(repeat, steps, delay=0)

            for type in ['human', 'robot']:
                player = getattr(self, type)
                self.save_model(player, repeat) if repeat % self.freq == 0 else None
                self.losses[type].append(player.L / steps)
            self.epsilon = max(round(self.epsilon - self.decay, self.acc), 0)

        self.graph_losses()

        self.print_state()
        print(self.human.action.applied, self.human.action.block.id, self.human.action.block.color.name, self.human.action.color.name)
        print(self.robot.action.applied, self.robot.action.block.id, self.robot.action.block.color.name, self.robot.action.color.name)
                
    def stage_over(self):
        for block in self.env.state:
            if block.is_hidden() or block.is_uncolored():
                return False
        return True
    
    def save_model(self, player, repeat):
        save_dir = os.path.join(self.dir, "models", f"repeat_{repeat}")
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, f"{player.type}.pth")
        torch.save(player.policy_net.state_dict(), path)
    
    def graph_losses(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.losses['human'], label='Human Loss', color='red')
        plt.plot(self.losses['robot'], label='Robot Loss', color='blue')
        plt.title('Training Losses')
        plt.xlabel('Steps')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid(True)
        save_dir = os.path.join(self.dir, 'static')
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, 'losses.png')
        plt.savefig(path)
    
    def display_status(self, repeat, steps, delay=0):
        f = '\rRepeat: {}, Steps: {} | Loss: (h={:.3f}, r={:.3f})'
        sys.stdout.write(f.format(repeat + 1, steps, self.human.L/steps, self.robot.L/steps))
        sys.stdout.flush()
        time.sleep(delay)

    def simulate(self, dir):
        pass

#######################################################################################################################
    
    def print_actions(self):
        print()
        print("Human Action Space:")
        for action in self.human.space: print(f"Action {action.id}:", (action.block.id, action.color.__class__.__name__, action.counter, action.invalid))
        print()
        print("Robot Action Space:")
        for action in self.robot.space: print(f"Action {action.id}:", (action.block.id, action.color.__class__.__name__, action.counter, action.invalid))

    def print_colors(self):
        print()
        print("Colors:")
        for color in [HIDDEN, NC] + COLORS: print(f"{color.__class__.__name__}:", (color.rgb, color.encoding))

    def print_state(self):
        print()
        print("State:")
        for block in self.env.state: print(f"Block {block.id}:", (block.id, block.color.__class__.__name__, len(block.cells), block.neighbors))

    def print_num_blocks(self):
        print()
        print("Number of blocks:", self.env.num_blocks)

    def print_dir(self):
        print()
        print("Directory:", self.dir)

    def print_decay(self):
        print()
        print("Epsilon decay:", self.decay)

    def print_exploration(self):
        print()
        print("Exploration time:", self.explore, "/", self.repeats * self.env.rows * self.env.cols, "(where epsilon reaches 0)")

""" class MetaGame(Game):
    def __init__(self):
        super().__init__()

    def get_utilities(self):
        utilities = None
        return utilities """