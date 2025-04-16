import numpy as np

def get_function(name):
    if name == "sin(x)":
        return np.sin
    elif name == "1 / (1 + 25x^2)":
        return lambda x: 1 / (1 + 25 * x**2)
    elif name == "|x|":
        return np.abs
    elif name == "exp(x)":
        return np.exp