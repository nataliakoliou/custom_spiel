# NOTE.1 | TWO POPULATIONS (ONE FOR EACH PLAYER) WITH STRATEGIES a.k.a. AGENTS = QLEARNING AGENTS
"""
If you need to choose from c colors for each block in the grid, then the total number of combinations C can be
calculated as:

A = c ^ b, where c represents the number of colors and b is the  total number of blocks in the grid.

a represents the total number of actions "paint(grid, color)" a player can choose. Given that we have 2 players,
the total number of strategy profiles (action[player-1], action[player-2]) is: S = (c ^ b) ^ p = c ^(b * p), where
p is the number of players.

If for example c = 6, b = 9 and p = 2:
A = c ^ b = 6 ^ 9 = 10,077,696
P = A ^ p = A ^ 2 = 10,077,696 ^ 2 = 1.0155996e+14
"""

# NOTE.2 | TWO POPULATIONS (ONE FOR EACH PLAYER) WITH STRATEGIES a.k.a. AGENTS = DQN AGENTS
"""
Unlike Q-learning, where storing Q-values becomes impractical for large state-action spaces, DQN agents use
neural networks to approximate Q-values. This allows them to handle vast strategy profiles efficiently.
"""