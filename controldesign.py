import control as ctrl
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols

kd = 2
kp = 5.5
ki= 0.075
alpha = 0.1

kd = 1
kp = 2.5
ki= 0.1
alpha = .1


C = ctrl.tf([2*alpha*kp*kd, (kp*ki*kd*alpha+1), kp*ki], [kd*alpha, 1, 0])
C = ctrl.tf([kd*kp+alpha*kp, (ki*alpha*kp + kp), kp*ki], [alpha, 1, 0])
C = ctrl.tf([kd*kp*alpha+kp*kd, (kp*kd*ki*alpha + kp), kp*ki], [alpha*kd, 1, 0])
C
Cd = ctrl.sample_system(C, 1, method='zoh')
Cd = ctrl.sample_system(C, 1/15, method='zoh')
Cd
G = ctrl.tf(0.638569, [300, 1])
Gd = ctrl.sample_system(G, 0.1, method='zoh')
Gd = ctrl.sample_system(G, 0.1, method='matched')
Gd
G = ctrl.tf(100/2, [1, 1/2])
Gd = ctrl.sample_system(G, 0.1, method='zoh')
Gd

# C = ctrl.tf([alpha*kp*ki*kd, (2*ki+1)*kp*kd*alpha, kp], [ki*kd*alpha, ki, 0])
t = np.arange(0, 50, 0.01)
t, step = ctrl.step_response(G, t)


# T = ctrl.feedback(C*G*10)
# t, step = ctrl.step_response(T, t)
plt.plot(t, step, label='step response')
# plt.plot(ctrl.root_locus(G))
# plt.legend()
plt.show()

# ctrl.sisotool(T)

# Gd = ctrl.sample_system(G, 0.001, method='zoh')
# Cd = ctrl.sample_system(C, 1, method='zoh')
# Cd
# Gd
