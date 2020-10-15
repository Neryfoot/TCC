import serial
import time
import threading
from multiprocessing import Process, Value

lvl = Value('f', 0)  # fluxo de entrada
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # open serial port
u = Value('f', 0)
yk_1 = 0
ref = Value('f', 0.25)
e_1 = 0
stop_flag = 0


def read_data(ser):  # read bytes until read \r(carriage return)
    buffer = ""
    while True:
        one_byte = ser.read(1)
        if one_byte == b"\r":    # method should returns bytes
            return buffer
        else:
            buffer += one_byte.decode()


def read_ch(AA: bytes, N: bytes, ser):  # Read sthe analog input
    command = b"#" + AA + N + b"\r"  # command in hex array
    ser.write(command)
    data = read_data(ser)  # reads response
    return data


def write_ch(AA: bytes, N: bytes, data: bytes, ser):  # Write data to analog output
    command = b"#" + AA + N + b"+" + data + b"\r"  # command in bytes array
    ser.write(command)  # command example #AAN+20.000, sets 20mA as output


# def checksum(cmd: bytes):  # calculates the checksum of command string
#     cmd = cmd[:-1]  # deletes CR from the command
#     ck = sum(cmd) & 0xFF  # checksum is equal to sum masked by 0xFF
#     ck = hex(ck)  # gets hexadecimal representation string
#     ck = bytes(ck[2]+ck[3], "ascii")  # gets ascii value of those characters
#     return ck


# def read_ch_ck(AA: bytes, N: bytes, ser):  # Read sthe analog input
#     command = b"#" + AA + N + b"\r"  # command in hex array
#     command = command[:-1] + checksum(command) + b"\r"  # add checksum 
#     ser.write(command)
#     data = read_data()  # reads response
#     return data


# def write_ch_ck(AA: bytes, N: bytes, data: bytes):  # Write data to a. output
#     command = b"#" + AA + N + data + b"\r"  # command in bytes array
#     command = command[:-1] + checksum(command) + b"\r"  # add checksum 
#     ser.write(command)  # command example #AAN20.000, sets 20mA as output
#     data = read_data()  # reads response
#     return data


def communication(ser):
    read_task(ser)
    controller()
    write_ch(b"03", b"2", bytes(str(u.value), "ascii"), ser)
    if stop_flag == 0:
        threading.Timer(1, communication, args=[ser,]).start()


def read_task(ser):
    data = read_ch(b"02", b"1", ser)
    data = data[1:]
    data = data[:-1]
    data = float(data)
    lvl.value = data
    print('ok')


def controller():
    global yk_1
    global e_1
    e = ref.value - lvl.value
    yk = 0.1*e + 0.9*e_1 + yk_1
    if yk > 5:
        yk = 5
    if yk < 0:
        yk = 0
    e_1 = e
    yk_1 = yk
    u.value = yk
    print(yk)


communication(ser)
read_task(ser)
write_ch(b"03", b"2", bytes(str(u.value), "ascii"), ser)
ref.value
ref.value=0.3
