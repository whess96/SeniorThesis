#################################################################
# readLogs.py
#
# Reads the LCM EventLogs, and can be modified to plot various 
# relevant data.
#################################################################

import lcm
from sys import argv
from datetime import datetime
from planeDataT import viconState, controlCommands, controlState

import numpy as np
from bokeh.plotting import figure, output_file, show
import csv

# Write the data to a csv. data is a 2D list where each lower 
# level list is a column of data. 
def writeCsv(data, filename):
    with open(filename, 'w') as destination:
        csvWriter = csv.writer(destination, delimiter=',')
        newRow = len(data)*[0]
        for i in range(len(data[0])):
            for j in range(len(data)):
                if (i < len(data[j])):
                    newRow[j] = data[j][i]
                else:
                    newRow[j] = 0
            csvWriter.writerow(newRow)

# Plots the data in bokeh
def plotFig(x, y, filename, yaxis, xaxis="Time (s)", title=""):
    output_file = "filename"
    fig = figure(x_axis_label=xaxis, y_axis_label=yaxis,
        title=title, tools='save,hover')
    fig.line(x,y,line_width=2)
    fig.xaxis.major_label_orientation = np.pi/2
    show(fig)

# Trims each list of data in dataLists based on the start and 
# end indices. Typical use is that start and end indicate the 
# actual time of the test flight, and many sets of data need to 
# be looked at.
def trimData(dataLists, start, end):
    for (i,data) in enumerate(dataLists):
        dataLists[i] = dataLists[i][start:end]
    return dataLists

# Read the log
def readLog(logName):
    log = lcm.EventLog(logName, 'r')

    time = []
    xPos, yPos, zPos, xVel, yVel, zVel = ([] for i in  range(6))
    pitch, roll, yaw = ([] for i in range(3))
    pitchVel, rollVel, yawVel = ([] for i in range(3))
    u, w, q, theta = ([] for i in range(4))
    elevCalc, elevAngle = ([] for i in range(2))
    chan0,chan1,chan2,chan3,chan4,chan5 = ([] for i in range(6))
    elevAngleTime = []

    for event in log:
        if event.channel == "controlCommands":
            msg = controlCommands.decode(event.data)

            elevCalc.append(msg.controlCalc)
            elevAngle.append(msg.controlAngle)
            elevAngleTime.append(msg.timestamp/1e6)

            chan0.append(msg.channels[0])
            chan1.append(msg.channels[1])
            chan2.append(msg.channels[2])
            chan3.append(msg.channels[3])
            chan4.append(msg.channels[4])
            chan5.append(msg.channels[5])

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
            yVel.append(msg.velocity[0])
            zVel.append(msg.velocity[2])

            pitch.append(msg.angles[0])
            roll.append(msg.angles[1])
            yaw.append(msg.angles[2])

            pitchVel.append(msg.angularRates[0])
            rollVel.append(msg.angularRates[1])
            yawVel.append(msg.angularRates[2])

    # Manually trimming the data to only include the actual trial
    startIndex = 347
    endIndex = 623
    [time,xPos,yPos,zPos,u,w,q,theta] = trimData([
        time,xPos,yPos,zPos,u,w,q,theta], startIndex, endIndex)

    # Getting time to the correct starting point
    startTime = time[0]
    for (i,t) in enumerate(time):
        time[i] = t - startTime

    for (i,t) in enumerate(elevAngleTime):
        elevAngleTime[i] = t - startTime

    plotFig(time,zPos,"zFigure.html", "z position (m)", 
        title="Z Position")

    plotFig(time,u,"uFigure.html", "u state (m/s)",
        title="U Control State")

    plotFig(time,w,"uFigure.html", "w state (m/s)",
        title="W Control State")

    plotFig(time,q,"qFigure.html", "q state (rad/s)",
        title="Q Control State")

    plotFig(time,pitch,"thetaFigure.html", "theta state (rad)",
        title="Theta Control State")

    plotFig(time, elevCalc, "elevatorFigure.html", 
        "Elevator control",
        title="Calculated Elevator Control over Time")

    plotFig(time, elevAngle, "elevAngleFigure.html", 
        "Elevator angle", title="Elevator Angle over Time")

    filename = 'newControl5.csv'
    writeCsv(['time','xPos','yPos','zPos','xVel','yVel','zVel',
        'pitch','roll','yaw','pitchVel','rollVel','yawVel','u',
        'w','q','theta','elevAngle','elevTime'],
        filename=filename)
    writeCsv([time,xPos,yPos,zPos,xVel,yVel,zVel,pitch,roll,yaw,
        pitchVel,rollVel,yawVel,u,w,q,theta,elevAngle,
        elevAngleTime], filename=filename)

#----------------------------------------------------------------
# If given a log name in the command line, read that log. Else, 
# read the default log name of 'flightdData.log'.
if __name__ == '__main__':
    if len(argv) > 1:
        readLog(argv[1])
    else:
        readLog('flightData.log')