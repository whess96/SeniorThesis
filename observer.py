################################################################################
# observer.py
#
# Takes in the raw output from the vicon system as well as controller output
# to make an estimated state. This state estimate is then fed into the 
# controller. 
################################################################################

import lcm
import numpy as np
from plane_data_t import vicon_state

global state_in

def y_handler(channel, data):
    pass

def u_handler(channel, data):
    pass

lc_y = lcm.LCM()
subscription_y = lc_y.subscribe("FLIGHT_STATE", y_handler)
lc_u = lcm.LCM()
subscription_u = lc_u.subscribe("CONTROL_COMMANDS", u_handler)

try:
    while True:
        lc_y.handle()
        lc_u.handle()
except KeyboardInterrupt:
    pass

lc_y.unsubscribe(subscription_y)
lc_u.unsubscribe(subscription_u)
