def get_max(list):
    maximum = float('-inf')
    for element in list:
        if element > maximum:
            maximum = element
    return maximum