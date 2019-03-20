################################################################################
# produce_test_data.py
#
# Produces test data to test out the code. "Simulates" flying the plane.
################################################################################

import lcm
import time
from plane_data_t import vicon_state

flight_state = vicon_state()

# Fake test data
flight_state.position = (1.0, 1.0, 1.0)
flight_state.angles = (2.0, 2.0, 2.0)
flight_state.velocity = (3.0, 3.0, 3.0)
flight_state.angular_rates = (4.0, 4.0, 4.0)

lc = lcm.LCM()

while True:
    lc.publish("FLIGHT_STATE", flight_state.encode())
    time.sleep(1)