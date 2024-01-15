# Game Description
In our game, players interact with a grid containing 'b' blocks, where each block can be colored in one of 'c' colors. The objective is to reach a state with no conflicts, defined as neighboring blocks sharing the same color. The game involves two players—human and robot—simultaneously choosing colors for all blocks in each stage.

**Action**: (block,color)

**State:** [(block,color),(block,color),(), ...]

---
# Q-Learning ❌

## Challenge: Huge State Space
One major obstacle to implementing simple Q-learning agents in our game is the exponential growth of the state space. If you need to choose from c colors for each block b in the grid, then the total number of states (S) can be calculated as:

```python
S = c^b
```
where c represents the number of colors and b is the total number of blocks in the grid.

## Example
For instance, if there are 6 colors (c = 6) and 9 blocks (b = 9), the total number of state (S) is 10,077,696. This immense state space does not allow us to train standard Q-learning agents for our game.

# Standard DQN ❌

## Solution: Huge State Space
One solution to the huge state space problem is to use function approximation methods like Deep Q-Networks (DQN). DQN employs neural networks to approximate the Q-values for state-action pairs. It takes the state as input and outputs Q-values for each possible action. This significantly reduces the need to explicitly store values for every possible state-action pair in a tabular form.

## Example
**Input:** state

**Output:** [p1, p2, ...], a list of values that indicates how good each action from that state is

**Use:** for some state s, we use the nn once to output probabilities for all actions

## Challenge: Variable Action Space
In our game, the action space is dynamic due to the changing nature of each stage's rounds. In each round, the environment decides which blocks can be colored, leading to variations in the set of available actions. Standard DQN faces challenges when dealing with variable action spaces, as it typically assumes a fixed number of actions corresponding to the output nodes of the neural network.

# Conditional DQN ✔️

## Solution: Variable Action Space
To address the variable action space challenge, a Conditional Deep Q Network (CDQN) approach can be adopted. In CDQN, each action is treated as a condition and is included in the input of the neural network.

## Example
**Input:** (state, action)

**Output:** p, a value that indicates how good it is

**Use:** for some state s, we use the neural network multiple times
> We input into the neural network all possible (s, action) pairs. Since action = (available_block, color), these pairs are num_available_blocks * num_colors in total.