%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% calculate_controller.m
%
% Used to calculate the K matrix for the steady state flight.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

A = [[ -0.0737,   -0.008,     0,         -9.8 ]
     [  -0.1643,   -14.6592,   10.32,     0   ]
     [  0.1903,    -24.18,     23.8969,   0   ]
     [  0,         0,          1,         0   ]];
 
B = [[ 0,          1 ]
     [ -20.4468,   1 ]
     [ -264.7649,  1 ]
     [ 0,          0 ]];

 