################################################################################
# controller.py
#
# Takes in the raw (or observer) state date about the aircraft's position over
# lcm. Publishes the resulting control vector to a new lcm channel.
################################################################################

import lcm
import numpy as np
from plane_data_t import vicon_state, control_commands

#-------------------------------------------------------------------------------
# Constants
global state_in  # global way to read in states: [u, w, q, theta]
state_in = [0]*4
# A state space matrix
A = [[ -0.0737,   -0.008,     0,         -9.8 ],
     [  -0.1643,   -14.6592,   10.32,     0   ],
     [  0.1903,    -24.18,     23.8969,   0   ],
     [  0,         0,          1,         0   ]]
# B state space matrix (fake numbers)
B = [[ 0,          1 ],
     [ -20.4468,   1 ],
     [ -264.7649,  1 ],
     [ 0,          0 ]]

# K control matrix (fake numbers)
K = [[ 1, 0, 0, 0],
     [ 0, 1, 0, 0],
     [ 0, 0, 1, 0],
     [ 0, 0, 0, 1],
     [ 1, 0, 0, 0],
     [ 0, 1, 0, 0]]
#-------------------------------------------------------------------------------

# Called by lc_in.handle(). Fills state_in array with appropriate values.
def my_handler(channel, data):
    print("Received message on channel \"%s\"" % channel)
    global state_in
    msg = vicon_state.decode(data)
    state_in[0] = msg.velocity[0]
    state_in[1] = msg.velocity[1]
    state_in[2] = msg.angular_rates[0]
    state_in[3] = msg.angles[0]

lc_in = lcm.LCM()
subscription = lc_in.subscribe("FLIGHT_STATE", my_handler)

lc_out = lcm.LCM()

# Continuously listen for new data. For each new package, run the controller
# calculations and publish the result.
try:
    while True:
        lc_in.handle()
        output = control_commands()
        # output.channels = np.matmul(K,state_in)
        
        output.channels = (0, 250, 500, 750, 333, 666) # Fake test data
        lc_out.publish("CONTROL_COMMANDS", output.encode())
except KeyboardInterrupt:
    pass

lc_in.unsubscribe(subscription)