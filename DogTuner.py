# An Adaptation of the EagleTuner from FRC 2073
# Needs python-tk and python-serial
# on windows CMD>pip2.7 install python-serial
# Tk is included with 2.7 by default
# Runs in python 2.7 

# On most machines this works. If you get a serial error try replacing the 3 with the serial port you see in the ardunio IDE
serdev = 'COM3' 

from Tkinter import *
import serial
import time


# default values 
errode = 1
dilate = 1
approx = 4      # Find Rectangles by default
area = 500
solidity = 100
ratio = 2   #Ratio of width to height for the target

####################################################################################################
# Send a command to JeVois and show response
def send_command(cmd):
    print "HOST>> " + cmd
    ser.write(cmd + '\n')
    out = ''
    time.sleep(0.1)
    while ser.inWaiting() > 0:
        out += ser.read(1)
    if out != '':
        print "JEVOIS>> " + out, # the final comma suppresses extra newline, since JeVois already sends one
    
####################################################################################################
def update_errode(val):
    global errode
    errode = val
    send_command('errode={0}'.format(errode))
    
####################################################################################################
def update_dilate(val):
    global dilate
    dilate = val
    send_command('dilate={0}'.format(dilate))
    
####################################################################################################
def update_approx(val):
    global approx
    approx = val
    send_command('approx={0}'.format(approx))
    
####################################################################################################
def update_area(val):
    global area
    area = val
    send_command('area={0}'.format(area))
    
####################################################################################################
def update_solidity(val):
    global solidity
    solidity = val
    send_command('solidity={0}'.format(solidity))
    
####################################################################################################
def update_ratio(val):
    global ratio
    ratio = val
    send_command('ratio={0}'.format(ratio))
    
####################################################################################################
# Main code
ser = serial.Serial(serdev, 115200, timeout=1)      #Default Jevois Values
send_command('ping')                   # should return ALIVE

master = Tk()
master.geometry('500x600')
master.config(bg="navy")
master.title("2085 Vision JeVois Tuner")


w1 = Label(master, text = "Errode", fg="white", bg="red3")
w2 = Scale(master, from_=0, to=20, tickinterval=4, length=600, width=16, orient=HORIZONTAL, command=update_errode)
w2.config(fg="black", bg="SlateBlue1", troughcolor="black", activebackground="red3")
w2.set(errode)

w3 = Label(master, text = "Dilate", fg="white", bg="red3")
w4 = Scale(master, from_=0, to=20, tickinterval=4, length=600, width=16, orient=HORIZONTAL, command=update_dilate)
w4.config(fg="black", bg="SlateBlue1", troughcolor="black", activebackground="red3")
w4.set(dilate)

w5 = Label(master, text = "Number of Sides", fg="white", bg="red3")
w6 = Scale(master, from_=0, to=25, tickinterval=5, length=600, width=16, orient=HORIZONTAL, command=update_approx)
w6.config(fg="black", bg="SlateBlue1", troughcolor="black", activebackground="red3")
w6.set(approx)

w7 = Label(master, text = "Area", fg="white", bg="red3")
w8 = Scale(master, from_=0, to=10000, tickinterval=1000, length=600, width=16, orient=HORIZONTAL, command=update_area)
w8.config(fg="black", bg="SlateBlue1", troughcolor="black", activebackground="red3")
w8.set(area)

w9 = Label(master, text = "Solidity", fg="white", bg="red3")
w10 = Scale(master, from_=0, to=100, tickinterval=20, length=600, width=16, orient=HORIZONTAL, command=update_solidity)
w10.config(fg="black", bg="grey", troughcolor="black", activebackground="red3")
w10.set(solidity)

w11 = Label(master, text = "Ratio", fg="white", bg="red3")
w12 = Scale(master, from_=0, to=6, tickinterval=1, resolution=0.1, length=600, width=16, orient=HORIZONTAL, command=update_ratio)
w12.config(fg="black", bg="grey", troughcolor="black", activebackground="red3")
w12.set(ratio)

w1.grid(row=0, column=0) #Errode
w2.grid(row=1, column=0)

w3.grid(row=2, column=0) #Dilate
w4.grid(row=3, column=0)

w5.grid(row=4, column=0) #Numbers of Sides
w6.grid(row=5, column=0)

w7.grid(row=6, column=0) #Area
w8.grid(row=7, column=0)

w9.grid(row=8, column=0)  #Solidity
w10.grid(row=9, column=0)

w11.grid(row=10, column=0)  #Ratio
w12.grid(row=11, column=0)


mainloop()
