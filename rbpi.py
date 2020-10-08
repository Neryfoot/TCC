import serial
import time
import threading
from multiprocessing import Process, Value
from opcua import ua,Server
import DCON

url = "opc.tcp://192.168.15.48:2194"
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # open serial port
stop_flag = 0

server = Server()
server.set_endpoint(url)
name = "OPC UA Simulation Server"
addspace = server.register_namespace(name)
server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt])
# load server certificate and private key
server.load_certificate("certificate.der")
server.load_private_key("key.pem")

node = server.get_objects_node()

lvl = node.add_object(addspace, "Level Sensors")
lvl1 = lvl.add_variable(addspace, "LVL1", 5.0)
lvl2 = lvl.add_variable(addspace, "LVL2", 6.0)
lvl3 = lvl.add_variable(addspace, "LVL3", 7.0)
lvl4 = lvl.add_variable(addspace, "LVL4", 8.0)
lvl5 = lvl.add_variable(addspace, "LVL5", 9.0)
lvl6 = lvl.add_variable(addspace, "LVL6", 10.0)

flow = node.add_object(addspace, "Flow Sensors")
flow1 = flow.add_variable(addspace, "FLOW1", 1.0)
flow2 = flow.add_variable(addspace, "FLOW2", 2.0)
flow3 = flow.add_variable(addspace, "FLOW3", 3.0)
flow4 = flow.add_variable(addspace, "FLOW4", 4.0)

pump = node.add_object(addspace, "Pump Actuators")
pump1 = pump.add_variable(addspace, "PUMP1", 0.1)
pump2 = pump.add_variable(addspace, "PUMP2", 0.2)
pump3 = pump.add_variable(addspace, "PUMP3", 0.3)
pump4 = pump.add_variable(addspace, "PUMP4", 0.4)
pump5 = pump.add_variable(addspace, "PUMP5", 0.5)
pump6 = pump.add_variable(addspace, "PUMP6", 0.6)

flows = [flow1, flow2, flow3, flow4]
lvls = [lvl1, lvl2, lvl3, lvl4, lvl5, lvl6]


def update_variable(variable, AA: bytes, N: bytes, ser):
    data = DCON.read_ch(AA, N, ser)
    data = data[1:]
    data = data[:-1]
    data = float(data)
    variable.set_value(data)
    print(variable)
    print(variable.get_value())

def communication(ser):
    global flows
    global lvls
    for i in range(4):
        update_variable(flows[i], b"02", bytes(str(i), 'ascii'), ser)
    for i in range(6):
        update_variable(lvls[i], b"05", bytes(str(i), 'ascii'), ser)
    if stop_flag == 0:
        threading.Timer(0.2, communication, args=[ser,]).start()


server.start()
communication(ser)
stop_flag = 1
stop_flag = 0
server.stop()
