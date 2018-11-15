# 10/27 Meeting with Rowley

* Tradeoffs with using VICON
    * Have to figure out how to send control from the computer to the plane
    * Want not to have latency
    * Probably should just build our own transmitter that the computer should control
* Building our own transmitter
    * Try a bunch of options and choose the one with minimal latency
    * Ways to measure latency:
        1) Put a marker on a control surface.
        2) Put step input to this control surface.
        3) See how long it takes for the vicon system to notice.
        4) Look for one that has latency < 50ms
* LCM
    * Figure out how we're going to learn how to use vicon system. 
    * Probably going to be a grad system
    * Helps your program read from the vicon system and convert it nicely to messages that can be interpreted by other programs.
    * Allows for communication over local network. (Don't need serial com)
    * Really good for separation of concerns
        * Helpful for logging the data

## Todo
Try to order hardware before break
Deliverables: info on transmitter, getting basic information back from Vicon (position of one marker), be able to measure latency based on a tracking marker.