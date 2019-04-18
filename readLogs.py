################################################################################
# readLogs.py
#
# Reads the LCM EventLogs.
################################################################################

import lcm
from sys import argv
from datetime import datetime
from planeDataT import viconState, controlCommands, controlState

import numpy as np
from bokeh.plotting import figure, output_file, show
import csv

# Remove occlusion noise from data by setting 0 values to previous values.
def removeOcclusionNoise(data):
    for (i,val) in enumerate(data):
        if val == 0 and i > 0:
            data[i] = data[i-1]
    return data

# Write the data to a csv. data is a 2D list where each lower level list is a 
# column of data. 
def writeCsv(data, filename):
    with open(filename, 'w') as destination:
        csvWriter = csv.writer(destination, delimiter=',')
        newRow = len(data)*[0]
        for i in range(len(data[0])):
            for j in range(len(data)):
                newRow[j] = data[j][i]
            csvWriter.writerow(newRow)

# Plots the data in bokeh
def plotFig(x, y, filename, yaxis, xaxis="Time (s)", title=""):
    output_file = "filename"
    fig = figure(x_axis_label=xaxis, y_axis_label=yaxis,
        title=title)
    fig.line(x,y,line_width=2)
    fig.xaxis.major_label_orientation = np.pi/2
    show(fig)

#
def trimData(dataLists, start, end):
    for (i,data) in enumerate(dataLists):
        dataLists[i] = dataLists[i][start:end]
    return dataLists

# Read the log
def readLog(logName):
    log = lcm.EventLog(logName, 'r')

    time, xPos, yPos, zPos, xVel, yVel, zVel = ([] for i in range(7))
    pitch, roll, yaw, pitchVel, rollVel, yawVel = ([] for i in range(6))
    u, w, q, theta = ([] for i in range(4))
    elevator = []

    for event in log:
        if event.channel == "controlCommands":
            msg = controlCommands.decode(event.data)

            elevator.append(msg.controls)

        if event.channel == "controlState":
            msg = controlState.decode(event.data)
            u.append(msg.states[0])
            w.append(msg.states[1])
            q.append(msg.states[2])
            theta.append(msg.states[3])

        if event.channel == "flightState":
            msg = viconState.decode(event.data)

            time.append(msg.timestamp/1e6)
            xPos.append(msg.position[1])
            yPos.append(msg.position[0])
            zPos.append(msg.position[2])

            xVel.append(msg.velocity[1])

    # xPos = removeOcclusionNoise(xPos)
    # yPos = removeOcclusionNoise(yPos)
    # zPos = removeOcclusionNoise(zPos)

    # Manually trimming the data to only include the actual trial
    startIndex = 347
    endIndex = 623
    [time,xPos,yPos,zPos,u,w,q,theta] = trimData([
        time,xPos,yPos,zPos,u,w,q,theta], startIndex, endIndex)

    # Getting time to the correct starting point
    startTime = time[0]
    for (i,t) in enumerate(time):
        time[i] = t - startTime

    plotFig(time,xPos,"xFigure.html", "x position (m)", 
        title="X Position with No Control")

    plotFig(time,yPos,"yFigure.html", "y position (m)", 
        title="Y Position with No Control")

    plotFig(time,zPos,"zFigure.html", "z position (m)", 
        title="Z Position with No Control")

    plotFig(time,u,"uFigure.html", "u state (m/s)",
        title="U Control State with No Control")

    plotFig(time,w,"uFigure.html", "w state (m/s)",
        title="W Control State with No Control")

    plotFig(time,q,"qFigure.html", "q state (rad/s)",
        title="Q Control State with No Control")

    plotFig(time,theta,"thetaFigure.html", "theta state (rad)",
        title="Theta Control State with No Control")

    filename = 'flightData.csv'
    writeCsv([time,xPos,yPos,zPos,u,w,q,theta], filename=filename)

#-------------------------------------------------------------------------------
# If given a log name in the command line, read that log. Else, read the default
# log name of 'flightdData.log'.
if __name__ == '__main__':
    if len(argv) > 1:
        readLog(argv[1])
    else:
        readLog('flightData.log')