import torch.nn as nn
import numpy as np
import torch

class DQN(nn.Module):
    def __init__(self, in_channels, output):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(in_channels, 64)
        self.fc2 = nn.Linear(64, 128)             
        self.fc3 = nn.Linear(128, output)  # output_size = num_blocks * num_colors
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.embedding(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.softmax(x)
        x = self.qvalues(x)
        return x
    
    def embedding(self, state): # state: [[0,1,0,0,0], [0,0,1,0,0],...]
        state = np.array([[block.color.encoding for block in state]])
        state = torch.tensor(state, dtype=torch.float32) # (batch size, num_blocks, num_colors)
        state = state.unsqueeze(1) # (batch, 1, num_blocks, num_colors)
        return state
    
    def qvalues(self, output):
        output = output.view(-1)
        return output.tolist()

