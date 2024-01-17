import random
from itertools import product, chain
from collections import defaultdict
from colors import *
from utils import *
from settings import *

class Grid:
    def __init__(self):
        self.grid = [[Cell(i, j) for j in range(COLUMNS)] for i in range(ROWS)]
        self.blocks = defaultdict(list)
        self.total = -1

    def configure(self):
        self.set_ids()
        self.set_blocks()
        self.set_neighbors()
        self.hide_cells()

    def set_ids(self):
        for i, j in product(range(ROWS), range(COLUMNS)):
            cell = self.grid[i][j]
            cell.neighbors = [self.grid[i + dr][j + dc] for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]
                                    if self.is_valid(i + dr, j + dc)]
            ids = [neighbor.id for neighbor in cell.neighbors if neighbor.id is not None]
            if random.random() < MERGE and ids:
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
            if random.random() < HIDE:
                for c in cells:
                    c.hidden = True

    def is_valid(self, row, col):
        return 0 <= row < ROWS and 0 <= col < COLUMNS
    
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

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.id = None
        self.color = NC()
        self.hidden = False
        self.neighbors = []

    def display_neighbors(self):
        print(f"Neighbors of cell ({self.row}, {self.col}) with id {self.id}: {','.join(str(neighbor.id) for neighbor in self.neighbors)}.")