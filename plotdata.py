# import csv
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

SMALL_SIZE = 12
MEDIUM_SIZE = 18
BIGGER_SIZE = 20

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE) 

# with open('./ensaios/matlab/u1.csv', newline='') as csvfile:
#     data = list(csv.reader(csvfile))

u1 = pd.read_csv("./ensaios/matlab/u1.csv", delimiter=';', decimal=',')
y1 = pd.read_csv("./ensaios/matlab/y1.csv", delimiter=';', decimal=',')
mv=0
mv=np.loadtxt('./simulação/4tanks/MV1.txt')
pv=np.loadtxt('./simulação/4tanks/PV1.txt')
mv=mv[:2236]
pv=pv[:2236]
t= np.arange(len(mv))
t
u1 = u1.to_numpy()
y1 = y1.to_numpy()
t= u1[:,0]
t= y1[:,0]
mv=u1[:,1]
pv=y1[:,1]

for i in range(len(t)):
    if t[i] > 985:
        t[i] = t[i+1]

fig, ax = plt.subplots()

ax.plot(t/60, mv, color="green")
ax.set(xlabel='tempo (min)', ylabel='sinal de controle (mA)', title='Sinal de controle 1')
ax.grid()

fig.savefig("MV1.png")
plt.show()

fig, ax = plt.subplots()
ax.plot(t/60, pv)
ax.set(xlabel='tempo (min)', ylabel='nível do tanque (cm)', title='Nível do tanque 1')
ax.grid()

fig.savefig("PV1.png")
plt.show()


ax.plot(t/60, mv, color="green")
ax.set(xlabel='tempo (min)', ylabel='sinal de controle (mA)', title='Sinal de controle 2')
ax.grid()

fig.savefig("MV2.png")
plt.show()

fig, ax = plt.subplots()
ax.plot(t/60, pv)
ax.set(xlabel='tempo (min)', ylabel='nível do tanque (cm)', title='Nível do tanque 2')
ax.grid()

fig.savefig("PV2.png")
plt.show()


ax.plot(t/60, mv, color="green")
ax.set(xlabel='tempo (min)', ylabel='sinal de controle (mA)', title='Sinal de controle 3')
ax.grid()

fig.savefig("MV3.png")
plt.show()

fig, ax = plt.subplots()
ax.plot(t/60, pv)
ax.set(xlabel='tempo (min)', ylabel='nível do tanque (cm)', title='Nível do tanque 3')
ax.grid()

fig.savefig("PV3.png")
plt.show()


ax.plot(t/60, mv, color="green")
ax.set(xlabel='tempo (min)', ylabel='sinal de controle (mA)', title='Sinal de controle 4')
ax.grid()

fig.savefig("MV4.png")
plt.show()

fig, ax = plt.subplots()
ax.plot(t/60, pv)
ax.set(xlabel='tempo (min)', ylabel='nível do tanque (cm)', title='Nível do tanque 4')
ax.grid()

fig.savefig("PV4.png")
plt.show()


