from time import sleep
import random
from opcua import Server

server = Server()
url = "opc.tcp://192.168.15.17:2194"
server.set_endpoint(url)

name = "OPC UA Simulation Server"
addspace = server.register_namespace(name)


node = server.get_objects_node()

lvl = node.add_object(addspace, "Level Sensors")
lvl1 = lvl.add_variable(addspace, "LVL1", 5)
lvl2 = lvl.add_variable(addspace, "LVL2", 6)
lvl3 = lvl.add_variable(addspace, "LVL3", 7)
lvl4 = lvl.add_variable(addspace, "LVL4", 8)
lvl5 = lvl.add_variable(addspace, "LVL5", 9)
lvl6 = lvl.add_variable(addspace, "LVL6", 10)

flow = node.add_object(addspace, "Flow Sensors")
flow1 = flow.add_variable(addspace, "FLOW1", 1)
flow2 = flow.add_variable(addspace, "FLOW2", 2)
flow3 = flow.add_variable(addspace, "FLOW3", 3)
flow4 = flow.add_variable(addspace, "FLOW4", 4)


pump = node.add_object(addspace, "Pump Actuators")
pump1 = pump.add_variable(addspace, "PUMP1", 0.1)
pump2 = pump.add_variable(addspace, "PUMP2", 0.2)
pump3 = pump.add_variable(addspace, "PUMP3", 0.3)
pump4 = pump.add_variable(addspace, "PUMP4", 0.4)
pump5 = pump.add_variable(addspace, "PUMP5", 0.5)
pump6 = pump.add_variable(addspace, "PUMP6", 0.6)


server.start()

