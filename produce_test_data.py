################################################################################
# produce_test_data.py
#
# Produces test data to test out the code. "Simulates" flying the plane.
################################################################################

import lcm
import time
from planeDataT import viconState

flightState = viconState()

# Fake test data
flightState.position = (1.0, 1.0, 1.0)
flightState.angles = (2.0, 2.0, 2.0)
flightState.velocity = (3.0, 3.0, 3.0)
flightState.angular_rates = (4.0, 4.0, 4.0)

lc = lcm.LCM()

while True:
    lc.publish("FLIGHTSTATE", flightState.encode())
    time.sleep(1)
