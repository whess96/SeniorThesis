#################################################################
# controllerEstimate.py
#
# Takes in the raw position and rotation data over lcm. Performs 
# necessary control calculations using a data based control 
# matrix. Publishes the resulting control vector to a new lcm 
# channel.
#################################################################

import lcm
import time
import numpy as np
from planeDataT import viconState, controlCommands, controlState
#----------------------------------------------------------------
# Constants & Global Variables
# global way to read in states: [z, x_d, z_d, theta, theta_d]
global state_in  
state_in = [0]*5

# K control matrix (Data based)
K = [2.3309,   -0.0031,    0.0343,    0.0396,   -0.0024]
#----------------------------------------------------------------

# Called by lc_in.handle(). Fills state_in array with appropriate
# values.
def my_handler(channel, data):
    global state_in
    msg = viconState.decode(data)

    state_in[0] = msg.position[2] - 1.4
    state_in[1] = msg.velocity[1]
    state_in[2] = msg.velocity[2]
    state_in[3] = msg.angles[0]
    state_in[4] = msg.angularRates[0]

# Apply control matrix K and map the new values to PWM [0,1000]
def stateToPWM():
    u = -np.matmul(K, state_in)

    thrust = 500
    ail = 500
    elev = np.interp(u, [np.radians(-19), np.radians(19)], 
        [0,1000])
    rudd = 580
    flap = 0

    return (thrust, ail, elev, rudd, 0, flap)

# Set up LCM
lc_in = lcm.LCM()
subscription = lc_in.subscribe("flightState", my_handler)

lc_out = lcm.LCM()

# Continuously listen for new data. For each new package, run the
# controller calculations and publish the result.
try:
    while True:
        lc_in.handle()
        output = controlCommands()   
        output.channels = stateToPWM()
        output.controlCalc = -np.matmul(K, state_in)
        output.controlAngle = np.interp(output.channels[2],
            [0, 1000], [-19, 19])
        output.timestamp = int(time.time()*1e6)
        lc_out.publish("controlCommands", output.encode())
except KeyboardInterrupt:
    pass

lc_in.unsubscribe(subscription)