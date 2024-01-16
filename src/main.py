from game import *
from settings import *
#from model import *
#from simulator import *

# LEARNING ###############################################################################################
game = Game(h=1, r=1)
game.run()

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