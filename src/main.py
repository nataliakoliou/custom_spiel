#################### TODO ####################
#  Get statistics for type/action combination
#  Simulation
#  Show colored grid during simulation
#  Do simulation from trained models
##############################################

from google.colab import drive
#from game import *
#from grid import *
#from player import *
#from meta import *
#from settings import *

drive.mount('/content/drive')

for agent in AGENTS:
    size, type, intel, name = agent
    env = Grid(**ENVIRONMENT[size])
    player = Player(**PLAYER(type)[intel])
    QLearner(**LEARNER(env, player)[name]).run()

"""for pair in PAIRS:
    size, types, intels, name = pair
    env = Grid(**ENVIRONMENT[size])
    human = Player(**AGENT(type.h)[intels.h])
    robot = Player(**AGENT(type.r)[intels.r])
    Simulator(env, human, robot)[name].run()"""

"""metagame = Metagame(
    payoffs = [v.game.payoff for v in versions],
    alpha=1e2,
    profiles=8
)
metagame.alpharank()"""