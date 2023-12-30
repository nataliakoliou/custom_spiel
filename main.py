from environment import *
from visualize import *

grid = Grid(rows=7, columns=6, merge=0.1, hide=0.2)

visualizer = Visualizer(grid, title="GAME:  Cooperative Graph Colouring Problem")

# display grid where cells=ids in terminal
"""
grid.display_grid()
"""

# display the neighbors of some cells
"""
grid.display_neighbors(0,0)
grid.display_neighbors(0,1)
grid.display_neighbors(0,2)
grid.display_neighbors(0,3)
grid.display_neighbors(0,4)
grid.display_neighbors(0,5)
"""

# display all the hidden cells
"""
grid.display_hidden_cells()
"""