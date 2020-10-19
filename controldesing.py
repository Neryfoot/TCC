import control as ctrl
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols

kd = 2
kp = 5.5
ki= 0.075
alpha = 0.1

C = ctrl.tf([2*alpha*kp*kd, kp*ki*kd*alpha, kp*ki], [kd*alpha, 1, 0])
Cd = ctrl.sample_system(C, 1, method='zoh')

# G = ctrl.tf(4, [1, 40])
# C = ctrl.tf([alpha*kp*ki*kd, (2*ki+1)*kp*kd*alpha, kp], [ki*kd*alpha, ki, 0])
# t = np.arange(0, 50, 0.01)
# t, step = ctrl.step_response(G, t)

# T = ctrl.feedback(C*G*10)
# t, step = ctrl.step_response(T, t)
# plt.plot(t, step, label='step response')
# plt.plot(ctrl.root_locus(G))
# plt.legend()
# plt.show()

# ctrl.sisotool(T)

# Gd = ctrl.sample_system(G, 0.001, method='zoh')
# Cd = ctrl.sample_system(C, 1, method='zoh')
# Cd
# Gd
