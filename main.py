import midi_generator
import plotter
from sympy import *
import math

if __name__ == "__main__":
    t = Symbol("theta")
    a = Symbol("a")
    x, y = Symbol("x"), Symbol("y")
    x_t = sympify("cos(theta)")
    y_t = sympify("sin(4*theta)")
    t_range = [0,2*math.pi]
    fun = sympify("x^2")
    
    kick = midi_generator.get_intersection(y_t,x_t,36,t_range=t_range)
    snare = midi_generator.get_intersection(x_t,y_t,37,t_range=t_range)
    hat = midi_generator.intersection_with_function(x_t,y_t,fun,42,t_range=t_range)
    hat2 = midi_generator.intersection_with_function(x_t,y_t,sympify("1"),53,t_range=t_range)
    plotter.plot_functions(x_t,y_t,t_range,fun,sympify("1"))
    midi_generator.intersections_to_midi(120,"fakka",kick,snare,hat,hat2)
