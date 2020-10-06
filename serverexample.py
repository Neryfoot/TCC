from time import sleep
import random
from opcua import Server

server = Server()
server.set_endpoint("opc.tcp://192.168.15.17:2194")
objects = server.get_objects_node()
objects
tempsens = objects.add_object('ns=2; s="TS1"', "Temperature Sensor1")
tempsens
tempsens.add_variable('ns=2; s="TS1_VendorName"',  "TS1 Vendor Name",  "Sensor King")
tempsens.add_variable('ns=2; s="TS1_SerialNumber"',  "TS1 Serial Number",  12345678)
temp = tempsens.add_variable('ns=2; s="TS1_Temperature"',  "TS1 Temperature",  12345678)
bulb = objects.add_object(2, "Light Bulb")
state = bulb.add_variable(2, "State of Light Bulb", False)
state.set_writable()
temperature = 20.0

print("Start Server")
server.start()
server.stop()
print("Server Online")
while True:
    temperature += random.uniform(-1, 1)
    temp.set_value(temperature)
    print("New Temperature: " +str(temp.get_value()))
    print("State of Light Bulb: "+str(state.get_value()))
    sleep(2)
