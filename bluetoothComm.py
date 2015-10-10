import serial
import json

blSerial=serial.Serial("/dev/rfcomm1",baudrate=9600)
while 1:
    print "Seeking data"
    data = blSerial.readline()
    if data:
        print data
        blSerial.write( str("TO") )


        
    
