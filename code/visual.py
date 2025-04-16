import tkinter as tk
from tkinter import ttk
from itertools import cycle
import matplotlib.pyplot as plt
from functions import *
from nodes import *
from interpolation import *
from calculate_error import *

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
