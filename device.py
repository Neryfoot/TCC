import serial


def read_data():  # read bytes until read \r(carriage return)
    buffer = ""
    while True:
        one_byte = ser.read(1)
        if one_byte == b"\r":    # method should returns bytes
            return buffer
        else:
            buffer += oneByte.decode()


def read_ch(AA: hex, N: hex):  # Readsthe analog input
    command = b'#'+AA+N  # command in hex array
    ser.write(command)
    data = read_data()
    return data


def device02():  # simulate device behavior
    buffer = b""
    while True:
        one_byte = ser.read(1)
        if one_byte == b"\r":
            if buffer[0:3] == b"#02":
                return b">4004\r"
            else:
                return b"?"
        else:
            buffer += one_byte


ser = serial.Serial('/dev/ttyUSB0')  # open serial port
print(ser.name)         # check which port was really used
ser.open()
a = device02()     # write a string
ser.write(a)
ser.close()             # close port
