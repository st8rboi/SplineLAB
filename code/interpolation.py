import numpy as np
from scipy.interpolate import CubicSpline

def lagrange_interpolation(x_nodes, y_nodes):
    def L(k, x):
        terms = [(x - x_nodes[j]) / (x_nodes[k] - x_nodes[j]) for j in range(len(x_nodes)) if j != k]
        return np.prod(terms, axis=0)
    def P(x):
        return sum(y_nodes[k] * L(k, x) for k in range(len(x_nodes)))
    return np.vectorize(P)

def newton_interpolation(x_nodes, y_nodes):
    n = len(x_nodes)
    coef = np.copy(y_nodes)
    for j in range(1, n):
        coef[j:] = (coef[j:] - coef[j - 1:-1]) / (x_nodes[j:] - x_nodes[:n - j])
    def P(x):
        result = coef[-1]
        for k in range(n - 2, -1, -1):
            result = result * (x - x_nodes[k]) + coef[k]
        return result
    return np.vectorize(P)

def cubic_spline_interpolation(x_nodes, y_nodes):
    cs = CubicSpline(x_nodes, y_nodes)
    return cs