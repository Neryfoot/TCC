

#from Tkinter import *  # Python <= 2.7
from tkinter import *  # Python > 2.7
import time
import serial

V_cc = 4.97	# This is the ADC's positive reference voltage
global comms	# This boolean variable will save the communications (comms) status
comms = True

#------------------------Definitions-----------------------
def isfloat(x):
    #Check if the received 4 characters can be converted to a float
    try:
            float(x)
            return True
    except ValueError:
            return False

class Application(Frame):
    def exit_protocol(self):
	# Will be called when the main window is closed
	# It should close the serial port if it has not 
	# been previously closed
        global comms
        if (comms):
            ser.close()
        self.master.destroy()	# Destroy root window
        self.master.quit()		# Exiting the main loop

    def say_msg(self):
        print("You pressed me!!!")  # Python > 2.7
        #print "You pressed me!!!"  # Python <= 2.7

    def comm(self):
        global comms
        if (comms):
            # Closing comms
            comms = False
            self.QUIT.configure(text = 'RS-232: OFF')
            self.QUIT.configure(fg = 'black')
            ser.close()
        else:
            # Re-opening comms
            comms = True
            self.QUIT.configure(text = 'RS-232: ON')
            self.QUIT.configure(fg = 'red')
            ser.open()

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "RS-232: ON"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.comm	# Will call the comms procedure
        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "PressMe",
        self.hi_there["command"] = self.say_msg	# Will call the say_msg procedure
        self.hi_there.pack({"side": "left"})

        global message
        self.message = Label(text='ATmega328P: ')
        self.message.pack()

        global ADC0
        self.ADC0 = Label(text='ADC0: ')
        self.ADC0.pack()

        global ADC1
        self.ADC1 = Label(text='ADC1: ')
        self.ADC1.pack()

        global ADC2
        self.ADC2 = Label(text='ADC2: ')
        self.ADC2.pack()

    def Refresher(self):
        global comms
        if (comms):
            global message
	    # The ATmega328 is expecting an arbitrary message to trigger the RX interrupt
            #ser.write('\r\n')   # Python <= 2.7
            ser.write(b'\r\n')  # Python > 2.7
            time.sleep(0.01)	# Wait for the connected device to respond
            out = ''		# Preparing the out variable
			
            while ser.inWaiting() > 0:
                while True:
                    # Check if trash is being received from the RS-232 such as %$///#@@ or Chinese characters
                    try:
                        # Append all of the received bytes into a single string
                        out += ser.read().decode('ascii') #python > 2.7
                        #out += ser.read()                 #python <= 2.7
                        break
                    except ValueError:
                        out = ''
						
            if out != '':
		# A clean message has been received- format: '####/####/.../####\r\n' where #### are 4 digits from 0000 to 1023
                self.message.configure(text='ATmega328P: '+ str(out))
                
                value = str(out[0:4])	# Extract the first four digits of the package
                if isfloat(value):
                    number = float(value)*V_cc/1024;	# Denormalizing from bits to Volts 1023 bits = 5 V
                    self.ADC0.configure(text='ADC0: %5.3f' % number)
                    
                value = str(out[5:9])	# Extract the NEXT first four digits of the package
                if isfloat(value):
                    number = float(value)*V_cc/1024;
                    self.ADC1.configure(text='ADC1: %5.3f' % number)
                    
                value = str(out[10:14])	# Extract the NEXT four digits of the package
                if isfloat(value):
                    number = float(value)*V_cc/1024;
                    self.ADC2.configure(text='ADC2: %5.3f' % number)
                    
        root.after(1000, self.Refresher) # Call the procedure every 1000 millisecs (1 sec)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
	# Call the core procedures
        self.createWidgets()
        self.Refresher()
        # Exit when the 'x' button is pressed, notice that its the name of the function
        # 'self.handler' and not a method call self.handler()
        master.protocol("WM_DELETE_WINDOW", self.exit_protocol)

#------------------------Main Program-----------------------
#port_name = raw_input("Enter a port name: ") # Python <= 2.7
port_name = input("Enter a port name: ")      # Python > 2.7
ser = serial.Serial(
      port = port_name,
      baudrate = 9600,
      parity = serial.PARITY_NONE,
      bytesize = serial.EIGHTBITS,
      stopbits = serial.STOPBITS_ONE,
      xonxoff = 0,
      rtscts = 0,
      timeout = 1
)

ser.close()
ser.open()

root = Tk()
app = Application(master=root)
app.mainloop()

