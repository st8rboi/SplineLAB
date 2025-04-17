import numpy as np

def get_function(name: str) -> callable:
    """
    Args:
        name: имя (название) функции, которую требуется интерполировать.
    Returns:
        Возвращает ссылку на функцию, которая была выбрана пользователем.
    Comment:
        Допустимые варианты (будут обновляться): sin(x), 1 / (1 + 25x^2), |x|, exp(x) 
    """
    match name:
        case "sin(x)": return np.sin
        case "1 / (1 + 25x^2)": return lambda x: 1 / (1 + 25 * x**2)
        case "|x|": return np.abs
        case "exp(x)": return np.exp
        case _: ...