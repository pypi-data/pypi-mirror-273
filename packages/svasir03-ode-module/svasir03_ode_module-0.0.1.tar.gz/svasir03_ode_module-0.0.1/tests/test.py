import numpy as np
import matplotlib.pyplot as plt
import ode

#Params
TIME_SPAN = (0, 9.9)
INITIAL_VALUE = np.array([np.pi / 4, 0])
omega = 2*np.pi
omega_0 = 3*np.pi
gamma = 0.1
NUM_OF_STEPS = 10000

#ODE func
def ODE_func(time,value, a, b, c):
    angle_vel= value[1]
    angle_acc = c * (b**2)*np.cos(a*time) -(b**2)*value[0]
    
    return np.array([angle_vel, angle_acc])

def ode_func(time, value):
    angle_vel= value[1]
    angle_acc = -np.sin(value[0])
    
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

times_RK1, values_RK1 = ode.solve_RK1(ode_func, TIME_SPAN, NUM_OF_STEPS, INITIAL_VALUE)

plt.plot(times_RK1, values_RK1[0])

plt.show()