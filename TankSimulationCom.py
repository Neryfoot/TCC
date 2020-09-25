import time
from multiprocessing import Process, Value
import serial

h = 0.1  # passo da solução numérica
Fin = Value('f', 4.0)  # fluxo de entrada
yk_1 = 0  # condição inicial
yk_sync = Value('f', 0)  # condição inicial

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
        else:
            buffer += one_byte


def device02(buffer, ser):  # simulate device behavior
    data = b">" + bytes(str(yk_sync.value), "ascii") + b"\r"
    ser.write(data)
    print('02')


def device03(buffer, ser):  # simulate device behavior
    data = buffer
    data = data[4:]
    data = data[:-1]
    data = float(data)
    Fin.value = data
    print('03')


def dynamic():
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
                yk = 0.004*Fin.value + 0.96*yk_1
                if yk < 0:  # nível não pode baixar de 0
                    yk = 0
                if yk > 0.5:  # nível não passa de 0.5
                    yk = 0.5
                yk_1 = yk
                steps -= 1
        yk_sync.value = yk
        print(yk)


dynamic_process = Process(target=dynamic)
com_process = Process(target=communication, args=(ser,))
dynamic_process.start()
com_process .start()
