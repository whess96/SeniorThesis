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
 
% A = [[  -0.0737,   -0.008,     0,         -9.8 ]
%      [  -0.1643,   -14.6592,   10.32,     0    ]
%      [  0.1903,    -24.18,     23.8969,   0    ]
%      [  0,         0,          1,         0    ]];
% 
% B = [[  0        ] 
%      [ -20.4468  ]
%      [ -264.7649 ]
%      [  0        ]];

% Ouimet Physics based model
A = [[  -0.2818,  -0.3757,   0,       -9.8]
     [  -0.7045,  -12.307,   26.826,  0   ]
     [  -0.1154,  -2.063,    0.386,   0   ]
     [  0,        0,         1,       0   ]];
    
B = [0, 0, 0, -13.74]';

% Estmated States
% A =[
% 
%     1.0032   -0.0004    0.0051    0.0006   -0.0005
%     3.0080    0.2672    0.2561    0.1749    0.2100
%     0.3865   -0.0514    0.6119    0.0688   -0.0575
%    -0.2365    0.0095   -0.0357    0.8203    0.0410
%     0.1873   -0.0915   -0.5806   -0.1667    0.0685];
% 
% 
% B = [
% 
%     0.0000
%    -0.0231
%     0.0057
%    -0.0082
%    -0.0262];

 
%---------------------------------%
% LQR matrices
Q = [[1, 0, 0, 0]
     [0, 10, 0, 0]
     [0, 0, 1, 0]
     [0, 0, 0, 100]];
% Q = [10 0 0 0 0
%      0 .1 0 0 0
%      0 0 1 0 0
%      0 0 0 1 0
%      0 0 0 0 1];

R = 100;

K = lqr(A, B, Q, R)
 