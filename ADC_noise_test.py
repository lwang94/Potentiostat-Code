# -*- coding: utf-8 -*-
"""
@author: lawre

IMPORTANT: This code was written to test the noise of the ADC in the potentiostat described in 
Lawrence Wang's 2019 master's thesis submitted to the University of Toronto: TITLE.
The code assumes the circuit described in Chapter 3 has been built, the program 'python_communication.ino' (also
included in the thesis) has been uploaded to the board and the user has all the necessary software installed on their computer. 

The code as written will send the same DAC value to the circuit multiple times as specified by the user. The ADC value will be read 
each time and recorded into a file. This process is repeated for a series of DAC values as specified by the user. The result is a
series of files that records the variation in the ADC reading for the same DAC value.
"""

import numpy as np
import struct
import serial #you need to install the pySerial library from pyserial.sourceforge.net
import time
            
def ADC_noise_test():
    dac_value_initial=input('DAC Value Initial') #asks user to input the initial DAC value for the sweep (in bits)
    dac_value_final=input('DAC Value Final') #asks user to input the final DAC value for the sweep (in bits)
    dac_increment=input('DAC step size') #asks user to input the step size for the sweep (in bits)
    dac_list=np.arange(dac_value_initial, dac_value_final-1, dac_increment) #creates list of values for sweep
    
    num_counts=input('Number of Inputs') #asks user to input the number of times the same DAC value will be sent to the Arduino
    fname=raw_input('file path name') #asks user for the name of the file to save data to    
    start=time.time() #begins keeping track of time
    
    #Executes testing of ADC noise and records data
    for i in range(len(dac_list)):
        with open('%d_'%(dac_list[i])+fname, 'w+') as f: #begins writing to file
            f.write('#count, time, ADC, ADC Voltage\n') #headers for columns
            for j in range(num_counts):
                #Writing DAC value to Arduino
                dac_value=struct.pack('>h', dac_list[i]) #converts DAC value inputs from integer type to byte type
                arduino.write(dac_value) #sends DAC value to Arduino (presumably the file 'python_communication.ino' has been uploaded to the Arduino)
                
                #Keep track of the progress
                print dac_list[i], ':', j 
                
                #Read ADC value from Arduino and record time
                value=struct.unpack('>h', arduino.read(2))[0] #reads two bytes from Arduino (presumably the file 'python_communication.ino' has been uploaded to the Arduino)
                end=time.time() #records time
                
                #Write data to file
                f.write('%d, %f, %d, %f\n'%(j, end-start, value, (value*-0.000062636)+0.0005))
                time.sleep(0.03) #pauses the program between each measurement

arduino = serial.Serial('COM6', 9600) #connects Python to the serial port         
time.sleep(2) #pauses the program after connecting Python to serial port
ADC_noise_test() #executes ADC_noise_test function
serial.Serial()