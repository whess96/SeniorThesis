#################################################################
# controller.py
#
# Takes in the raw position and rotation data over lcm. Performs 
# necessary control calculations using a physics based control 
# matrix. Publishes the resulting control vector to a new lcm 
# channel.
#################################################################

import lcm
import time
import numpy as np
from planeDataT import viconState, controlCommands, controlState

#----------------------------------------------------------------
# Constants & Global Variables
global state_in  # global way to read in states: [u, w, q, theta]
state_in = [0]*4

# K control matrix (Physics based)
K = [0.0397, 0.0583, -0.1869, -0.5411]
#----------------------------------------------------------------

# Called by lc_in.handle(). Fills state_in array with appropriate
# values.
def my_handler(channel, data):
    global state_in
    msg = viconState.decode(data)
    x_dot = msg.velocity[1]
    z_dot = msg.velocity[2]
    theta = msg.angles[0]
    theta_dot = msg.angularRates[0]
    
    u = x_dot*np.cos(theta) + z_dot*np.sin(theta)
    w = -x_dot*np.sin(theta) + z_dot*np.cos(theta)
    q = theta_dot

    state_in[0] = u
    state_in[1] = w
    state_in[2] = q
    state_in[3] = theta

# Apply control matrix K and map the new values to PWM [0,1000]
def stateToPWM():
    u = -np.matmul(K, state_in)

    thrust = 600
    ail = 520
    elev = np.interp(u, [np.radians(-19), np.radians(19)], 
        [0,1000])
    rudd = 540
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

        # Publish the states for the sole purpose of logging the 
        # data
        stateLog = controlState()
        stateLog.states = state_in
        stateLog.timestamp = int(time.time()*1e6)
        lc_out.publish("controlState", stateLog.encode())
except KeyboardInterrupt:
    pass

lc_in.unsubscribe(subscription)