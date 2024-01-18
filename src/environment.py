import random
from itertools import product, chain
from collections import defaultdict
from colors import *
from utils import *
from settings import *

class Grid:
    def __init__(self):
        self.grid = [[Cell(i, j) for j in range(COLUMNS)] for i in range(ROWS)]
        self.blocks = []
        self.state = []

    def load(self):
        self.init_cells()
        self.init_blocks()
        self.init_colors()
        REVEAL.value = 9

    def init_cells(self):
        global BLOCKS
        for i, j in product(range(ROWS), range(COLUMNS)):
            cell = self.grid[i][j]
            cell.neighbors = [self.grid[i + dr][j + dc] for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]
                              if Cell(i + dr, j + dc).is_valid()]
            ids = [neighbor.id for neighbor in cell.neighbors if neighbor.id is not None]
            if random.random() < MERGE and ids:
                cell.id = random.choice(ids)
            else:
                cell.id = BLOCKS.value
                BLOCKS.value += 1

    def init_blocks(self):
        self.blocks = [Block(id) for id in range(BLOCKS.value)]
        for cell in chain.from_iterable(self.grid):
            self.blocks[cell.id].cells.append(cell)
        for block in self.blocks:
            shared = set()
            for cell in block.cells:
                shared |= {neighbor for neighbor in cell.neighbors if neighbor.id != block.id}
            block.neighbors = list(shared)

    def init_colors(self):
        global COLORS, HIDDEN, NC
        max_neighbors = get_max(len(cell.neighbors) for cell in chain.from_iterable(self.grid))
        num_colors = max_neighbors + 1; num_encodings = num_colors + 2
        COLORS[:] = COLORS[:num_colors]
        HIDDEN.encoding, NC.encoding = encode(k=1, n=num_encodings), encode(k=2, n=num_encodings)
        for i, color in enumerate(COLORS, start=3):
            color.encoding = encode(k=i, n=num_encodings)

    def init_state(self):
        self.state = [HIDDEN.encoding for _ in self.blocks]

    def reset(self):
        for block in self.blocks:
            block.set_color(HIDDEN)
            self.state[block.id] = block.color.encoding

    def step(self):
        global REVEAL
        REVEAL.value = random.randint(PLAYERS, int(PLAYERS + Wr * BLOCKS.value))
        hidden_blocks = [block for block in self.blocks if block.is_hidden()]
        r = min(len(hidden_blocks), REVEAL.value)
        for block in random.sample(hidden_blocks, r):
            block.set_color(NC)

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.id = None
        self.color = None
        self.neighbors = []  # before merging cells

    def set_color(self, color):
        self.color = color

    def is_valid(self):
        return 0 <= self.row < ROWS and 0 <= self.col < COLUMNS
    
    def is_hidden(self):
        return isinstance(self.color, NC)

class Block:
    def __init__(self, id):
        self.id = id
        self.color = None
        self.cells = []
        self.neighbors = []  # after merging cells

    def set_color(self, color):
        self.color = color
        [cell.set_color(color) for cell in self.cells]

    def is_hidden(self):
        return isinstance(self.color, Hidden)
    
    def is_uncolored(self):
        return isinstance(self.color, NC)