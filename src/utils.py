from settings import *

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
    
def is_valid(row, col):
    return 0 <= row < ROWS and 0 <= col < COLUMNS