import os
import random

def get_size(struct):
    if isinstance(struct, (dict, list, tuple, set)):
        return len(struct)
    else:
        raise ValueError("Unsupported structure type")
    
def encode(k, n):
    if k > n:
        raise ValueError("k should be less than or equal to n")
    encoding = [0 for _ in range(n)]
    encoding[k - 1] = 1
    return encoding

def get_id(list, value):
    ids = [i for i, x in enumerate(list) if x == value]
    return random.choice(ids) if ids else None

def get_path(dir, folder, name):
    folder = folder if isinstance(folder, tuple) else (folder,)
    save_dir = os.path.join(dir, *folder)
    os.makedirs(save_dir, exist_ok=True)
    return os.path.join(save_dir, name)

def get_color(type):
    if type == "robot":
        return "blue"
    elif type == "human":
        return "red"
    else:
        raise ValueError("Invalid type.")