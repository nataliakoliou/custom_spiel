from game import *
from settings import *
#from simulator import *

# SETUP ##################################################################################################
game = Game()
game.run()

# EXPLORE + EXPLOIT (QLEARNING) ##########################################################################
#game.run()

# SIMULATE ###############################################################################################
"""
grid = Grid()
game = Game(grid)
grid.playing = True
#TODO: game.show_start_screen()
game.new()
game.run()
#TODO: game.show_go_screen()
"""

# EVALUATE ###############################################################################################

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