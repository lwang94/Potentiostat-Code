# -*- coding: utf-8 -*-
"""
@author: lawre
IMPORTANT: This code was written to perform a Current vs time measurement using the potentiostat described in 
Lawrence Wang's 2019 master's thesis submitted to the University of Toronto: TITLE.
The code assumes the circuit described in Chapter 3 has been built, the program 'python_communication.ino' (also
included in the thesis) has been uploaded to the board and the user has all the necessary software installed on their computer. 

"""

import numpy as np
import struct
import serial # you need to install the pySerial :pyserial.sourceforge.net
import time

def It_measurement():
    #Inputs
    dac_value=input('DAC Value') #input for the DAC value (in bits)
#    dac_voltage=raw_input('DAC Voltage') #input for the DAC (in volts)
    fname=raw_input('File Name') #input for the file name
    wait_time=input('Wait Time (s)') #input for the wait time
    scan_rate=input('Scan Rate (s-1)') #input for the scan rate. NOTE: timing from Python is still off sometimes so not completely accurate
    run_time=input('Run Time (s)') #input for the run time
    
    #Converts DAC voltage to a value in bits
#    dac_value=(2.5475-(float(dac_voltage)/4.0696)+0.0066426)(4096/5.0655)
#    dac_value=int(dac_value)
    
    #Converts dac_value from integer type to bit type
    dac_value=struct.pack('>h', dac_value)
    
    #Write data to file
    with open(fname, 'w+') as f: #create file in write mode
        f.write('#count, time (s), ADC, Current (microA)\n') #put in headers
        
        #wait before recording data
        arduino.write(dac_value) #write dac_value to Arduino to bring system to applied potential
        arduino.read(2) #read ADC value to remove it from serial port but don't record it
        time.sleep(wait_time) #waits the specified waiting time
        
        #execute I-t measurement
        start=time.time() #begins keeping track of time
        end=time.time() #records time (will be 0 at first so the following while loop can work)
        i=0 #keeps track of the iteration of the measurement
        while (end-start)<run_time: #while the time recorded is less than the run time, continuing executing the loop
            #Writing DAC value to Arduino
            arduino.write(dac_value) #sends DAC value to Arduino (presumably the file 'python_communication.ino' has been uploaded to the Arduino)
            end=time.time() #records time
            i+=1 #records iteration
            
            #keep track of the progress
            print end-start
            
            #Read ADC value from Arduino and writes data to file
            value=struct.unpack('>h', arduino.read(2))[0] #reads two bytes from Arduino (presumably the file 'python_communication.ino' has been uploaded to the Arduino)
            f.write('%d, %f, %d, f\n'%(i, end-start, value, (value*-0.000062636+0.0005)*500)) #writes data to file
            time.sleep(1.0/float(scan_rate)) #pauses the program to be in line with scan rate

arduino = serial.Serial('COM6', 9600) #connects Python to the serial port   
time.sleep(2) #pauses the program after connecting Python to the serial port
It_measurement() #executes It_measurement function
print 'UNPLUG INSTRUMENT WHEN SWITCHING ELECTRODES' #prints warning message to ensure working electrode and auxiliary electrode are not connected in solution with an active potential (causes ITO to blacken)
serial.Serial() 