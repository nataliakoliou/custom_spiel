import random
import torch.optim as optim
from itertools import chain
from collections import defaultdict
from settings import *
from utils import *

class Game:
    def __init__(self):
        self.env = Grid()
        self.colors = []
        self.human = Human()
        self.robot = Robot()

    def initialize(self):
        self.env.initialize()
        self.define_colors()

        """ self.env.display()
        self.display_colors()
        self.env.grid[2][2].display_neighbors()
        self.env.display_hidden_cells()
        self.env.display_blocks() """
    
    def define_colors(self):
        max_neighbors = get_max(len(cell.neighbors) for cell in chain.from_iterable(self.env.grid))
        num_colors = max_neighbors + 1
        self.colors = COLORS[:num_colors] + [None]

    def display_colors(self):
        print("Number of colors:", get_size(self.colors))
        print("Colors:", self.colors)

""" class MetaGame(Game):
    def __init__(self):
        super().__init__()

    def get_utilities(self):
        utilities = None
        return utilities """

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.id = None
        self.colour = WHITE  # white indicates that it's not coloured yet
        self.hidden = False
        self.neighbors = []

    def display_neighbors(self):
        print(f"Neighbors of cell ({self.row}, {self.col}) with id {self.id}: {','.join(str(neighbor.id) for neighbor in self.neighbors)}.")

class Grid:
    def __init__(self):
        self.rows = ROWS
        self.cols = COLUMNS
        self.merge = MERGE
        self.hide = HIDE
        self.grid = [[Cell(i, j) for j in range(self.cols)] for i in range(self.rows)]
        self.blocks = defaultdict(list)
        self.total = -1

    def initialize(self):
        self.set_ids()
        self.set_blocks()
        self.set_neighbors()
        self.hide_cells()

    def set_ids(self):
        for i, j in product(range(self.rows), range(self.cols)):
            cell = self.grid[i][j]
            cell.neighbors = [self.grid[i + dr][j + dc] for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]
                                    if self.is_valid(i + dr, j + dc)]
            ids = [neighbor.id for neighbor in cell.neighbors if neighbor.id is not None]
            if random.random() < self.merge and ids:
                cell.id = random.choice(ids)
            else:
                self.total += 1
                cell.id = self.total

    def set_blocks(self):
        for cell in chain.from_iterable(self.grid):
            self.blocks[cell.id].append(cell)

    def set_neighbors(self):
        for id, cells in self.blocks.items():
            shared = set()
            for cell in cells:
                shared |= {neighbor for neighbor in cell.neighbors if neighbor.id != id}
            for cell in cells:
                cell.neighbors = list(shared)

    def hide_cells(self):
        for cells in self.blocks.values():
            if random.random() < self.hide:
                for c in cells:
                    c.hidden = True

    def is_valid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def define_colors(self):
        max_neighbors = get_max(len(cell.neighbors) for cell in chain.from_iterable(self.grid))
        num_colors = max_neighbors + 1
        self.colors = COLORS[:num_colors]
    
    def display(self):
        for row in self.grid:
            print('\t'.join(str(cell.id) for cell in row))

    def display_hidden_cells(self):
        hidden_found = False
        for cell in chain.from_iterable(self.grid):
            if cell.hidden:
                print(f"Hidden cells: ({cell.row}, {cell.col}) with ID: {cell.id}")
                hidden_found = True
        if not hidden_found:
            print("Hidden cells: None")

    def display_blocks(self):
        print("Number of blocks:", get_size(self.blocks))

class Player:
    def __init__(self, type):
        self.type = type
        self.model = None
        self.optimizer = None

class Human(Player):
    def __init__(self):
        super().__init__('human')
        self.model = ...
        self.optimizer = optim.AdamW(self.model.parameters(), **HUMAN_PARAMETERS)

class Robot(Player):
    def __init__(self):
        super().__init__('robot')
        self.model = ...
        self.optimizer = optim.AdamW(self.model.parameters(), **ROBOT_PARAMETERS)