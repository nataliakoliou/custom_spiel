from collections import namedtuple
import numpy as np
import keyboard
import sys
import time
from grid import *
from player import *
from colors import *
from utils import *

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
        self.explore = int(0.9 * repeats)
        self.decay = round(1/self.explore, accuracy)
        self.freq = round(repeats/saves)

    @property
    def players(self):
        return [self.human, self.robot]
    
    @property
    def active_players(self):
        return [player for player in self.players if player.action is not None]
    
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

            ##################
            #self.print_state()
            ##################

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
                
                if keyboard.is_pressed('esc'):
                    print("User pressed the 'esc' key. Exiting the loop.")
                    #self.print_state()
                    print(self.human.action.applied, self.human.action.block.id, self.human.action.block.color.name, self.human.action.color.name)
                    print(self.robot.action.applied, self.robot.action.block.id, self.robot.action.block.color.name, self.robot.action.color.name)
                    break

                self.env.apply(self.actions)

                for player in self.active_players:
                    player.update(self.info)
                    if player.action.applied:
                        self.env.reward(player)
                        player.optimize()
                    player.save_model(self.dir, repeat) if repeat % self.freq == 0 else None

                steps += 1
                self.display_status(repeat, steps, delay=0)

            self.epsilon = max(round(self.epsilon - self.decay, self.acc), 0)

        #self.print_state()
        #print(self.human.action.applied, self.human.action.block.id, self.human.action.block.color.name, self.human.action.color.name)
        #print(self.robot.action.applied, self.robot.action.block.id, self.robot.action.block.color.name, self.robot.action.color.name)
                
    def stage_over(self):
        for block in self.env.state:
            if block.is_hidden() or block.is_uncolored():
                return False
        return True
    
    def display_status(self, repeat, steps, delay=0):
        f = '\rRepeat: {}, Steps: {} | Loss: (h={:.3f}, r={:.3f}), Reward: (h={:.3f}, r={:.3f})'
        sys.stdout.write(f.format(repeat + 1, steps, self.human.L / steps, self.robot.L / steps,
                                    self.human.R / steps, self.robot.R / steps))
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