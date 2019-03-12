import sys
import serial
import struct
from numpy import interp

# Open up a serial port
with serial.Serial('/dev/cu.usbmodem14101', 9600) as ser:
    print(ser.name)
    ser.timeout = 50

    while True:
        # Use first element as a detector for lost packets
        # u = [int(interp(int(input("Channel " + str(i) + ": \n")), [0, 1000], [0, 255]))
        #     for i in range(1,7)]
        u = interp([0, 250, 500, 750, 333, 666], [0, 1000], [0, 255])
        ser.write(struct.pack('>B', 123))
        for comm in u:
            ser.write(struct.pack('>B',int(comm)))
