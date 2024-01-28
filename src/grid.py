import random
from itertools import product, chain
from colors import *
from utils import *

class Grid:
    def __init__(self, rows, cols, merge, minR, wR):
        self.rows = rows
        self.cols = cols
        self.merge = merge
        self.minR = minR
        self.wR = wR
        self.grid = [[Cell(i, j) for j in range(cols)] for i in range(rows)]
        self.state, self.space = [], []
        self.num_blocks = 0

    @property
    def maxR(self):
        return int(self.minR + self.wR * self.num_blocks)

    def load(self):
        self.load_cells()
        self.load_state()
        self.load_colors()
        self.load_space()

    def load_cells(self):
        for i, j in product(range(self.rows), range(self.cols)):
            cell = self.grid[i][j]
            cell.neighbors = [self.grid[i + dr][j + dc] for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]
                              if Cell(i + dr, j + dc).is_valid(self.rows, self.cols)]
            ids = [neighbor.id for neighbor in cell.neighbors if neighbor.id is not None]
            if random.random() < self.merge and ids:
                cell.id = random.choice(ids)
            else:
                cell.id = self.num_blocks
                self.num_blocks += 1

    def load_state(self):
        self.state = [Block(id) for id in range(self.num_blocks)]
        for cell in chain.from_iterable(self.grid):
            self.state[cell.id].cells.append(cell)
        for block in self.state:
            shared = set()
            for cell in block.cells:
                shared |= {neighbor.id for neighbor in cell.neighbors if neighbor.id != block.id}
            block.neighbors = list(shared)

    def load_colors(self):
        max_neighbors = max(len(block.neighbors) for block in self.state)
        num_colors = max_neighbors + 1; num_encodings = num_colors + 2
        COLORS[:] = COLORS[:num_colors]
        HIDDEN.encoding, NC.encoding = encode(k=1, n=num_encodings), encode(k=2, n=num_encodings)
        for i, color in enumerate(COLORS, start=3):
            color.encoding = encode(k=i, n=num_encodings)
        self.reset()
    
    def load_space(self):
        for counter, (block, color) in enumerate(product(self.state, COLORS)):
            action = Action(block, color)
            action.id = counter
            self.space.append(action)

    def reset(self):
        [block.set_color(HIDDEN) for block in self.state]

    def step(self):
        reveal = random.randint(self.minR, self.maxR)
        hidden_blocks = [block for block in self.state if block.is_hidden()]
        r = min(len(hidden_blocks), reveal)
        for block in random.sample(hidden_blocks, r):
            block.set_color(NC)
    
    def apply(self, actions):
        distinct = actions.former != actions.latter
        [action.set_invalid() for action in actions]

        actions_list = list(actions)
        random.shuffle(actions_list)
        applied = False

        for action in actions_list:
            if not bool(action.invalid):
                if distinct:
                    applied = action.apply()
                elif applied:
                    action.applied = False
                    ##################################################################################################################
                    #print(actions.former.applied, actions.former.block.id, actions.former.block.color.name, actions.former.color.name)
                    #print(actions.latter.applied, actions.latter.block.id, actions.latter.block.color.name, actions.latter.color.name)
                    ##################################################################################################################
                else:
                    applied = action.apply()
    """
    def reward(self, player):
        k, m = 0, 0
        for id in player.action.block.neighbors:
            neighbor = self.state[id]
            k, m = (k + 1, m) if neighbor.color != player.action.color else (k, m + 1)
        s = player.action.invalid * player.sanction
        g = k * player.gain
        p = m * player.penalty
        
        ###################################################
        #print(player.gain, player.penalty, player.sanction)
        ###################################################

        player.reward = s + g + p

        ###########################################################################################################
        #print(player.reward, bool(player.action.invalid), player.action.color.name, player.action.block.color.name)
        ###########################################################################################################
    """

    def reward(self, player):
        player.reward = player.sanction if bool(player.action.invalid) else player.gain

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.id = None
        self.color = HIDDEN
        self.neighbors = []  # the initial 4 instances of class Cell

    def set_color(self, color):
        self.color = color

    def is_valid(self, rows, cols):
        return 0 <= self.row < rows and 0 <= self.col < cols
    
    def is_hidden(self):
        return isinstance(self.color, Hidden)
    
    def is_uncolored(self):
        return isinstance(self.color, White)

class Block:
    def __init__(self, id):
        self.id = id
        self.color = HIDDEN
        self.cells = []
        self.neighbors = []  # ids after merging cells

    def set_color(self, color):
        self.color = color
        [cell.set_color(color) for cell in self.cells]

    def is_hidden(self):
        return isinstance(self.color, Hidden)
    
    def is_uncolored(self):
        return isinstance(self.color, White)
    
class Action:
    def __init__(self, block, color):
        self.block = block
        self.color = color
        self.id = None
        self.counter = {"explore": 0, "exploit": 0}
        self.invalid = 0  # 0 means false 1 means true
        self.applied = False

    def set_invalid(self):
        self.invalid = int(not self.block.is_uncolored())

    def increment(self, phase):
        self.counter[phase] += 1

    def apply(self):
        self.block.set_color(self.color)
        self.applied = True
        return self.applied

    def __eq__(self, other):
        return isinstance(other, Action) and self.block == other.block
    
    def __ne__(self, other):
        return not self.__eq__(other)