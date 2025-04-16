import numpy as np

def calculate_max_error(f, p, x):
    return np.max(np.abs(f(x) - p(x)))

def calculate_mse(f, p, x):
    return np.mean((f(x) - p(x))**2)
