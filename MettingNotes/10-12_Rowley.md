# 10/12 Meeting with Rowley
1. Quick overview of what we wrote

2. How can we accomplish it within a year
    * Thesis worthy?
        - Yes. Maybe want to think about what actual changes we want to do that handicap the wing without being too dramatic. Start simple.

3. What physical things do we need to buy?

4. What software should we be looking into? How will the controls work?
    * Have to figure out how to switch on the autopilot.
    * Have to figure out how to curve fit to the existing data, just because we don't really know all of the parameters.
    * numpy, python control systems library, scipy for signal processing

5. projected time scale? milestones?
    * Disable one of the control surfaces (elevator, aileron, etc.) Not just control, but also jam.
    * Wouldn't take a lot of mechanical adjustment.
    * Options with how to approach this:
        1. Have 2 different models. One with normal dynamics, one with dynamics of broken airplane. Detect something is wrong midflight and switch.
        2. Have the plane realize something is wrong and try to figure out how to compensate with damage on the fly.
        3. some kind of combination?
    * Really try to see what we can do with our sensors/pixHawk and with the plane.

    * Steps:
        1. Figure out what we can know from time to time.
        2. Just figure out how to do autopilot we the uninjured aircraft.
            Take measurements early so we can get a really solid analysis of the plane model.
        3. How does the PixHawk work? Have computer fly the plane potentially? Trainer port kind of works, but there's an unfortunate delay.
        4. Make some aerodynamic models of the aircraft.
        5. Take a model of longitudinal dynamics. Try to fit the parameters to the known flight data. Thrust, elevator, and see how it effects the altitude.
        6. Try to back out the flight parameters from existing flight data.
            Start adding noise and disturbances from the model and see what we can do to keep it robust. 

6. Weekly meeting time.


## General Notes

PixelHawk microprocessor

Figure out where we should fly it
    Potentially fields across Lake Carnegie
    Be sure to read the sUAS policies carefully. 
    drones@princeton.edu

See if they list the maximum payload of the plane. Make sure it can support our sensor system. 

Things we need to do now:
    Talk to Ani about hardware concerns.
        What plane
        How do we communicate with it
            On plane or on ground control
    Learn about how to control the plane
        PixHawk

Programming/Controls:
    Can try to get an average xdot at some point to try to get rid of noise.
    Do a linear fitting.
    Maybe even do some discrete models.
    Start with: $a = (xdot_ave - u_ave)/x_ave$
