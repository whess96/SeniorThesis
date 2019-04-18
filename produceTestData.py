################################################################################
# produceTestData.py
#
# Produces test data to test out the code. "Simulates" flying the plane.
################################################################################

import lcm
import time, sys
from planeDataT import viconState, controlCommands

flightState = viconState()
controlCommands = controlCommands()

lc1 = lcm.LCM()
lc2 = lcm.LCM()

while True:
    # Fake test data
    flightState.position = (1.0, 1.0, 1.0)
    flightState.angles = (2.0, 2.0, 2.0)
    flightState.velocity = (3.0, 3.0, 3.0)
    flightState.angularRates = (4.0, 4.0, 4.0)
    flightState.timestamp = int(time.time()*1e6)

    # controlCommands.channels = (100, 200, 300, 400, 500, 600)
    
    lc1.publish("flightState", flightState.encode())
    # lc2.publish("controlCommands", controlCommands.encode())
    time.sleep(0.2)