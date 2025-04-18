"""
GUI-модуль для сравнения различных методов интерполяции.

Позволяет пользователю выбрать функцию, способ размещения узлов, 
количество узлов и интерполяционные методы, после чего визуализирует 
результаты интерполяции и ошибки в графическом окне.

Поддерживаемые методы:
- Интерполяция Лагранжа
- Интерполяция Ньютона
- Кубическая сплайн-интерполяция

Зависимости:
- tkinter: для построения GUI
- matplotlib: для визуализации
- numpy: для численных вычислений
- functions, nodes, interpolation, calculate_error: локальные модули проекта
"""

import tkinter as tk
from tkinter import ttk
from itertools import cycle
import matplotlib.pyplot as plt
import numpy as np

from functions import *            # Получение аналитических функций
from nodes import *               # Генерация узлов интерполяции
from interpolation import *       # Методы интерполяции
from calculate_error import *     # Оценка ошибок интерполяции

def run_gui():
    """
    Запускает графический интерфейс для сравнения методов интерполяции.

    Пользователь может:
        - выбрать функцию для интерполяции;
        - задать количество узлов и их распределение;
        - выбрать один или несколько методов интерполяции;
        - построить график функции и результатов интерполяции;
        - просмотреть ошибки интерполяции (максимальную и MSE).
    """

    def run_comparison():
        """
        Выполняет сравнение выбранных методов интерполяции:
            - строит графики функции и интерполяционных полиномов;
            - выводит графики ошибок;
            - сохраняет график в ./img/plot.png;
            - печатает значения ошибок в консоль.
        """
        f = get_function(function_var.get())  # Получаем аналитическую функцию
        a, b = -1, 1                           # Интервал интерполяции
        n = int(entry_nodes.get())            # Количество узлов

        x_nodes = generate_nodes(a, b, n, nodes_var.get())
        y_nodes = f(x_nodes)
        x_plot = np.linspace(a, b, 1000)

        # Словарь доступных методов интерполяции
        methods = {
            "Лагранж": lagrange_interpolation,
            "Ньютон": newton_interpolation,
            "Кубический сплайн": cubic_spline_interpolation
        }

        colors = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])

        # Создание графиков
        plt.figure(figsize=(12, 6))

        # График функции и интерполяции
        plt.subplot(1, 2, 1)
        plt.plot(x_plot, f(x_plot), label="f(x)", linewidth=2)

        # График ошибок
        plt.subplot(1, 2, 2)
        errors = {}

        for name, var in method_vars.items():
            if var.get():
                p = methods[name](x_nodes, y_nodes)
                color = next(colors)

                # Интерполяционная кривая
                plt.subplot(1, 2, 1)
                plt.plot(x_plot, p(x_plot), '--', label=name, color=color)

                # Ошибка
                plt.subplot(1, 2, 2)
                plt.plot(x_plot, np.abs(f(x_plot) - p(x_plot)), label=name, color=color)

                # Расчёт ошибок
                max_err = calculate_max_error(f, p, x_plot)
                mse = calculate_mse(f, p, x_plot)
                errors[name] = (max_err, mse)

        # Оформление графиков
        plt.subplot(1, 2, 1)
        plt.title("Интерполяция функции")
        plt.legend()
        plt.grid()

        plt.subplot(1, 2, 2)
        plt.title("Ошибки интерполяции")
        plt.legend()
        plt.grid()

        plt.tight_layout()
        plt.savefig('./img/plot.png')  # Сохранение в файл

        # Вывод ошибок
        print("\n📊 Сравнение ошибок:")
        for method, (max_err, mse) in errors.items():
            print(f"{method}: Max Error = {max_err:.4e}, MSE = {mse:.4e}")

    # --- GUI-интерфейс ---
    root = tk.Tk()
    root.title("Сравнение методов интерполяции")

    # Выбор функции
    ttk.Label(root, text="Функция:").grid(row=0, column=0)
    global function_var
    function_var = tk.StringVar(value="sin(x)")
    ttk.Combobox(root, textvariable=function_var, values=[
        "sin(x)", "1 / (1 + 25x^2)", "|x|", "exp(x)"]).grid(row=0, column=1)

    # Выбор типа узлов
    ttk.Label(root, text="Узлы:").grid(row=1, column=0)
    global nodes_var
    nodes_var = tk.StringVar(value="Равномерные")
    ttk.Combobox(root, textvariable=nodes_var, values=[
        "Равномерные", "Чебышёвские"]).grid(row=1, column=1)

    # Количество узлов
    ttk.Label(root, text="Кол-во узлов:").grid(row=2, column=0)
    global entry_nodes
    entry_nodes = ttk.Entry(root)
    entry_nodes.insert(0, "10")
    entry_nodes.grid(row=2, column=1)

    # Методы интерполяции
    ttk.Label(root, text="Методы:").grid(row=3, column=0)
    global method_vars
    method_vars = {
        "Лагранж": tk.BooleanVar(value=True),
        "Ньютон": tk.BooleanVar(value=True),
        "Кубический сплайн": tk.BooleanVar(value=True),
    }
    for i, (name, var) in enumerate(method_vars.items()):
        ttk.Checkbutton(root, text=name, variable=var).grid(row=3 + i, column=1, sticky="w")

    # Кнопка запуска сравнения
    ttk.Button(root, text="Сравнить", command=run_comparison).grid(row=6, column=0, columnspan=2, pady=10)

    root.mainloop()
