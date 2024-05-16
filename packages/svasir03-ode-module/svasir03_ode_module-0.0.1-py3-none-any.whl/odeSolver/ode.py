#Imports
import numpy as np


#RK1
def solve_RK1(ode_func, time_span, num_of_steps, initial_value, *args):
    times = np.linspace(time_span[0], time_span[1], num_of_steps + 1)
    values = np.zeros((len(times), len(initial_value)))
    values[0] = initial_value

    time_step = times[1] - times[0]

    def calc_next_value(time, value):
        next_value = value + time_step * ode_func(time, value, *args)
        return next_value

    for i in range(len(times) - 1):
        next_value = calc_next_value(times[i], values[i])
        values[i+1] = next_value

    values = np.transpose(values)
    return times, values

#RK4
def solve_RK4(ode_func, time_span, num_of_steps, initial_value, *args):
    times = np.linspace(time_span[0], time_span[1], num_of_steps + 1)
    values = np.zeros((len(times), len(initial_value)))
    values[0] = initial_value

    time_step = times[1] - times[0]

    def calc_next_value(time, value):
        k1 = ode_func(time, value, *args)
        k2 = ode_func(time + time_step / 2, value + k1 * time_step / 2, *args)
        k3 = ode_func(time + time_step / 2, value + k2 * time_step / 2, *args)
        k4 = ode_func(time + time_step, value + k3 * time_step, *args)

        next_value = value + time_step / 6 * (k1 + 2*k2 + 2*k3 + k4)
        return next_value

    for i in range(len(times) - 1):
        next_value = calc_next_value(times[i], values[i])
        values[i+1] = next_value

    values = np.transpose(values)
    return times, values