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
        self.prev_state = []
        self.total = 0  # number of blocks

    def configure(self):
        self.set_ids()
        self.set_blocks()
        self.set_neighbors()

    def set_ids(self):
        for i, j in product(range(ROWS), range(COLUMNS)):
            cell = self.grid[i][j]
            cell.neighbors = [self.grid[i + dr][j + dc] for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]
                              if Cell(i + dr, j + dc).is_valid()]
            ids = [neighbor.id for neighbor in cell.neighbors if neighbor.id is not None]
            if random.random() < MERGE and ids:
                cell.id = random.choice(ids)
            else:
                cell.id = self.total
                self.total += 1

    def set_blocks(self):
        self.blocks = [Block(id) for id in range(self.total)]
        for cell in chain.from_iterable(self.grid):
            self.blocks[cell.id].cells.append(cell)

    def set_neighbors(self):
        for block in self.blocks:
            shared = set()
            for cell in block.cells:
                shared |= {neighbor for neighbor in cell.neighbors if neighbor.id != block.id}
            block.neighbors = list(shared)

    def init_state(self):
        self.state = [block.color.id for block in self.blocks]

    def reset(self):
        for block in self.blocks:
            block.set_color(Hidden())
            self.state[block.id] = block.color.id

    """
    def hide_blocks(self):
        for block in self.blocks:
            if random.random() < HIDE:
                block.hidden = True
                for cell in block.cells:
                    cell.hidden = block.hidden
    """

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.id = None
        self.color = Hidden()
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
        self.color = Hidden()
        self.cells = []
        self.neighbors = []  # after merging cells

    def set_color(self, color):
        self.color = color
        [cell.set_color(color) for cell in self.cells]

    def is_hidden(self):
        return isinstance(self.color, Hidden)
    
    def is_uncolored(self):
        return isinstance(self.color, NC)