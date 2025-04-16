import numpy as np

def generate_nodes(a, b, n, kind):
    if kind == "Равномерные":
        return np.linspace(a, b, n)
    elif kind == "Чебышёвские":
        i = np.arange(n)
        x = np.cos((2 * i + 1) / (2 * n) * np.pi)
        return 0.5 * (a + b) + 0.5 * (b - a) * x