################################################################################
# writeLogs.py
#
# Write all open LCM channels to a file called flightData.log. This can later be read
# using readLogs.py.
################################################################################
import lcm
import time
from planeDataT import viconState, controlCommands, controlState

#-------------------------------------------------------------------------------
# Global variables
global log
#-------------------------------------------------------------------------------

# Write the incoming data to the shared log
def my_handler(channel, data):
    global log
    log.write_event(int(time.time()*1e6), channel, data)

# Set up LCM, including the log
log = lcm.EventLog('flightData.log', 'w', overwrite=True)

lc1 = lcm.LCM()
sub1 = lc1.subscribe("flightState", my_handler)
lc2 = lcm.LCM()
sub2 = lc2.subscribe("controlCommands", my_handler)
lc3 = lcm.LCM()
sub3 = lc3. subscribe("controlState", my_handler)

try:
    while True:
        lc1.handle()
        lc2.handle()
        lc3.handle()
except KeyboardInterrupt:
    pass

sub1.unsubscribe(sub1)
sub2.unsubscribe(sub2)
sub3.unsubscribe(sub3)