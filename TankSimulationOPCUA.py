import time
from multiprocessing import Process, Value
import serial
import numpy as np

h = 0.1  # passo da solução numérica
yk_1 = 0  # condição inicial
stop_flag = 0 # flag para parar os processos
t_0= 0
t_read= []
time= []
PV = []
MV = []

# Tanque 1
h1 = Value('f', 0)  # condição inicial de nivel
u1 = Value('f', 16)  # fluxo de entrada
f1 = Value('f', 0) # vazão de entrada
# Tanque 2
h2 = Value('f', 0)  # condição inicial de nivel
u2 = Value('f', 3.5)  # fluxo de entrada
f2 = Value('f', 1) # vazão de entrada
# Tanque 3
h3 = Value('f', 0)  # condição inicial de nivel
u3 = Value('f', 3.0)  # fluxo de entrada
f3 = Value('f', 2) # vazão de entrada
# Tanque 4
h4 = Value('f', 0)  # condição inicial de nivel
u4 = Value('f', 2.5)  # fluxo de entrada
f4 = Value('f', 3) # vazão de entrada

# Tanque 5 e 6 não têm medidor de vazão
h5 = Value('f', 0)  # condição inicial de nivel
u5 = Value('f', 2.0)  # fluxo de entrada
h6 = Value('f', 0)  # condição inicial de nivel
u6 = Value('f', 1.0)  # fluxo de entrada






ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # open serial port


def read_data(ser):  # read bytes until read \r(carriage return)
    buffer = ""
    while True:
        one_byte = ser.read(1)
        if one_byte == b"\r":    # method should returns bytes
            return buffer
        else:
            buffer += one_byte.decode()


def communication(ser):  # simulate device behavior
    buffer = b""
    while stop_flag == 0:
        one_byte = ser.read(1)
        if one_byte == b"\r":
            if buffer[0:3] == b"#02":
                device02(buffer, ser)
                buffer = b""
            if buffer[0:3] == b"#03":
                device03(buffer, ser)
                buffer = b""
            if buffer[0:3] == b"#05":
                device05(buffer, ser)
                buffer = b""
        else:
            buffer += one_byte


def device02(buffer, ser):  # simulate device behavior
    case = int(chr(buffer[3]))
    if case == 0:
        data = b">" + bytes(str(f1.value), "ascii") + b"\r"
        ser.write(data)
    elif case == 1:
        data = b">" + bytes(str(f2.value), "ascii") + b"\r"
        ser.write(data)
    elif case == 2:
        data = b">" + bytes(str(f3.value), "ascii") + b"\r"
        ser.write(data)
    elif case == 3:
        data = b">" + bytes(str(f4.value), "ascii") + b"\r"
        ser.write(data)


def device05(buffer, ser):  # simulate device behavior
    case = int(chr(buffer[3]))
    if case == 0:
        data = b">" + bytes(str(h1.value), "ascii") + b"\r"
        ser.write(data)
    elif case == 1:
        data = b">" + bytes(str(h2.value), "ascii") + b"\r"
        ser.write(data)
    elif case == 2:
        data = b">" + bytes(str(h3.value), "ascii") + b"\r"
        ser.write(data)
    elif case == 3:
        data = b">" + bytes(str(h4.value), "ascii") + b"\r"
        ser.write(data)
    elif case == 4:
        data = b">" + bytes(str(h5.value), "ascii") + b"\r"
        ser.write(data)
    elif case == 5:
        data = b">" + bytes(str(h6.value), "ascii") + b"\r"
        ser.write(data)



def device03(buffer, ser):  # simulate device behavior 
    case = int(chr(buffer[3]))
    data = buffer
    data = data[5:]
    data = data[:-1]
    data = float(data) #retirou caracteres do protocolo
    if case == 0:
        u1.value = data
    elif case == 1:
        u2.value = data
    elif case == 2:
        u3.value = data
    elif case == 3:
        u4.value = data
    elif case == 4:
        u5.value = data
    elif case == 5:
        u6.value = data
    ser.write(b">\r")


def dynamic1():
    global yk_1
    global h
    yk = h1.value
    steps = 0  # condição inicial
    tn_1 = float("{:.1f}".format(time.time()))  # condição inicial
    while stop_flag == 0:
        tn = float("{:.1f}".format(time.time()))  # tempo atual
        steps = (tn - tn_1)//h  # número de passos
        # print(steps)
        tn_1 = tn_1 + steps*h  # atualiza o tempo
        if steps > 0:
            while(steps > 0):  # executa atualização da função
                yk = 0.4988*u1.value/20 + 0.995*yk_1
                if yk < 0:  # nível não pode baixar de 0
                    yk = 0
                if yk > 100:  # nível não passa de 100
                    yk = 100
                yk_1 = yk
                steps -= 1
        h1.value = yk


def dynamic2():
    global yk_1
    global h
    yk = h2.value*0.5/100
    steps = 0  # condição inicial
    tn_1 = float("{:.1f}".format(time.time()))  # condição inicial
    while stop_flag == 0:
        tn = float("{:.1f}".format(time.time()))  # tempo atual
        steps = (tn - tn_1)//h  # número de passos
        # print(steps)
        tn_1 = tn_1 + steps*h  # atualiza o tempo
        if steps > 0:
            while(steps > 0):  # executa atualização da função
                yk = 0.004*u2.value + 0.96*yk_1
                if yk < 0:  # nível não pode baixar de 0
                    yk = 0
                if yk > 0.5:  # nível não passa de 0.5
                    yk = 0.5
                yk_1 = yk
                steps -= 1
        h2.value = yk*100/0.5


def dynamic3():
    global yk_1
    global h
    yk = h3.value*0.5/100
    steps = 0  # condição inicial
    tn_1 = float("{:.1f}".format(time.time()))  # condição inicial
    while stop_flag == 0:
        tn = float("{:.1f}".format(time.time()))  # tempo atual
        steps = (tn - tn_1)//h  # número de passos
        # print(steps)
        tn_1 = tn_1 + steps*h  # atualiza o tempo
        if steps > 0:
            while(steps > 0):  # executa atualização da função
                yk = 0.004*u3.value + 0.96*yk_1
                if yk < 0:  # nível não pode baixar de 0
                    yk = 0
                if yk > 0.5:  # nível não passa de 0.5
                    yk = 0.5
                yk_1 = yk
                steps -= 1
        h3.value = yk*100/0.5


def dynamic4():
    global yk_1
    global h
    yk = h4.value*0.5/100
    steps = 0  # condição inicial
    tn_1 = float("{:.1f}".format(time.time()))  # condição inicial
    while stop_flag == 0:
        tn = float("{:.1f}".format(time.time()))  # tempo atual
        steps = (tn - tn_1)//h  # número de passos
        # print(steps)
        tn_1 = tn_1 + steps*h  # atualiza o tempo
        if steps > 0:
            while(steps > 0):  # executa atualização da função
                yk = 0.004*u4.value + 0.96*yk_1
                if yk < 0:  # nível não pode baixar de 0
                    yk = 0
                if yk > 0.5:  # nível não passa de 0.5
                    yk = 0.5
                yk_1 = yk
                steps -= 1
        h4.value = yk*100/0.5


def dynamic5():
    global yk_1
    global h
    yk = h5.value*0.5/100
    steps = 0  # condição inicial
    tn_1 = float("{:.1f}".format(time.time()))  # condição inicial
    while stop_flag == 0:
        tn = float("{:.1f}".format(time.time()))  # tempo atual
        steps = (tn - tn_1)//h  # número de passos
        # print(steps)
        tn_1 = tn_1 + steps*h  # atualiza o tempo
        if steps > 0:
            while(steps > 0):  # executa atualização da função
                yk = 0.004*u5.value + 0.96*yk_1
                if yk < 0:  # nível não pode baixar de 0
                    yk = 0
                if yk > 0.5:  # nível não passa de 0.5
                    yk = 0.5
                yk_1 = yk
                steps -= 1
        h5.value = yk*100/0.5


def dynamic6():
    global yk_1
    global h
    yk = h1.value*0.5/100
    steps = 0  # condição inicial
    tn_1 = float("{:.1f}".format(time.time()))  # condição inicial
    while stop_flag == 0:
        tn = float("{:.1f}".format(time.time()))  # tempo atual
        steps = (tn - tn_1)//h  # número de passos
        # print(steps)
        tn_1 = tn_1 + steps*h  # atualiza o tempo
        if steps > 0:
            while(steps > 0):  # executa atualização da função
                yk = 0.004*u6.value + 0.96*yk_1
                if yk < 0:  # nível não pode baixar de 0
                    yk = 0
                if yk > 0.5:  # nível não passa de 0.5
                    yk = 0.5
                yk_1 = yk
                steps -= 1
        h6.value = yk*100/0.5



dynamic_process1 = Process(target=dynamic1)
# dynamic_process2 = Process(target=dynamic2)
# dynamic_process3 = Process(target=dynamic3)
# dynamic_process4 = Process(target=dynamic4)
# dynamic_process5 = Process(target=dynamic5)
# dynamic_process6 = Process(target=dynamic6)
com_process = Process(target=communication, args=(ser,))
com_process.start()
dynamic_process1.start()
# dynamic_process2.start()
# dynamic_process3.start()
# dynamic_process4.start()
# dynamic_process5.start()
# dynamic_process6.start()ess1.start()
stop_flag = 1
stop_flag = 0
dynamic_process1.terminate()
# dynamic_process2.terminate()
# dynamic_process3.terminate()
# dynamic_process4.terminate()
# dynamic_process5.terminate()
# dynamic_process6.terminate()
com_process.terminate()



