import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from itertools import cycle

# --- Интерполяционные методы ---
def get_function(name):
    if name == "sin(x)":
        return np.sin
    elif name == "1 / (1 + 25x^2)":
        return lambda x: 1 / (1 + 25 * x**2)
    elif name == "|x|":
        return np.abs
    elif name == "exp(x)":
        return np.exp

def generate_nodes(a, b, n, kind):
    if kind == "Равномерные":
        return np.linspace(a, b, n)
    elif kind == "Чебышёвские":
        i = np.arange(n)
        x = np.cos((2 * i + 1) / (2 * n) * np.pi)
        return 0.5 * (a + b) + 0.5 * (b - a) * x

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

# --- Ошибки ---
def calculate_max_error(f, p, x):
    return np.max(np.abs(f(x) - p(x)))

def calculate_mse(f, p, x):
    return np.mean((f(x) - p(x))**2)

# --- GUI-функция ---
def run_comparison():
    f = get_function(function_var.get())
    a, b = -1, 1
    n = int(entry_nodes.get())
    x_nodes = generate_nodes(a, b, n, nodes_var.get())
    y_nodes = f(x_nodes)
    x_plot = np.linspace(a, b, 1000)

    methods = {
        "Лагранж": lagrange_interpolation,
        "Ньютон": newton_interpolation,
        "Кубический сплайн": cubic_spline_interpolation
    }

    colors = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(x_plot, f(x_plot), label="f(x)", linewidth=2)

    plt.subplot(1, 2, 2)
    errors = {}

    for name, var in method_vars.items():
        if var.get():
            p = methods[name](x_nodes, y_nodes)
            color = next(colors)

            # Интерполяция
            plt.subplot(1, 2, 1)
            plt.plot(x_plot, p(x_plot), '--', label=name, color=color)

            # Ошибка
            plt.subplot(1, 2, 2)
            plt.plot(x_plot, np.abs(f(x_plot) - p(x_plot)), label=name, color=color)

            # Метрики
            max_err = calculate_max_error(f, p, x_plot)
            mse = calculate_mse(f, p, x_plot)
            errors[name] = (max_err, mse)

    # Графики
    plt.subplot(1, 2, 1)
    plt.title("Интерполяция функции")
    plt.legend()
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.title("Ошибки интерполяции")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.savefig('/home/monkeyreel/study/2nd-year/plot.png')

    print("\n📊 Сравнение ошибок:")
    for method, (max_err, mse) in errors.items():
        print(f"{method}: Max Error = {max_err:.4e}, MSE = {mse:.4e}")

# --- GUI-интерфейс ---
root = tk.Tk()
root.title("Сравнение методов интерполяции")

ttk.Label(root, text="Функция:").grid(row=0, column=0)
function_var = tk.StringVar(value="sin(x)")
ttk.Combobox(root, textvariable=function_var, values=[
    "sin(x)", "1 / (1 + 25x^2)", "|x|", "exp(x)"]).grid(row=0, column=1)

ttk.Label(root, text="Узлы:").grid(row=1, column=0)
nodes_var = tk.StringVar(value="Равномерные")
ttk.Combobox(root, textvariable=nodes_var, values=[
    "Равномерные", "Чебышёвские"]).grid(row=1, column=1)

ttk.Label(root, text="Кол-во узлов:").grid(row=2, column=0)
entry_nodes = ttk.Entry(root)
entry_nodes.insert(0, "10")
entry_nodes.grid(row=2, column=1)

# Методики (Checkbutton)
ttk.Label(root, text="Методы:").grid(row=3, column=0)
method_vars = {
    "Лагранж": tk.BooleanVar(value=True),
    "Ньютон": tk.BooleanVar(value=True),
    "Кубический сплайн": tk.BooleanVar(value=True),
}
for i, (name, var) in enumerate(method_vars.items()):
    ttk.Checkbutton(root, text=name, variable=var).grid(row=3 + i, column=1, sticky="w")

ttk.Button(root, text="Сравнить", command=run_comparison).grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
