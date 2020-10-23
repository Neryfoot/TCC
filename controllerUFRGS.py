import time
import threading
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from multiprocessing import Process, Value
from opcua import ua, Client



url = "opc.tcp://143.54.96.127:2194"

client = Client(url)

client.connect()
# Variables
yk_11 = 0
yk_12 = 0
e_11 = 0
e_12 = 0
stop_flag = 0
t_01 = 0
PV1 = []
MV1 = []
t1 = []
tread1 = []
twrite1 = []

# Variables
yk_21 = 0
yk_22 = 0
e_21 = 0
e_22 = 0
stop_flag = 0
t_02 = 1
PV2 = []
MV2 = []
t2 = []
tread2 = []
twrite2 = []

# Variables
yk_31 = 0
yk_32 = 0
e_31 = 0
e_32 = 0
stop_flag = 0
t_03 = 1
PV3 = []
MV3 = []
t3 = []
tread3 = []
twrite3 = []

# Variables
yk_41 = 0
yk_42 = 0
e_41 = 0
e_42 = 0
stop_flag = 0
t_04 = 1
PV4 = []
MV4 = []
t4 = []
tread4 = []
twrite4 = []


lvl1 = client.get_node("ns=2;i=2")
lvl2 = client.get_node("ns=2;i=3")
lvl3 = client.get_node("ns=2;i=4")
lvl4 = client.get_node("ns=2;i=5")
lvl5 = client.get_node("ns=2;i=6")
lvl6 = client.get_node("ns=2;i=7")

flow1 = client.get_node("ns=2;i=9")
flow2 = client.get_node("ns=2;i=10")
flow3 = client.get_node("ns=2;i=11")
flow4 = client.get_node("ns=2;i=12")

pump1 = client.get_node("ns=2;i=14")
pump2 = client.get_node("ns=2;i=15")
pump3 = client.get_node("ns=2;i=16")
pump4 = client.get_node("ns=2;i=17")
pump5 = client.get_node("ns=2;i=18")
pump6 = client.get_node("ns=2;i=19")

ref1 = Value('f', 20) # referência
ref2 = Value('f', 0) # referência
ref3 = Value('f', 0) # referência
ref4 = Value('f', 0) # referência
ref5 = Value('f', 0) # referência
ref6 = Value('f', 0) # referência

h1 = Value ('f',0) # nível do tanque 1
h2 = Value ('f',0) # nível do tanque 2
h3 = Value ('f',0) # nível do tanque 3
h4 = Value ('f',0) # nível do tanque 4
h5 = Value ('f',0) # nível do tanque 5
h6 = Value ('f',0) # nível do tanque 6

u1 = Value('f', 0) # sinal de controle do tanque 1
u2 = Value('f', 0) # sinal de controle do tanque 2
u3 = Value('f', 0) # sinal de controle do tanque 3
u4 = Value('f', 0) # sinal de controle do tanque 4
u5 = Value('f', 0) # sinal de controle do tanque 5
u6 = Value('f', 0) # sinal de controle do tanque 6


def get_level(lvl):
    if lvl == 1:
        h1 = lvl1.get_value() # leitura em mA 
        h1.value = 0.0078*((h1)**3) - 0.2790*((h1)**2) + 4.3687*((h1)**1) -12.724 # converte em cm
    elif lvl == 2:
        h2 = lvl2.get_value() # leitura em mA
        h2.value = 0.0073*((h2)**3) - 0.2598*((h2)**2) + 4.1948*((h2)**1) -12.9610 # converte em cm
    elif lvl == 3:
        h3 = lvl3.get_value() # leitura em mA
        h3.value = 0.0083*((h3)**3) - 0.3122*((h3)**2) + 4.9216*((h3)**1) -16.2650 # converte em cm 
    elif lvl == 4:
        h4 = lvl4.get_value() # leitura em mA
        h4.value = 0.0063*((h4)**3) - 0.2491*((h4)**2) + 4.3008*((h4)**1) -14.561 # converte em cm 
    elif lvl == 5:
        h5 = lvl5.get_value() # leitura em mA
        h5.value = 0.0102*((h5)**3) - 0.4416*((h5)**2) + 7.2539*((h5)**1) -21.7 # converte em cm 
    elif lvl == 6:
        h6 = lvl6.get_value() # leitura em mA
        h6.value = 0.0070*((h6)**3) - 0.3233*((h6)**2) + 5.9765*((h6)**1) -22.9 # converte em cm 


def get_levelsim(lvl):
    if lvl == 1:
        h1.value = lvl1.get_value() # leitura em mA 
    elif lvl == 2:
        h2.value = lvl2.get_value() # leitura em mA
    elif lvl == 3:
        h3.value = lvl3.get_value() # leitura em mA
    elif lvl == 4:
        h4.value = lvl4.get_value() # leitura em mA
    elif lvl == 5:
        h5.value = lvl5.get_value() # leitura em mA
    elif lvl == 6:
        h6.value = lvl6.get_value() # leitura em mA


# def controller():
#     global yk_1
#     global yk_2
#     global e_1
#     global e_2
#     h1 = lvl1.get_value() # leitura em mA 
#     h1.value = 0.0078*((h1)**3) - 0.2790*((h1)**2) + 4.3687*((h1)**1) -12.724 # converte em cm
#     e = ref1.value - h1.value
#     yk = 4*e -6.8*e_1 + 3*e_2 + 1*yk_1 
#     if yk > 20:
#         yk = 20
#     if yk < 0:
#         yk = 0
#     # atualiza as variáveis
#     e_2 = e_1
#     e_1 = e
#     yk_2 = yk_1
#     yk_1 = yk
#     pump1.set_value(float(yk))
#     print(yk)
#     if stop_flag == 0:
#         threading.Timer(1, controller).start()


def controller1():
    global yk_11
    global yk_12
    global e_11
    global e_12
    global t_01, t1
    global PV1, MV1
    t_start = time.time()
    h = lvl1.get_value() # leitura em mA 
    t_end = time.time()
    tread = t_end - t_start
    h1.value = h
    # h1.value = 0.0078*((h)**3) - 0.2790*((h)**2) + 4.3687*((h)**1) -12.724 # converte em cm
    e = ref1.value - h1.value
    yk = 4*e - 6.8*e_11 + 3*e_12 + 1*yk_11
    if yk > 20:
        yk = 20
    if yk < 0:
        yk = 0
    # atualiza as variáveis
    e_12 = e_11
    e_11 = e
    yk_12 = yk_11
    yk_11 = yk
    t_start = time.time()
    pump1.set_value(float(yk))
    t_end = time.time()
    twrite = t_end - t_start
    print(yk)
    print(h)
    print(h1.value)
    PV1.append(h1.value)
    MV1.append(yk)
    t = t_start - t_01
    t1.append(t)
    tread1.append(tread)
    twrite1.append(twrite)
    if stop_flag == 0:
        threading.Timer(1, controller1).start()
        
def controller2():
    global yk_21
    global yk_22
    global e_21
    global e_22
    global t_02, t2
    global PV2, MV2
    t_start = time.time()
    h = lvl3.get_value() # leitura em mA 
    t_end = time.time()
    tread = t_end - t_start
    h = h[1:]
    h = float(h)
    # h1.value = h
    h2.value = 0.0078*((h)**3) - 0.2790*((h)**2) + 4.3687*((h)**1) -12.724 # converte em cm
    e = ref2.value - h2.value
    yk = 4*e - 6.8*e_21 + 3*e_22 + 1*yk_21
    if yk > 20:
        yk = 20
    if yk < 0:
        yk = 0
    # atualiza as variáveis
    e_22 = e_21
    e_21 = e
    yk_22 = yk_21
    yk_21 = yk
    t_start = time.time()
    pump3.set_value(float(yk))
    t_end = time.time()
    twrite = t_end - t_start
    print(yk)
    #print(h)
    #print(h2.value)
    PV2.append(h2.value)
    MV2.append(yk)
    t = t_start - t_02
    t2.append(t)
    tread2.append(tread)
    twrite2.append(twrite)
    if stop_flag == 0:
        threading.Timer(1, controller2).start()


ref1.value=3
ref2.value=10
t_01 = time.time()
t_02 = time.time()
controller2()
stop_flag = 1
stop_flag = 0


client.disconnect()

results1 = np.vstack((t1, PV1, MV1, tread1))
results1 = results1.transpose()
np.savetxt('results1.csv', results1, delimiter=',')
np.savetxt('t1.txt', t1, delimiter=',')
np.savetxt('PV1.txt', PV1, delimiter=',')
np.savetxt('MV1.txt', MV1, delimiter=',')
np.savetxt('tread1.txt', tread1, delimiter=',')

fig, ax = plt.subplots()
ax.plot(t1, MV1)

ax.set(xlabel='tempo (s)', ylabel='sinal de controle em mA',
       title='MV')
ax.grid()

fig.savefig("MV.png")
plt.show()

fig, ax = plt.subplots()
ax.plot(t1, PV1)

ax.set(xlabel='tempo (s)', ylabel='nível do tanque %',
       title='PV')
ax.grid()

fig.savefig("PV.png")
plt.show()
