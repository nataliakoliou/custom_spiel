from torch.nn import SmoothL1Loss
from collections import namedtuple

DIR = '/content/drive/MyDrive/Repositories/custom_spiel'
ACCURACY = 4

@property  
def TUPLE(type): return namedtuple(type, ["h", "r"])

AGENTS = [("giant", "robot", "genius", "gg"), ("tiny", "human", "dump", "td")]
PAIRS = [("huge", TUPLE("type")("human", "robot"), TUPLE("intels")("dump", "genius"), "hdg"),
         ("giant", TUPLE("type")("wise", "smart"), TUPLE("intels")("basic", "genius"), "gbg")]

@property
def ENVIRONMENT():
    return {
        "tiny": {'rows': 2, 'cols': 2, 'merge': 0.2, 'minR': 2, 'wR': 0.2},
        "small": {'rows': 3, 'cols': 3, 'merge': 0.2, 'minR': 2, 'wR': 0.2},
        "average": {'rows': 4, 'cols': 4, 'merge': 0.3, 'minR': 2, 'wR': 0.2},
        "big": {'rows': 5, 'cols': 5, 'merge': 0.3, 'minR': 2, 'wR': 0.2},
        "large": {'rows': 6, 'cols': 6, 'merge': 0.3, 'minR': 2, 'wR': 0.2},
        "huge": {'rows': 7, 'cols': 7, 'merge': 0.4, 'minR': 2, 'wR': 0.2},
        "giant": {'rows': 8, 'cols': 8, 'merge': 0.4, 'minR': 2, 'wR': 0.2}
    }

@property
def AGENT(type=None):
    return {
        "dump": {"type": type, "model": "DQN", "criterion": SmoothL1Loss(), "optimizer": "AdamW", "lr": 0.001, "tau": 0.005, "batch_size": 128, "gamma": 0, "weight_decay": 1e-5, "gain": +1, "penalty": -2, "sanction": -10},
        "basic": {"type": type, "model": "DQN", "criterion": SmoothL1Loss(), "optimizer": "AdamW", "lr": 0.001, "tau": 0.005, "batch_size": 128, "gamma": 0, "weight_decay": 1e-5, "gain": +1, "penalty": -2, "sanction": -10},
        "moderate": {"type": type, "model": "DQN", "criterion": SmoothL1Loss(), "optimizer": "AdamW", "lr": 0.001, "tau": 0.005, "batch_size": 128, "gamma": 0, "weight_decay": 1e-5, "gain": +1, "penalty": -2, "sanction": -10},
        "advanced": {"type": type, "model": "DQN", "criterion": SmoothL1Loss(), "optimizer": "AdamW", "lr": 0.001, "tau": 0.005, "batch_size": 128, "gamma": 0, "weight_decay": 1e-5, "gain": +1, "penalty": -2, "sanction": -10},
        "smart": {"type": type, "model": "DQN", "criterion": SmoothL1Loss(), "optimizer": "AdamW", "lr": 0.001, "tau": 0.005, "batch_size": 128, "gamma": 0, "weight_decay": 1e-5, "gain": +1, "penalty": -2, "sanction": -10},
        "wise": {"type": type, "model": "DQN", "criterion": SmoothL1Loss(), "optimizer": "AdamW", "lr": 0.001, "tau": 0.005, "batch_size": 128, "gamma": 0, "weight_decay": 1e-5, "gain": +1, "penalty": -2, "sanction": -10},
        "genius": {"type": type, "model": "DQN", "criterion": SmoothL1Loss(), "optimizer": "AdamW", "lr": 0.001, "tau": 0.005, "batch_size": 128, "gamma": 0, "weight_decay": 1e-5, "gain": +1, "penalty": -2, "sanction": -10}
        }

@property
def LEARNER(env=None, agent=None):
    return {
        "td": {"name": "td", "env": env, "agent": agent, "repeats": 500, "epsilon": 1, "cutoff": 0.9},
        "gg": {"name": "gg", "env": env, "agent": agent, "repeats": 500, "epsilon": 1, "cutoff": 0.9},
        # add more ....
        }