from torch.nn import SmoothL1Loss, MSELoss, L1Loss
from collections import namedtuple

DIR = '/content/drive/MyDrive/Repositories/custom_spiel'
ACCURACY = 4

def TUPLE(type): return namedtuple(type, ["h", "r"])

AGENTS = [("big", "human", "dump", "bd"), ("big", "robot", "genius", "bg")]

#TODO: FIX ERROR
"""PAIRS = [("huge", TUPLE("type")("human", "robot"), TUPLE("intels")("dump", "genius"), "hdg"),
         ("giant", TUPLE("type")("wise", "smart"), TUPLE("intels")("basic", "genius"), "gbg")]"""

ENVIRONMENT = {
    "tiny": {'rows': 2, 'cols': 2, 'merge': 0.2, 'minR': 2, 'wR': 0.2},
    "small": {'rows': 3, 'cols': 3, 'merge': 0.2, 'minR': 2, 'wR': 0.2},
    "average": {'rows': 4, 'cols': 4, 'merge': 0.3, 'minR': 2, 'wR': 0.2},
    "big": {'rows': 5, 'cols': 5, 'merge': 0.3, 'minR': 2, 'wR': 0.2},
    "large": {'rows': 6, 'cols': 6, 'merge': 0.3, 'minR': 2, 'wR': 0.2},
    "huge": {'rows': 7, 'cols': 7, 'merge': 0.4, 'minR': 2, 'wR': 0.2},
    "giant": {'rows': 8, 'cols': 8, 'merge': 0.4, 'minR': 2, 'wR': 0.2}
}

def PLAYER(type=None):
    return {
        "dump": {"type": type, "model": "LDQN", "criterion": MSELoss(), "optimizer": "SGD", "lr": 5e-3, "tau": 5e-1, "batch_size": 8, "gamma": 0, "weight_decay": 5e-3, "gain": +1, "penalty": -2, "sanction": -10},
        "naive": {"type": type, "model": "LDQN", "criterion": L1Loss(), "optimizer": "Adagrad", "lr": 4e-3, "tau": 1e-1, "batch_size": 16, "gamma": 0, "weight_decay": 1e-3, "gain": +1, "penalty": -2, "sanction": -10},
        "decent": {"type": type, "model": "MDQN", "criterion": SmoothL1Loss(beta=0.2), "optimizer": "Adadelta", "lr": 3e-3, "tau": 5e-2, "batch_size": 32, "gamma": 0, "weight_decay": 5e-4, "gain": +1, "penalty": -2, "sanction": -10},
        "smart": {"type": type, "model": "MDQN", "criterion": SmoothL1Loss(beta=0.5), "optimizer": "RMSprop", "lr": 2e-3, "tau": 1e-2, "batch_size": 64, "gamma": 0, "weight_decay": 1e-4, "gain": +1, "penalty": -2, "sanction": -10},
        "wise": {"type": type, "model": "HDQN", "criterion": SmoothL1Loss(beta=0.8), "optimizer": "Adam", "lr": 1e-3, "tau": 5e-3, "batch_size": 128, "gamma": 0, "weight_decay": 5e-5, "gain": +1, "penalty": -2, "sanction": -10},
        "genius": {"type": type, "model": "HDQN", "criterion": SmoothL1Loss(beta=1.0), "optimizer": "AdamW", "lr": 8e-4, "tau": 1e-3, "batch_size": 256, "gamma": 0, "weight_decay": 1e-5, "gain": +1, "penalty": -2, "sanction": -10}
        }

def LEARNER(env=None, player=None):
    return {
        "bd": {"name": "bd", "env": env, "player": player, "repeats": 100, "epsilon": 1, "cutoff": 0.9},
        "bg": {"name": "bg", "env": env, "player": player, "repeats": 500, "epsilon": 1, "cutoff": 0.9},
        # add more ....
        }