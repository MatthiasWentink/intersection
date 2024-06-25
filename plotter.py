import matplotlib.pyplot as plt
from sympy import *
import numpy as np

def plot_functions(x_t,y_t,t_range,*fun):
    # Convert the parametric equations to numpy functions for plotting
    x_func = lambdify(Symbol('theta'), x_t, modules=['numpy'])
    y_func = lambdify(Symbol('theta'), y_t, modules=['numpy'])

    # Generate values for t
    t_values = np.linspace(t_range.min, t_range.max, 400)

    # Calculate the corresponding x and y values for the parametric plot
    x_values = x_func(t_values)
    y_values = y_func(t_values)

    # Create the plot
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values)
    for func in fun:
        x_explicit_values = np.linspace(-1.5, 1.5)
        if func.is_number:
            plt.plot(x_explicit_values, [func] * len(x_explicit_values), linestyle='--')
        else:
            y_explicit_func = lambdify(Symbol('x'), func, modules=['numpy'])
            
            y_explicit_values = y_explicit_func(x_explicit_values)
            plt.plot(x_explicit_values, y_explicit_values, linestyle='--')

    # Add labels and legend
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Plot of Parametric Equation and Explicit Equation')
    plt.grid(True)
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.show()