import numpy as np
from scipy.interpolate import CubicSpline

def lagrange_interpolation(x_nodes: float, y_nodes: float) -> list[float]:
    """
    Args:
        x_nodes: Узлы интерполяции по оси X.
        y_nodes: Значения функции в узлах интерполяции.
    
    Returns:
        Возвращает векторизованную функцию P(x), реализующую интерполяцию Лагранжа.
    
    Comment:
        Интерполяционный многочлен Лагранжа строится как линейная комбинация базисных полиномов L_k(x).
        Каждый базисный полином аннулируется в остальных узлах, кроме k-го.
    """
    def L(k, x):
        terms = [(x - x_nodes[j]) / (x_nodes[k] - x_nodes[j]) for j in range(len(x_nodes)) if j != k]
        return np.prod(terms, axis=0)
    
    def P(x):
        return sum(y_nodes[k] * L(k, x) for k in range(len(x_nodes)))
    
    return np.vectorize(P)

def newton_interpolation(x_nodes: float, y_nodes: float) -> list[float]:
    """
    Args:
        x_nodes: Узлы интерполяции по оси X.
        y_nodes: Значения функции в узлах интерполяции.
    
    Returns:
        Возвращает векторизованную функцию P(x), реализующую интерполяцию Ньютона.
    
    Comment:
        Интерполяция осуществляется с использованием разделённых разностей и формулы Ньютона.
        Коэффициенты полинома находятся рекурсивно, начиная с нулевой разделённой разности.
    """
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

def cubic_spline_interpolation(x_nodes: float, y_nodes: float) -> list[float]:
    """
    Args:
        x_nodes: Узлы интерполяции по оси X.
        y_nodes: Значения функции в узлах интерполяции.
    
    Returns:
        Возвращает объект, представляющий кусочно-гладкую функцию кубического сплайна cs(x).
    
    Comment:
        Кубическая сплайн-интерполяция строит гладкую функцию, которая проходит через все узлы,
        с непрерывными первыми и вторыми производными. Используется библиотека SciPy.
    """
    cs = CubicSpline(x_nodes, y_nodes)
    return cs  # cs(x) можно вызывать как обычную функцию
