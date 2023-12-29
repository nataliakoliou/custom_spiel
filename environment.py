import random
from collections import defaultdict

class Cell:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.id = None
        self.colour = "white"  # white indicates that it's not coloured yet
        self.hidden = False
        self.neighbors = []

class Grid:
    def __init__(self, rows=7, columns=6, merge=0.1, hide=0.2):
        self.rows = rows
        self.columns = columns
        self.merge = merge
        self.hide = hide
        self.grid = [[Cell(i, j) for j in range(columns)] for i in range(rows)]
        self.initialize()

    def initialize(self):
        counter = 0
        for i in range(self.rows):
            for j in range(self.columns):
                cell = self.grid[i][j]
                cell.neighbors = [self.grid[i + dr][j + dc] for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]
                                  if self.is_valid(i + dr, j + dc)]
                counter = self.assign_id(cell, counter)
        self.update_neighbors()
        self.hide_cells()

    def hide_cells(self):
        for row in self.grid:
            for cell in row:
                if random.random() < self.hide:
                    cell.hidden = True

    def is_valid(self, row, column):
        return 0 <= row < self.rows and 0 <= column < self.columns
    
    def assign_id(self, cell, counter):
        neighbors = [neighbor.id for neighbor in cell.neighbors if neighbor.id is not None]
        if random.random() < self.merge and neighbors:
            cell.id = random.choice(neighbors)
        else:
            cell.id = counter
            counter += 1
        return counter

    def update_neighbors(self):
        idsXcells = defaultdict(list)
        for row in self.grid:
            for cell in row:
                idsXcells[cell.id].append(cell)
        for id, cells in idsXcells.items():
            common_neighbors = []
            for cell in cells:
                for neighbor in cell.neighbors:
                    if neighbor.id != id and neighbor not in common_neighbors:
                        common_neighbors.append(neighbor)
            for cell in cells:
                cell.neighbors = list(set(common_neighbors))

    def display_grid(self):
        for row in self.grid:
            print('\t'.join(str(cell.id) for cell in row))

    def display_neighbors(self, row, column):
        cell = self.grid[row][column]
        print(f"Neighbors of cell ({cell.row}, {cell.column}) with id {cell.id}: {','.join(str(neighbor.id) for neighbor in cell.neighbors)}.")

    def display_hidden_cells(self):
        for row in self.grid:
            for cell in row:
                if cell.hidden:
                    print(f"Cell at ({cell.row}, {cell.column}) is hidden with ID: {cell.id}")