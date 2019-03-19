################################################################################
# controller.py
#
# Takes in the raw (or observer) state date about the aircraft's position over
# lcm. Publishes the resulting control vector to a new lcm channel.
#
################################################################################

import lcm
import numpy as np
from plane_data_t import vicon_state, arduino_pwm

# Executes upon call of "lc_in.handle()"
def my_handler(channel, data):
    msg = vicon_state.decode(data)
    print("Received message on channel \"%s\"" % channel)
    # print("     position: %s" % (str(msg.position)))
    # print("     angles: %s" %(str(msg.angles)))
    # print("     velocity: %s" %(str(msg.velocity)))
    # print("     angular rates: %s" %(str(msg.angular_rates)))
    # print()

lc_in = lcm.LCM()
subscription = lc_in.subscribe("FLIGHT_STATE", my_handler)

lc_out = lcm.LCM()

# Continuously listen for new data. For each new package, run the controller
# calculations and publish the result.
try:
    while True:
        state = lc_in.handle()
        output = arduino_pwm()
        # Fake test data
        output.channels = (0, 250, 500, 750, 333, 666)
        lc_out.publish("PWM_COMMANDS", output.encode())
except KeyboardInterrupt:
    pass

lc_in.unsubscribe(subscription)