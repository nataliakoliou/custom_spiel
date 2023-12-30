from environment import *
from settings import *
from simulator import *

grid = Grid()

# EXPLORE + EXPLOIT (QLEARNING) ##########################################################################

# SIMULATE ###############################################################################################
game = Game(grid)
grid.playing = True
#TODO: game.show_start_screen()
game.new()
game.run()
#TODO: game.show_go_screen()

# EVALUATE ###############################################################################################

# HELP ###################################################################################################
"""
grid.display_grid()

grid.display_neighbors(0,0)
grid.display_neighbors(0,1)
grid.display_neighbors(0,2)
grid.display_neighbors(0,3)
grid.display_neighbors(0,4)
grid.display_neighbors(0,5)

grid.display_hidden_cells()
"""