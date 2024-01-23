from tqdm import tqdm
from collections import namedtuple
import numpy as np
from grid import *
from player import *
from colors import *
from utils import *

class Game:
    def __init__(self, title, repeats, env, human, robot, gamma, epsilon, accuracy, dir):
        self.title = title
        self.repeats = repeats
        self.env = env
        self.human = human
        self.robot = robot
        self.gamma = gamma
        self.epsilon = epsilon
        self.accuracy = accuracy
        self.dir = dir
        self.explore = int(0.9 * repeats * env.rows * env.cols)
        self.decay = round(1/self.explore, accuracy)

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
        self.print_exploration()
        self.print_decay()
        self.print_dir()
        ########################

        self.env.load()

        #######################
        self.print_num_blocks()
        self.print_state()
        #######################

        self.human.load(self.info)
        self.robot.load(self.info)

        ####################
        self.print_actions()
        ####################

    def qlearning(self):
        steps = 0
        for repeat in tqdm(range(self.repeats), desc='Q-Learning', total=self.repeats):
            self.env.reset()
            pbar = tqdm(desc=f'Repeat {repeat + 1}/{self.repeats}')

            while not self.stage_over():
                self.env.step()

                for player in self.players:
                    if np.random.rand() < self.epsilon:
                        player.explore()
                    else:
                        player.expoit()

                self.env.apply(self.actions)

                for player in self.players:
                    player.update(self.info)
                    self.env.reward(player)
                    player.optimize()
                    player.save_model(repeat) if (repeat+1) % 2 == 0 else None

                steps += 1
                self.epsilon = max(round(self.epsilon - self.decay, self.accuracy), 0) 

                pbar.set_postfix({'Human Loss': '{0:.3f}'.format(self.human.L/steps),
                                  'Robot Loss': '{0:.3f}'.format(self.robot.L/steps),
                                  'Human Reward': '{0:.3f}'.format(self.human.R/steps),
                                  'Robot Reward': '{0:.3f}'.format(self.robot.R/steps)})

    def stage_over(self):
        for block in self.env.state:
            if block.is_hidden() or block.is_uncolored():
                return False
        return True
    
    def simulate(self, dir):
        pass

#######################################################################################################################
    
    def print_actions(self):
        print()
        print("Human Action Space:")
        for action in self.human.space: print(f"Action {action.id}:", (action.block.id, action.color.__class__.__name__, action.counter, action.invalid, action.distinct))
        print()
        print("Robot Action Space:")
        for action in self.robot.space: print(f"Action {action.id}:", (action.block.id, action.color.__class__.__name__, action.counter, action.invalid, action.distinct))

    def print_colors(self):
        print()
        print("Colors:")
        for color in [HIDDEN, NC] + COLORS: print(f"{color.__class__.__name__}:", (color.rgb, color.encoding))

    def print_state(self):
        print()
        print("State:")
        for block in self.env.state: print(f"Block {block.id}:", (block.id, block.color.__class__.__name__, len(block.cells), block.neighbors))
        self.print_colors()

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