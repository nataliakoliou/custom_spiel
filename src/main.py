import torch.nn as nn

from game import *
from grid import *
from player import *

########## TODO ##########
# 1) Replay Memory
# 2) Batch Size
# 3) Simulation
# 4) Model Architecture
# 5) Colors Representation
# 6) Code Structure
# 7) Testers
##########################

env = Grid(
    rows=2, 
    cols=2, 
    merge=0.2,
    minR=2,
    wR=0.2
    )

human = Player(
    type="human",
    model="DQN",
    criterion = nn.MSELoss(),
    optimizer="AdamW",
    lr=0.001,
    weight_decay=1e-5,
    bG=+1,
    bP=-1,
    wS=-3
    )

robot = Player(
    type="robot",
    model="DQN",
    criterion = nn.SmoothL1Loss(),
    optimizer="AdamW",
    lr=0.001,
    weight_decay=1e-5,
    bG=+1,
    bP=-1,
    wS=-3
    )

game = Game(
    title="CGCP.1: Human-Robot",
    repeats=10,
    env=env,
    human=human,
    robot=robot,
    gamma=0.9,
    epsilon=1,
    accuracy=4,
    dir=r"C:\Users\natalia\git-repos\custom_spiel"
    )

game.load()


"""game.learn(dir=.../models/game1)
#train human and robot models

game.simulate(dir=.../models/game1) 
#dir is the local directory where we store human and robot's trained models

meta_game.evaluate(algorithm="alpha-rank", dir=.../simulations)
#dir is the local directory where we store the simulations payoff tables"""


"""
#NOTE: DISPLAYS ENVIRONMENT
for row in game.env.grid:
    print('\t'.join(str(cell.id) for cell in row))
"""
    
"""
#NOTE: DISPLAYS COLORS
print("Number of colors:", get_size(COLORS))
print("Colors:", [color.__class__.__name__ for color in COLORS])
"""

"""
#NOTE: DISPLAYS CELL'S NEIGHBORS
cell = game.env.grid[0][0]
print(f"Neighbors of cell ({cell.row}, {cell.col}) with id {cell.id}: {','.join(str(neighbor.id) for neighbor in cell.neighbors)}.")
"""

"""
#NOTE: DISPLAYS BLOCK'S NEIGHBORS
block = game.env.blocks[0]
print(f"Neighbors of block with id {block.id}: {','.join(str(neighbor.id) for neighbor in block.neighbors)}.")
"""

"""
#NOTE: DISPLAYS BLOCKS
print("Number of blocks:", BLOCKS.value)
"""

# VISUALIZE ###############################################################################################
"""
grid = Grid()
game = Game(grid)
grid.playing = True
#TODO: game.show_start_screen()
game.new()
game.run()
#TODO: game.show_go_screen()
"""

# EVALUATION ##############################################################################################

""" # Construct meta-game payoff tables
payoffs = game.meta.get_utilities()
hpt = utils.check_payoffs_are_hpt(payoffs)  # hpt = False
strat_labels = utils.get_strat_profile_labels(payoffs, hpt)

# Run AlphaRank
rhos, rho_m, pi, _, _ = alpharank.compute(payoffs, alpha=1e2)

# Report & plot results
alpharank.print_results(payoffs, hpt, rhos=rhos, rho_m=rho_m, pi=pi)
utils.print_rankings_table(payoffs, pi, strat_labels)
m_network_plotter = alpharank_visualizer.NetworkPlot(payoffs, rhos, rho_m, pi, strat_labels, num_top_profiles=8)
m_network_plotter.compute_and_draw_network() """

# VISUALIZATION ##########################################################################################

"""
import pygame as pg
import sys
from settings import *

class Game:
    def __init__(self, grid):
        self.grid = grid
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)

    def run(self):
        while self.grid.playing:  # stops when reaching equilibrium
            self.events()
            self.update()

    def quit(self):
        pg.quit()
        sys.exit()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_players(self):
        pg.draw.circle(self.image, RED, CENTER, RADIUS)
   

    # applies all changes in the env (cell colours & agents positions)
    def update(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        #TODO LATER: self.draw_players()
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:  # case: click the X button on the window
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    TODO:
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
    
"""