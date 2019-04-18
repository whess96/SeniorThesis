################################################################################
# controller.py
#
# Takes in the raw (or observer) state date about the aircraft's position over
# lcm. Publishes the resulting control vector to a new lcm channel.
################################################################################

import lcm
import time
import numpy as np
from planeDataT import viconState, controlCommands, controlState

#-------------------------------------------------------------------------------
# Constants & Global Variables
global state_in  # global way to read in states: [u, w, q, theta]
state_in = [0]*4

# K control matrix
# K = [[ 1, 0, 0, 0],
#      [ 0, 1, 0, 0]]
K = [  -0.1909,    8.3840,    0.8895,    4.7545]
# K = [0, 0, 0, 4]
#-------------------------------------------------------------------------------

# Called by lc_in.handle(). Fills state_in array with appropriate values.
def my_handler(channel, data):
    # print("Received message on channel \"%s\"" % channel)
    global state_in
    msg = viconState.decode(data)
    x_dot = msg.velocity[1]
    z_dot = msg.velocity[2]
    theta = msg.angles[0]
    theta_dot = -msg.angularRates[0]
    
    u = -x_dot*np.cos(theta) + z_dot*np.sin(theta)
    w = x_dot*np.sin(theta) + z_dot*np.cos(theta)
    q = theta_dot

    # print("     Axis velocity (u):   ", u)
    # print("     Normal velocity (w): ", w)
    # print("     Pitch rate (q) :     ", q)
    # print("     Pitch angle (theta): ", theta)
    # print()

    state_in[0] = u
    state_in[1] = w
    state_in[2] = q
    state_in[3] = theta

# Apply control matrix K and map the new values to PWM [0,1000]
def stateToPWM():
    u = np.matmul(K, state_in)

    thrust = 450
    ail = 550
    elev = np.interp(u, [np.radians(-100), np.radians(100)], [0,1000])
    # elev = 500
    rudd = 600
    flap = 0

    return (thrust, ail, elev, rudd, 0, flap)

# Set up LCM, including the log
# log = lcm.EventLog('LCM_log', 'w', overwrite=True)

lc_in = lcm.LCM()
subscription = lc_in.subscribe("flightState", my_handler)

lc_out = lcm.LCM()

# Continuously listen for new data. For each new package, run the controller
# calculations and publish the result.
try:
    while True:
        lc_in.handle()
        output = controlCommands()   
        output.channels = stateToPWM()
        output.controls = np.matmul(K, state_in)
        output.timestamp = int(time.time()*1e6)
        # output.channels = (0, 500, 500, 500, 500, 0) # Fake test data
        lc_out.publish("controlCommands", output.encode())

        stateLog = controlState()
        stateLog.states = state_in
        stateLog.timestamp = int(time.time()*1e6)
        lc_out.publish("controlState", stateLog.encode())
except KeyboardInterrupt:
    pass

lc_in.unsubscribe(subscription)