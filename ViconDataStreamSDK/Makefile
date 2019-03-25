# Simple makefile for compiling the Vicon SDK so I don't have to remember the compilaiton command.

all: test planedata

test: ViconDataStreamSDK_CPPTest.cpp 
	g++ ViconDataStreamSDK_CPPTest.cpp -o test -lViconDataStreamSDK_CPP

planedata: streamPlaneState.cpp
	g++ streamPlaneState.cpp -o streamPlaneData -lViconDataStreamSDK_CPP
