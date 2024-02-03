import torch
import torch.nn as nn
from google.colab import drive
#from game import *
#from grid import *
#from player import *

drive.mount('/content/drive')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

############# TODO #############
#  Fine-tune parameters
#  Get statistics for type/action combination
#  Simulation
#  Show colored grid during simulation
#  Continue training from trained models
#  Optimize Code
################################

env = Grid(
    rows=2, 
    cols=2, 
    merge=0.1,
    minR=2,
    wR=0.2
    )

human = Player(
    type="human",
    model="DQN1",
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

robot = Player(
    type="robot",
    model="DQN1",
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

game = Game(
    title="CGCP.1: Human-Robot",
    repeats=1000,
    env=env,
    human=human,
    robot=robot,
    epsilon=1,
    cutoff=0.9,
    accuracy=4,
    saves=5,
    dir='/content/drive/MyDrive/Repositories/custom_spiel'
    )

###############################################################################################
game.load()
game.qlearning()