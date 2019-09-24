import Tkinter as tk
from Tkinter import *
import mpsse_connect as mp
import numpy as np
import ttk
import serial
import pprint
import tkMessageBox
import serial.tools.list_ports
import struct
# import ctypes
import time
ports = list(serial.tools.list_ports.comports())
portArr = []
for p in ports:
    print p
    portBeforSub = p
    portIn = str(portBeforSub)
    if portIn[7] == "'":
        portIn = portIn[2:7]
    else:
        portIn = portIn[2:6]
    portArr.append(portIn)
    for x in portArr:
        print(x)
set_baudrate = 9600
set_timeout = 1
port = portArr[0]
portValues = portArr[:]


def read_partnumber():
    mp.init_i2c()
    mp.i2c_write(0x55, [0x80])
    partnumber = mp.i2c_read8bytes(0x55)
    print partnumber
    # print mp.i2c_read8bytes(0x55)
    partNum = Entry(frame2)
    partNum.insert(1, partnumber)
    partNum.grid(row=10, column=2)
    mp.close_i2c()
    return(partnumber)


def write_partnumber(partnumber="00000000"):
    pn = partNum.get()
    print("########################")
    print pn
    print("########################")
    ord_partnumber = list(map(ord, pn.strip()))
    print("########################")
    print ord_partnumber
    print("########################")
    reg = [0x80]
    writeout_to_reg = reg+ord_partnumber
    print writeout_to_reg

    ret = mp.i2c_write(0x55, writeout_to_reg)
    return(ret)

# def write_partnumber(partnumber="0x00"):
#     ord_partnumber = list(map(ord, partnumber.strip()))
#     print("#####################")
#     print ord_partnumber
#     print("#####################")
#     reg = [0x80]
#     writeout_to_reg = reg+ord_partnumber
#     print writeout_to_reg
#     ret = mp.i2c_write(0x55, writeout_to_reg)
#     print("#############")
#     print ret
#     return(ret)
# def write_partnumber():
#     mp.init_i2c()
#     mp.i2c_write(0x55, [0x80])
#     deckstatus = mp.i2c_read(0x55)
#     mp.close_i2c()
#     return deckstatus.encode('hex')


def read_partnumber1():
    mp.init_i2c()
    mp.i2c_write(0x55, [0x80])
    partnumber = mp.i2c_read8bytes(0x55)
    # print mp.i2c_read8bytes(0x55)
    part_Num = Entry(frame1)
    part_Num.insert(1, partnumber)
    part_Num.grid(row=6, column=1)
    mp.close_i2c()
    return(partnumber)


def read_serialnumber():
    mp.init_i2c()
    mp.i2c_write(0x55, [0x82])
    serialnumber = mp.i2c_read8bytes(0x55)
    serialNum = Entry(frame2)
    serialNum.insert(1, serialnumber)
    serialNum.grid(row=11, column=2)
    mp.close_i2c()
    return(serialnumber)


def read_serialnumber1():
    mp.init_i2c()
    mp.i2c_write(0x55, [0x82])
    serialnumber = mp.i2c_read8bytes(0x55)
    serialNum = Entry(frame1)
    serialNum.insert(1, serialnumber)
    serialNum.grid(row=7, column=1)
    mp.close_i2c()
    return(serialnumber)


def read_deckstatus():
    mp.init_i2c()
    mp.i2c_write(0x55, [0x05])
    deckstatus = mp.i2c_read(0x55)

    if not(deckstatus):
        deckstatus = struct.pack('1B', 0x00)
    mp.close_i2c()
    return deckstatus.encode('hex')


def write_deckstatus(status=0x00):
    mp.init_i2c()
    mp.i2c_write(0x55, [0x05, status])
    deckstatus = mp.i2c_read(0x55)
    mp.close_i2c()
    return deckstatus.encode('hex')


def read_statusheater():
    mp.init_i2c()
    mp.i2c_write(0x55, [0x07])
    heaterstatus = mp.i2c_read(0x55, 1)
    input_Heater = Listbox(frame1, height=1)
    input_Heater.insert(1, heaterstatus)
    input_Heater.grid(row=4, column=1)
    print heaterstatus
    mp.close_i2c()

    return (heaterstatus)


def read_heater_status():  # need to check with designer what are in reg 8? cause 97% reg7 showed 248
    mp.i2c_write(0x55, [0x06])
    reg6 = mp.i2c_read(0x55)
    if reg6:
        heater_status = 'ON'
    else:
        heater_status = 'OFF'

    mp.i2c_write(0x55, [0x07])
    reg7 = mp.i2c_read(0x55)
    if not(reg7):
        reg7 = struct.pack('1B', 0x00)

    print struct.unpack('1B', reg7)[0]

    # +0.5 for rounding process only.
    pwm_percent = int(((struct.unpack('1B', reg7)[0]/256.0)*100.0)+0.5)

   # print 'Heater Status:[',heater_status ,']  heaterPWM = ',pwm_percent,'%'
    return heater_status, pwm_percent


def read_temp():
    mp.init_i2c()
    mp.i2c_write(0x55, [0x24, 0x25])
    temp = mp.i2c_read8bytes(0x55)
    print temp
    # print mp.i2c_read8bytes(0x55)
    temp1 = Entry(frame1)
    temp1.insert(1, temp)
    temp1.grid(row=8, column=1)
    temp2 = Entry(frame1)
    temp2.insert(1, temp)
    temp2.grid(row=9, column=1)

    mp.close_i2c()
    temerature = int(((struct.unpack('1B', temp1)[0]/256.0)*100.0)+0.5)
    return(temp)


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
root.geometry('900x600')
number = tk.StringVar()

mp.init_i2c()
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
E1 = Entry(frame, width=20).grid(row=3, column=1)
E2 = Entry(frame, width=20).grid(row=4, column=1)
OC_loop = Label(frame, text="Delay After (ms)", relief=GROOVE).grid(row=5)
Label(frame, text="Open(ms) : ").grid(row=6)
Label(frame, text="Close(ms) : ").grid(row=7)
E1 = Entry(frame, width=20).grid(row=6, column=1)
E2 = Entry(frame, width=20).grid(row=7, column=1)
Start = tk.Button(frame, text="Start")
Start.grid(row=8, column=1, columnspan=1, sticky=W+E+N+S)


Sic = Label(root, text="SIC").grid(row=0, column=1, sticky=W)
Pic = Label(frame1, text="PIC Rev : ").grid(row=2)
input_Pic = Listbox(frame1, height=1).grid(row=2, column=1)
MiniDeck = Label(frame1, text="Mini-Deck Power : ").grid(row=3)
input_MD = Listbox(frame1, height=1).grid(row=3, column=1)
Heater = Label(frame1, text="Heater : ").grid(row=4)
input_Heater = Listbox(frame1, height=1).grid(row=4, column=1)
PMW = Label(frame1, text="PMW % : ").grid(row=5)
input_PMW = Listbox(frame1, height=1).grid(row=5, column=1)
Part_num = Label(frame1, text="Part Number : ").grid(row=6)
input_Partnum = Listbox(frame1, height=1).grid(row=6, column=1)
Serial_num = Label(frame1, text="Serial Number : ").grid(row=7)
input_Serialnum = Listbox(frame1, height=1).grid(row=7, column=1)
T1 = Label(frame1, text="T1 : ").grid(row=8)
input_T1 = Listbox(frame1, height=1).grid(row=8, column=1)
T2 = Label(frame1, text="T2 : ").grid(row=9)
input_T2 = Listbox(frame1, height=1).grid(row=9, column=1)
Update = tk.Button(frame1, text="Update", command=lambda: [
    read_statusheater(), read_partnumber1(), read_serialnumber1(), read_temp()])
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
partNum = Entry(frame2)
partNum.grid(row=10, column=2)
serialNum = Entry(frame2)
serialNum.grid(row=11, column=2)
Set = Button(frame2, text="SET", width=10, command=write_partnumber)
Set.grid(row=12, column=0, columnspan=2, sticky=E)
Get = Button(frame2, text="GET", width=10, command=lambda: [read_partnumber(), read_serialnumber()])
Get.grid(row=12, column=1, columnspan=2, sticky=W)

PowerSupply = Label(frame3, text="Power Supply", relief=GROOVE).grid(row=0)
# comboExample = ttk.Combobox(frame3, values=portValues)
# comboExample.grid(row=0, column=1, columnspan=1, sticky=W+E+N+S)
Label(frame3, text="Supply ID : ").grid(row=1)
tk.Label(frame3, text="Voltage").grid(row=2)
tk.Label(frame3, text="Current").grid(row=3)
tk.Label(frame3, text="Show").grid(row=4)
E1 = tk.Entry(frame3, width=20)
E2 = tk.Entry(frame3, width=20)
E1.grid(row=2, column=1)
E2.grid(row=3, column=1)
listbox = tk.Listbox(frame3, height=2)
# vOUT = allOutput()
# iOut = output_current()
# listbox.insert(1, vOUT)
# listbox.insert(2, iOut)
listbox.grid(row=4, column=1)
ON = tk.Button(frame3, text="ON", width=10, command=lambda: [
    input_volt(), input_current(), allOutput()])
ON.grid(row=5, column=0, columnspan=2, sticky=W)
OFF = tk.Button(frame3, text="OFF", width=10, command=lambda: [OFF_volt(), OFF_current()])
OFF.grid(row=5, column=1, columnspan=2, sticky=E)

# read_deckstatus()
# mp.i2c_write(0x55, [0x05])
# deckstatus = mp.i2c_read(0x55)
# print deckstatus

# read_partnumber()

mp.close_i2c()

root.mainloop()
