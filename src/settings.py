from utils import *
from colors import *

# MUTABLE OBJECTS (GLOBAL AMONG MODULES)
BLOCKS = Global(0)
REVEAL = Global(0)
COLORS = [Red(), Orange(), Yellow(), Green(), Blue(), Pink(), Violet(), Cyan(), Coral(), Teal()]
HIDDEN = Hidden()
NC = NC()

# IMMUTABLE OBJECTS
ACCURACY = 20

TITLE = "GAME:  Cooperative Graph Colouring Problem"
PLAYERS = 2
ROWS = 2
COLUMNS = 2
MERGE = 0.1
Wr = 0.2

REPEATS = 10
STAGES = 10 # TO-DELETE
STEPS = STAGES * ROWS * COLUMNS
GAMMA = 0.9
EPSILON = 1
EXPLORATION = int(0.9 * STEPS)
EXPLOITATION = STEPS - EXPLORATION
DECAY = 1/EXPLORATION
HUMAN_MODEL = "DQN"
ROBOT_MODEL = "DQN"
HUMAN_PARAMETERS = {'lr': 0.001, 'weight_decay': 1e-5}
ROBOT_PARAMETERS = {'lr': 0.001, 'weight_decay': 1e-5}

#########################################################################################
BGCOLOR = NC
FPS = 60
TILESIZE = 80
RADIUS = TILESIZE // 2
WIDTH = ROWS * TILESIZE
HEIGHT = COLUMNS * TILESIZE
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
CENTER = (TILESIZE//2, TILESIZE//2)