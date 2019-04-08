################################################################################
# csvLogger.py
#
# Logs the Vicon state values and the control inputs to a single csv file.
# Will overwrite file each time, so if we want to keep a run's data, need to 
# rename the file.
################################################################################

import lcm
import csv
import numpy as np
from planeDataT import viconState, controlCommands

#-------------------------------------------------------------------------------
# Constants
global states
states = [0] * 5
global comms
comms = [0] * 7
#-------------------------------------------------------------------------------
# Handler for reading state from LCM
def stateHandler(channel, data):
    global states
    msg = viconState.decode(data)
    x_dot = msg.velocity[1]
    z_dot = msg.velocity[2]
    theta = msg.angles[0]
    theta_dot = -msg.angularRates[0]
    
    u = x_dot*np.cos(theta) + z_dot*np.sin(theta)
    w = -x_dot*np.sin(theta) + z_dot*np.cos(theta)
    q = theta_dot

    states[0] = u
    states[1] = w
    states[2] = q
    states[3] = theta
    states[5] = msg.frame


# Handler for reading control commands from LCM
def controlHandler(channel, data):
    global comms
    msg = controlCommands.decode(data)
    comms = list(msg.channels).append(msg.frame)

with open('planeLogs.csv', 'w', newline='') as csvfile:
    csvWriter = csv.writer(csvfile, delimiter=',')
    header = ['Axis vel (u)', 'Norm vel (w)', 'Pitch Rate (q)', 'Pitch (theta)',
        'Frame', 'Chan 1', 'Chan 2', 'Chan 3', 'Chan 4', 'Chan 5', 'Chan 6', 
        'Frame'];    
    csvWriter.writerow(header)

    lcState = lcm.LCM()
    subState = lcState.subscribe("flightState", stateHandler)
    lcControl = lcm.LCM()
    subControl = lcControl.subscribe("controlCommands", controlHandler)

    try:
        while True:
            lcState.handle()
            lcControl.handle()
            csvWriter.writerow(state + comms)

    except KeyboardInterrupt:
        pass

    lcState.unsubscribe(subState)
    lcControl.unsubscribe(subControl)