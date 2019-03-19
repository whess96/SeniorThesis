################################################################################
# serial_writer.py
#
# Used to send control signal to Arduino via serial. Packs control output into 
# the range [0, 255] so each input can be sent over a single byte.
#
# Dependent on PySerial api to send data over serial port.
################################################################################

import sys, serial, struct
import lcm
from plane_data_t import arduino_pwm
from numpy import interp

################## Constants ####################
pack_start = 123    # Send across to indicate new packet
global comms_out
#################################################

comms_out = [0, 500, 500, 500, 500, 0]

# Packs the incomming data into the global varialbe channels_out
def my_handler(channel, data):
    global comms_out
    msg = arduino_pwm.decode(data)
    comms_out = list(msg.channels)

# Open up a serial port
with serial.Serial('/dev/cu.usbmodem14101', 9600) as ser:
    print(ser.name)
    ser.timeout = 50

    lc_in = lcm.LCM()
    lc_in.subscribe("PWM_COMMANDS", my_handler)

    while True:
        lc_in.handle()
        print(comms_out)
        # Indicate 'start of packet'
        ser.write(struct.pack('>B', pack_start))
        # Send across control commands as bytes
        for comm in comms_out:
            mapped_com = interp(comm, [0, 1000], [0, 255])
            ser.write(struct.pack('>B',int(mapped_com)))

    lc_in.unsubscribe()
