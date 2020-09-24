import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

kd = 0
kp = .1
ki = 10

G = ctrl.tf(4, [1, 40])
C = ctrl.tf([kd, kp, ki], [1, 0])
t = np.arange(0, 50, 0.01)
t, step = ctrl.step_response(G, t)

T = ctrl.feedback(C*G*10)
t, step = ctrl.step_response(T, t)
plt.plot(t, step, label='step response')
plt.plot(ctrl.root_locus(G))
plt.legend()
plt.show()

ctrl.sisotool(T)

Gd = ctrl.sample_system(G, 0.001, method='zoh')
Cd = ctrl.sample_system(C, 0.1, method='zoh')
Cd
Gd
