import torch.nn as nn

# input: tensor([ [[0 1 0 0], ... , [0 0 1 0]], ..., [[0 1 0 0], ... , [0 0 1 0]] ]) --> (batch, num_blocks, num_all_colors)
# output: tensor([[2,1,...], [5,6,...], ...]) --> (batch, num_actions)

class DQN1(nn.Module):
    def __init__(self, input, output):
        super(DQN1, self).__init__()
        self.fc1 = nn.Linear(input, 64)
        self.fc2 = nn.Linear(64, 128)             
        self.fc3 = nn.Linear(128, output)
        self.relu = nn.LeakyReLU()

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
class DQN2(nn.Module):
    def __init__(self, input, output):
        super(DQN2, self).__init__()
        self.fc1 = nn.Linear(input, 128)
        self.fc2 = nn.Linear(128, 128)        
        self.fc3 = nn.Linear(128, output)  # output_size = num_blocks * num_colors
        self.relu = nn.LeakyReLU()

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
class DQN3(nn.Module):
    def __init__(self, input, output):
        super(DQN3, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(256*input, 512)
        self.fc2 = nn.Linear(512, output)
        self.relu = nn.LeakyReLU()
    
    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.relu(self.conv3(x))
        x = self.relu(self.conv4(x))
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x