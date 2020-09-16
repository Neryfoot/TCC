import serial


def read_data():  # read bytes until read \r(carriage return)
    buffer = ""
    while True:
        one_byte = ser.read(1)
        if one_byte == b"\r":    # method should returns bytes
            return buffer
        else:
            buffer += one_byte.decode()


def read_ch(AA: bytes, N: bytes):  # Read sthe analog input
    command = b"#" + AA + N + b"\r"  # command in hex array
    ser.write(command)
    data = read_data()  # reads response
    return data


def write_ch(AA: bytes, N: bytes, data: bytes):  # Write data to analog output
    command = b"#" + AA + N + data + b"\r"  # command in bytes array
    ser.write(command)  # command example #AAN20.000, sets 20mA as output
    data = read_data()  # reads response
    return data 


def checksum(cmd: bytes):  # calculates the checksum of command string
    cmd = cmd[:-1]  # deletes CR from the command
    ck = sum(cmd) & 0xFF  # checksum is equal to sum masked by 0xFF
    ck = hex(ck)  # gets hexadecimal representation string
    ck = bytes(ck[2]+ck[3], "ascii")  # gets ascii value of those characters
    return ck


def read_ch_ck(AA: bytes, N: bytes):  # Read sthe analog input
    command = b"#" + AA + N + b"\r"  # command in hex array
    command = command[:-1] + checksum(command) + b"\r"  # add checksum 
    ser.write(command)
    data = read_data()  # reads response
    return data


def write_ch_ck(AA: bytes, N: bytes, data: bytes):  # Write data to a. output
    command = b"#" + AA + N + data + b"\r"  # command in bytes array
    command = command[:-1] + checksum(command) + b"\r"  # add checksum 
    ser.write(command)  # command example #AAN20.000, sets 20mA as output
    data = read_data()  # reads response
    return data 

