import numpy as np

def generate_nodes(a: float, b: float, n: int, kind: str) -> list[float]:
    """
    Args:
        a: стартовая точка отрезка (включительно).
        b: конечная точка отрезка (включительно).
        n: количество узлов на отрезке.
        kind: вид узлов (разбиения) сетки.

    Returns:
        Возвращает массив от a до b с n узлами.
        
    Comment:
        Допустимые варианты (будут обновляться): Равномерные, Чебышёвсике.
    """
    match kind:
        case "Равномерные":
            return np.linspace(a, b, n)
        case "Чебышёвские":
            i = np.arange(n)
            x = np.cos((2 * i + 1) / (2 * n) * np.pi)
            return 0.5 * (a + b) + 0.5 * (b - a) * x
        case _:
            ...