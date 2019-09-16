import Tkinter as tk
from Tkinter import *
import ttk
import serial
import time
import pprint
import tkMessageBox
import serial.tools.list_ports
import struct
import ctypes
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print p
portBeforSub = p
port = str(portBeforSub)
port = port[2:6]
print port
set_baudrate = 9600
set_timeout = 1


class ChannelConfig(ctypes.Structure):
    _fields_ = [("ClockRate",   ctypes.c_int),
                ("LatencyTimer", ctypes.c_ubyte),
                ("Options",     ctypes.c_int)]


class I2C_TRANSFER_OPTION(object):
    START_BIT = 0x01
    STOP_BIT = 0x02
    BREAK_ON_NACK = 0x04
    NACK_LAST_BYTE = 0x08
    FAST_TRANSFER_BYTES = 0x10
    FAST_TRANSFER_BITS = 0x20
    FAST_TRANSFER = 0x30
    NO_ADDRESS = 0x40


def init_i2c():
    try:
        close_i2c()
    except:
        print "initing i2c"
    global libMPSSE, chn_count, chn_conf, chn_no, handle, mode
    libMPSSE = ctypes.cdll.LoadLibrary("C:\\Users\\718080\\Desktop\\MDprebuild\\libMPSSE.dll")
    chn_count = ctypes.c_int()
    chn_conf = ChannelConfig(400000, 5, 0)
    chn_no = 0
    handle = ctypes.c_void_p()
    mode = I2C_TRANSFER_OPTION.START_BIT | I2C_TRANSFER_OPTION.STOP_BIT

    libMPSSE.Init_libMPSSE()
    ret = libMPSSE.I2C_GetNumChannels(ctypes.byref(chn_count))
    ret = libMPSSE.I2C_OpenChannel(chn_no, ctypes.byref(handle))
    ret = libMPSSE.I2C_InitChannel(handle, ctypes.byref(chn_conf))
    return(ret)


def close_i2c():
    ret = 0
    try:
        ret = libMPSSE.I2C_CloseChannel(handle)
        libMPSSE.Cleanup_libMPSSE()
        ctypes.cdll.FreeLibrary(libMPSSE)
    except:
        return 99
    return(ret)


def i2c_write(i2c_addr, i2c_req):
    values = i2c_req
    raw = struct.pack("%dB" % len(values), *values)
    bytes_transfered = ctypes.c_int()
    buf = ctypes.create_string_buffer(raw, len(raw))
    ret = libMPSSE.I2C_DeviceWrite(handle, i2c_addr, len(
        buf), buf, ctypes.byref(bytes_transfered), mode)
    return(ret)


def i2c_read(i2c_addr, datasize=1):
    values = [0x00]*datasize
    raw = struct.pack("%dB" % len(values), *values)
    bytes_transfered = ctypes.c_int()
    buf = ctypes.create_string_buffer(raw, len(raw))
    ret = libMPSSE.I2C_DeviceRead(handle, i2c_addr, len(
        buf), buf, ctypes.byref(bytes_transfered), mode)
    return(buf.value)


def i2c_read8bytes(i2c_addr, datasize=8):
    values = [0x00]*datasize
    raw = struct.pack("%dB" % len(values), *values)
    bytes_transfered = ctypes.c_int()
    buf = ctypes.create_string_buffer(raw, len(raw))
    ret = libMPSSE.I2C_DeviceRead(handle, i2c_addr, len(
        buf), buf, ctypes.byref(bytes_transfered), mode)
    #print("I2C_DeviceRead status:",ret, "transfered:",bytes_transfered8)
    return(buf.value)


def delete():
    current.delete(0, END)


def input_volt(command="VSET"):
    powerPort = serial.Serial(port=port, baudrate=set_baudrate, timeout=set_timeout)
    v_in = E1.get()
    if v_in == '':
        v_in = 0
    v_in = float(v_in)+0.1
    powerPort.write(command+" "+str(v_in)+";OUT1\r\n".encode())
    voltDisplay = powerPort.read(100)
    powerPort.close()
    return voltDisplay


def input_current(command="ISET"):
    powerPort = serial.Serial(port=port, baudrate=set_baudrate, timeout=set_timeout)
    v_in = E2.get()
    if v_in == '':
        v_in = 0
    v_in = float(v_in)+0.1
    powerPort.write(command+" "+str(v_in)+";OUT1\r\n".encode())
    currentDisplay = powerPort.read(100)
    powerPort.close()
    return currentDisplay


def allOutput(command="VSET?"):
    powerPort = serial.Serial(port=port, baudrate=set_baudrate, timeout=set_timeout)
    powerPort.write(command+"\r\n".encode())
    voltDisplay = powerPort.read(100)
    powerPort.close()
    powerPort1 = serial.Serial(port=port, baudrate=set_baudrate, timeout=set_timeout)
    powerPort1.write("ISET?\r\n".encode())
    currentDisplay = powerPort1.read(100)
    powerPort1.close()
    listbox = tk.Listbox(frame3, height=2)
    listbox.insert(1, voltDisplay)
    listbox.insert(2, currentDisplay)
    listbox.grid(row=4, column=1)
    return voltDisplay


def output_current(command="ISET?"):
    powerPort = serial.Serial(port=port, baudrate=set_baudrate, timeout=set_timeout)
    powerPort.write(command+"\r\n".encode())
    currentDisplay = powerPort.read(100)
    powerPort.close()
    return currentDisplay


def OFF_volt(command="OUT0"):
    powerPort = serial.Serial(port=port, baudrate=set_baudrate, timeout=set_timeout)
    powerPort.write(command+"\r\n".encode())
    voltDisplay = powerPort.read(100)
    powerPort.close()
    return voltDisplay


def OFF_current(command="OUT0"):
    powerPort = serial.Serial(port=port, baudrate=set_baudrate, timeout=set_timeout)
    powerPort.write(command+"\r\n".encode())
    currentDisplay = powerPort.read(100)
    powerPort.close()
    return currentDisplay


root = tk.Tk()
root.title('Power Supply')
root.geometry('800x600')
number = tk.StringVar()

frame = Frame(root, bd=3, padx=10, pady=5, height=500, width=500, relief=GROOVE)
frame.grid(row=1, column=0, sticky=N)
frame1 = Frame(root, bd=3, padx=10, pady=5, height=500, width=500, relief=GROOVE)
frame1.grid(row=1, column=1, sticky=W)
frame2 = Frame(root, bd=3, padx=10, pady=5, height=500, width=500, relief=GROOVE)
frame2.grid(row=2, column=0, sticky=N)
frame3 = Frame(root, bd=3, padx=10, pady=5, height=500, width=500, relief=GROOVE)
frame3.grid(row=2, column=1, sticky=W)

Rosa = Label(root, text="ROSA Test(SIC)").grid(row=0, column=0, sticky=W)
OC_loop = Label(frame, text="Open Close Loop", relief=GROOVE).grid(row=2)
Label(frame, text="Cycles : ").grid(row=3)
Label(frame, text="Current Cycle : ").grid(row=4)
E1 = Entry(frame, width=20).grid(row=3, column=2)
E2 = Entry(frame, width=20).grid(row=4, column=2)
OC_loop = Label(frame, text="Delay After (ms)", relief=GROOVE).grid(row=5)
Label(frame, text="Open(ms) : ").grid(row=6)
Label(frame, text="Close(ms) : ").grid(row=7)
E1 = Entry(frame, width=20).grid(row=6, column=2)
E2 = Entry(frame, width=20).grid(row=7, column=2)
Start = tk.Button(frame, text="Start")
Start.grid(row=8, column=1, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)


Sic = Label(root, text="SIC").grid(row=0, column=1, sticky=W)
Pic = Label(frame1, text="PIC Rev : ").grid(row=2)
input_Pic = Entry(frame1).grid(row=2, column=1)
MiniDeck = Label(frame1, text="Mini-Dack Power : ").grid(row=3)
input_MD = Entry(frame1).grid(row=3, column=1)
Heater = Label(frame1, text="Heater : ").grid(row=4)
input_Heater = Entry(frame1).grid(row=4, column=1)
PMW = Label(frame1, text="PMW % : ").grid(row=5)
input_PMW = Entry(frame1).grid(row=5, column=1)
Part_num = Label(frame1, text="Part Number : ").grid(row=6)
input_Partnum = Entry(frame1).grid(row=6, column=1)
Serial_num = Label(frame1, text="Serial Number : ").grid(row=7)
input_Serialnum = Entry(frame1).grid(row=7, column=1)
T1 = Label(frame1, text="T1 : ").grid(row=8)
input_T1 = Entry(frame1).grid(row=8, column=1)
T2 = Label(frame1, text="T2 : ").grid(row=9)
input_T2 = Entry(frame1).grid(row=9, column=1)
Update = tk.Button(frame1, text="Update")
Update.grid(row=10, column=1, columnspan=1, sticky=W+E+N+S)

Label(frame1, text="Current").grid(row=2, column=2, columnspan=1)
current = Entry(frame1, width=10)
current.grid(row=3, column=2, columnspan=1)

Label(frame1, text="Step 1", relief=GROOVE).grid(row=2, column=3)
Label(frame1, text="  ").grid(row=3, column=3)
Label(frame1, text="  ").grid(row=3, column=5)
Label(frame1, text="Step 2", relief=GROOVE).grid(row=3, column=3)
Label(frame1, text="  ").grid(row=4, column=3)
Label(frame1, text="  ").grid(row=4, column=5)
Label(frame1, text="Step 3", relief=GROOVE).grid(row=4, column=3)
Label(frame1, text="  ").grid(row=5, column=3)
Label(frame1, text="  ").grid(row=5, column=5)
Label(frame1, text="Step 4", relief=GROOVE).grid(row=5, column=3)
Label(frame1, text="  ").grid(row=6, column=3)
Label(frame1, text="  ").grid(row=6, column=5)
Label(frame1, text="Step 5", relief=GROOVE).grid(row=6, column=3)

step1 = Button(frame1, text="Enter", width=10, command=delete)
step1.grid(row=2, column=4)
step2 = Button(frame1, text="Enter", width=10, command=delete)
step2.grid(row=3, column=4)
step3 = Button(frame1, text="Enter", width=10, command=delete)
step3.grid(row=4, column=4)
step4 = Button(frame1, text="Enter", width=10, command=delete)
step4.grid(row=5, column=4)
step5 = Button(frame1, text="Enter", width=10, command=delete)
step5.grid(row=6, column=4)
okButton = Button(frame1, text="OK", width=10)
okButton.grid(row=8, column=3, columnspan=1, sticky=W)
cancelButton = Button(frame1, text="Cancel", width=10, command=root.destroy)
cancelButton.grid(row=8, column=4, columnspan=2, sticky=W)


SerialP_num = Label(frame2, text="Serial/Part Number", relief=GROOVE).grid(row=9)
Label(frame2, text="Part Number : ").grid(row=10)
Label(frame2, text="Serial Number : ").grid(row=11)
E1 = Entry(frame2, width=20).grid(row=10, column=2)
E2 = Entry(frame2, width=20).grid(row=11, column=2)
Set = Button(frame2, text="SET", width=10)
Set.grid(row=12, column=0, columnspan=2, sticky=E)
Get = Button(frame2, text="GET", width=10)
Get.grid(row=12, column=1, columnspan=2, sticky=W)

PowerSupply = Label(frame3, text="Power Supply", relief=GROOVE).grid(row=0)
Label(frame3, text="Supply ID : ").grid(row=1)
tk.Label(frame3, text="Voltage").grid(row=2)
tk.Label(frame3, text="Current").grid(row=3)
tk.Label(frame3, text="Show").grid(row=4)
E1 = tk.Entry(frame3, width=20)
E2 = tk.Entry(frame3, width=20)
E1.grid(row=2, column=1)
E2.grid(row=3, column=1)
listbox = tk.Listbox(frame3, height=2)
vOUT = allOutput()
iOut = output_current()
listbox.insert(1, vOUT)
listbox.insert(2, iOut)
listbox.grid(row=4, column=1)
ON = tk.Button(frame3, text="ON", width=10, command=lambda: [
    input_volt(), input_current(), allOutput()])
ON.grid(row=5, column=0, columnspan=2, sticky=W)
OFF = tk.Button(frame3, text="OFF", width=10, command=lambda: [OFF_volt(), OFF_current()])
OFF.grid(row=5, column=1, columnspan=2, sticky=E)

print init_i2c()


root.mainloop()
