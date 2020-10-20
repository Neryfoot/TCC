import serial
import time
import threading
from multiprocessing import Process, Value
from opcua import ua, Client
import DCON


url = "opc.tcp://192.168.15.19:2124"

client = Client(url)

client.connect()
# Variables
yk_1 = 0
yk_2 = 0
e_1 = 0
e_2 = 0
stop_flag = 0

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


def controller():
    global yk_1
    global yk_2
    global e_1
    global e_2
    get_levelsim(1)
    e = ref1.value - h1.value
    yk = 11*e -21.59*e_1 + 11*e_2 + 1.007*yk_1 - 0.006738*yk_2
    if yk > 20:
        yk = 20
    if yk < 0:
        yk = 0
    # atualiza as variáveis
    e_2 = e_1
    e_1 = e
    yk_2 = yk_1
    yk_1 = yk
    pump1.set_value(float(yk))
    print(yk)
    if stop_flag == 0:
        threading.Timer(1, controller).start()

ref1.value=20
controller()
stop_flag = 1
