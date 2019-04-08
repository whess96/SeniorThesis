%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% calculateController.m
%
% Used to calculate the K matrix for the steady state flight.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%---------------------------------%
% Control Matrices
% States: x = [u, w, q, theta]
%           u = axial velocity
%           w = normal velocity
%           q = pitch rate
%           theta = pitch
%
% Controls: u = [delE]
%               delE = elevator deflection
%---------------------------------%
A = [[ -0.0737,   -0.008,     0,         -9.8 ]
     [  -0.1643,   -14.6592,   10.32,     0   ]
     [  0.1903,    -24.18,     23.8969,   0   ]
     [  0,         0,          1,         0   ]];
 
B = [ 0 -20.4468 -264.7649 0 ]';

C = eye(4);

D = 0;
 
%---------------------------------%
% LQR matrices
Q = [[1, 0, 0, 0]
     [0, 5, 0, 0]
     [0, 0, .1, 0]
     [0, 0, 0, .1]];

R = [1];

K = lqr(A, B, Q, R)
 