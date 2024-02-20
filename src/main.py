#################### TODO ####################
#  Fine-tune parameters
#  Early stopping
#  Get statistics for type/action combination
#  Simulation
#  Show colored grid during simulation
#  Do simulation from trained models
#  Optimize Code
##############################################

from google.colab import drive
import torch
import torch.nn as nn
#from game import *
#from grid import *
#from player import *
#from meta import *

drive.mount('/content/drive')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

env = Grid(
    rows=4,
    cols=4,
    merge=0.2,
    minR=2,
    wR=0.2
    )

"""human = Player(
    type="human",
    model="DQN",
    criterion = nn.SmoothL1Loss(),
    optimizer="AdamW",
    lr=0.0005,
    tau=0.001,
    batch_size=64,
    gamma=0,
    weight_decay=1e-4,
    gain=+1,
    penalty=-2,
    sanction=-10,
    device=device
    )"""

robot = Player(
    type="robot",
    model="DQN",
    criterion = nn.SmoothL1Loss(),
    optimizer="AdamW",
    lr=0.001,
    tau=0.005,
    batch_size=128,
    gamma=0,
    weight_decay=1e-5,
    gain=+1,
    penalty=-2,
    sanction=-10,
    device=device
    )

qlearning = QLearner(
    repeats=500,
    env=env,
    player=robot,
    epsilon=1,
    cutoff=0.9,
    accuracy=4,
    saves=5,
    color="blue".
    dir='/content/drive/MyDrive/Repositories/custom_spiel'
    )

qlearning.run()

"""metagame = Metagame(
    payoffs = [v.game.payoff for v in versions],
    alpha=1e2,
    profiles=8
)
metagame.alpharank()"""