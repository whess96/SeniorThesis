################################################################################
# serialWriter.py
#
# Used to send control signal to Arduino via serial. Packs control output into 
# the range [0, 255] so each input can be sent over a single byte.
#
# Dependent on PySerial api to send data over serial port.
################################################################################

import sys, serial, struct
import lcm
from planeDataT import controlCommands
from numpy import interp

#-------------------------------------------------------------------------------
# Constants 
pack_start = 123    # Send across to indicate new packet
global comms_in
#-------------------------------------------------------------------------------

# Initial values for comms_in. Would result in a stopped plane.
comms_in = [0, 500, 500, 500, 500, 0]

# Packs the incomming data into the global varialbe comms_in
def my_handler(channel, data):
    print("Received message on channel \"%s\"" % channel)
    global comms_in
    msg = controlCommands.decode(data)
    comms_in = list(msg.channels)
    for i,comm in enumerate(comms_in):
        # Constrain the inputs to [0, 1000]
        if comm < 0:
            comms_in[i] = 0
        if comm > 1000:
            comms_in[i] = 1000

    print("     Channels: ", comms_in)

# Open up a serial port
with serial.Serial('/dev/cu.usbmodem14101', 9600) as ser:
    print(ser.name)
    ser.timeout = 50

    lc_in = lcm.LCM()
    lc_in.subscribe("controlCommands", my_handler)

    while True:
        lc_in.handle()
        # comms_in = (100, 200, 300, 400, 500, 600)
        print(comms_in)
        # Indicate 'start of packet'
        ser.write(struct.pack('>B', pack_start))
        # Send across control commands as bytes
        for comm in comms_in:
            mapped_com = interp(comm, [0, 1000], [0, 255])
            ser.write(struct.pack('>B',int(mapped_com)))

    lc_in.unsubscribe()
