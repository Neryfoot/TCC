import time
from multiprocessing import Process, Value
import serial

h = 0.1  # passo da solução numérica
yk_1 = 0  # condição inicial

# Tanque 1
h1 = Value('f', 0)  # condição inicial de nivel
u1 = Value('f', 4.0)  # fluxo de entrada
f1 = Value('f', 0) # vazão de entrada
# Tanque 2
h2 = Value('f', 0)  # condição inicial de nivel
u2 = Value('f', 4.0)  # fluxo de entrada
f2 = Value('f', 1) # vazão de entrada
# Tanque 3
h3 = Value('f', 0)  # condição inicial de nivel
u3 = Value('f', 4.0)  # fluxo de entrada
f3 = Value('f', 2) # vazão de entrada
# Tanque 4
h4 = Value('f', 0)  # condição inicial de nivel
u4 = Value('f', 4.0)  # fluxo de entrada
f4 = Value('f', 3) # vazão de entrada

# Tanque 5 e 6 não têm medidor de vazão
h5 = Value('f', 0)  # condição inicial de nivel
u5 = Value('f', 4.0)  # fluxo de entrada
h6 = Value('f', 0)  # condição inicial de nivel
u6 = Value('f', 4.0)  # fluxo de entrada






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
    while True:
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
    case = buffer[4]
    if case == 1:
        data = b">" + bytes(str(f1.value), "ascii") + b"\r"
        ser.write(data)
    elif case == 2:
        data = b">" + bytes(str(f2.value), "ascii") + b"\r"
        ser.write(data)
    elif case == 3:
        data = b">" + bytes(str(f3.value), "ascii") + b"\r"
        ser.write(data)
    elif case == 4:
        data = b">" + bytes(str(f4.value), "ascii") + b"\r"
        ser.write(data)



def device05(buffer, ser):  # simulate device behavior
    case = buffer[4]
    if case == 1:
        data = b">" + bytes(str(h1.value), "ascii") + b"\r"
        ser.write(data)
    elif case == 2:
        data = b">" + bytes(str(h2.value), "ascii") + b"\r"
        ser.write(data)
    elif case == 3:
        data = b">" + bytes(str(h3.value), "ascii") + b"\r"
        ser.write(data)
    elif case == 4:
        data = b">" + bytes(str(h4.value), "ascii") + b"\r"
        ser.write(data)
    elif case == 5:
        data = b">" + bytes(str(h5.value), "ascii") + b"\r"
        ser.write(data)
    elif case == 6:
        data = b">" + bytes(str(h6.value), "ascii") + b"\r"
        ser.write(data)



def device03(buffer, ser):  # simulate device behavior 
    data = buffer
    case = data[4] # pega o canal a ser lido
    data = data[4:]
    data = data[:-1]
    data = float(data) #retirou caracteres do protocolo
    if case == 1:
        u1.value = data
    elif case == 2:
        u2.value = data
    elif case == 3:
        u3.value = data
    elif case == 4:
        u4.value = data
    elif case == 5:
        u5.value = data
    elif case == 6:
        u6.value = data


def dynamic1():
    global yk_1
    global h
    yk = yk_sync.value
    steps = 0  # condição inicial
    tn_1 = float("{:.1f}".format(time.time()))  # condição inicial
    while 1:
        tn = float("{:.1f}".format(time.time()))  # tempo atual
        steps = (tn - tn_1)//h  # número de passos
        # print(steps)
        tn_1 = tn_1 + steps*h  # atualiza o tempo
        if steps > 0:
            while(steps > 0):  # executa atualização da função
                yk = 0.004*u1.value + 0.96*yk_1
                if yk < 0:  # nível não pode baixar de 0
                    yk = 0
                if yk > 0.5:  # nível não passa de 0.5
                    yk = 0.5
                yk_1 = yk
                steps -= 1
        h1.value = yk
        print(yk)


dynamic_process1 = Process(target=dynamic1)
com_process = Process(target=communication, args=(ser,))
dynamic_process.start()
com_process .start()
