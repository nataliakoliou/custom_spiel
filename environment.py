class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.id = None
        self.neighbors = []

class Grid:
    def __init__(self, rows=7, columns=6):
        self.rows = rows
        self.columns = columns
        self.grid = [[Cell(i, j) for j in range(columns)] for i in range(rows)]
        self.initialize()

    def is_valid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.columns

    def initialize(self):
        for i in range(self.rows):
            for j in range(self.columns):
                cell = self.grid[i][j]
                cell.row, cell.col, cell.id = i, j, i * self.columns + j
                cell.neighbors = [self.grid[i + dr][j + dc] for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]
                                  if self.is_valid(i + dr, j + dc)]

    def display_grid(self):
        for row in self.grid:
            print('\t'.join(str(cell.id) for cell in row))

    def display_neighbors(self, row, column):
        cell = self.grid[row][column]
        print(f"Neighbors of cell {cell.id}: {','.join(str(neighbor.id) for neighbor in cell.neighbors)}.")