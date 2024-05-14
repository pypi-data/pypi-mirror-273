import numpy as np
import matplotlib.pyplot as plt
from ..src import ode

#Params
TIME_SPAN = (0, 9.9)
INITIAL_VALUE = np.array([0, 0])
omega = 2*np.pi
omega_0 = 3*np.pi
gamma = 0.1
NUM_OF_STEPS = 10000

#ODE func
def ODE_func(time,value, params):
    angle_vel= value[1]
    angle_acc = params[2] * (params[1]**2)*np.cos(params[0]*time) -(params[1]**2)*value[0]
    
    return np.array([angle_vel, angle_acc])


#analytic func
def analytic_func(time, omega, omega0, gamma):
    #case w==w0
    if omega == omega0:
        angle = gamma * omega0 * time * np.sin(omega0*time)/ 2
        
    #case w=/=w0
    else:
        a = gamma * (omega0**2) /((omega0**2)- (omega**2))
        angle = a * np.cos(omega*time) -a * np.cos(omega0*time)
        
    return angle

#times_RK4, values_RK4 = ode.solve_RK4(ODE_func, TIME_SPAN, NUM_OF_STEPS, INITIAL_VALUE, omega, omega_0, gamma)

#plt.plot(times_RK4, values_RK4[0])

#error = values_RK4[0][-1] - analytic_func(9.9, omega, omega_0, gamma)
#print(error)

times_RK1, values_RK1 = ode.solve_RK1(ODE_func, TIME_SPAN, NUM_OF_STEPS, INITIAL_VALUE, omega, omega_0, gamma)

plt.plot(times_RK1, values_RK1[0])


plt.show()