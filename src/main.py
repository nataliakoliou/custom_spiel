from game import *
from settings import *
#from model import *
#from simulator import *

# SETUP ##################################################################################################
game = Game(h=1, r=1)
game.start()

# EXPLORE + EXPLOIT (QLEARNING) ##########################################################################
#model = QLearning()
#model.run(game)

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