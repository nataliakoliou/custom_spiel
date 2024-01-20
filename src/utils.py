import random

def get_max(list):
    maximum = float('-inf')
    for element in list:
        if element > maximum:
            maximum = element
    return maximum

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