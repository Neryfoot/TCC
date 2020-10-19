import serial
import time
import threading
from multiprocessing import Process, Value
from opcua import ua, Server
import DCON

yk_1 = 0
e_1 = 0
# Tanque 1
lvl1 = Value('f', 0)  # condição inicial de nivel
pump1 = Value('f', 4.0)  # fluxo de entrada
flow1 = Value('f', 0) # vazão de entrada
ref1 = Value('f', 0) # referência
# Tanque 2
lvl2 = Value('f', 0)  # condição inicial de nivel
pump2 = Value('f', 3.5)  # fluxo de entrada
flow2 = Value('f', 1) # vazão de entrada
ref2 = Value('f', 0) # referência
# Tanque 3
lvl3 = Value('f', 0)  # condição inicial de nivel
pump3 = Value('f', 3.0)  # fluxo de entrada
flow3 = Value('f', 2) # vazão de entrada
ref3 = Value('f', 0) # referência
# Tanque 4
lvl4 = Value('f', 0)  # condição inicial de nivel
pump4 = Value('f', 2.5)  # fluxo de entrada
flow4 = Value('f', 3) # vazão de entrada
ref4 = Value('f', 0) # referência

# Tanque 5 e 6 não têm medidor de vazão
lvl5 = Value('f', 0)  # condição inicial de nivel
pump5 = Value('f', 2.0)  # fluxo de entrada
ref5 = Value('f', 0) # referência
lvl6 = Value('f', 0)  # condição inicial de nivel
pump6 = Value('f', 1.0)  # fluxo de entrada
ref6 = Value('f', 0) # referência

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # open serial port

flows = [flow1, flow2, flow3, flow4]
lvls = [lvl1, lvl2, lvl3, lvl4, lvl5, lvl6]
pumps = [pump1, pump2, pump3, pump4, pump5, pump6]


def communication():
    ""
    

def controller():
    global yk_1
    global e_1
    e = ref1.value - lvl1.value
    yk = 0.1*e + 0.9*e_1+ yk_1
    if yk > 5:
        yk = 5
    if yk < 0:
        yk = 0
    e_1 = e
    yk_1 = yk
    pump1.value = yk
    print(yk)


communication()
DCON.write_ch(b"03", b"2", bytes(str(pump1.value), "ascii"), ser)
ref1.value
ref1.value=0.3
