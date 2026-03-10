import math

import numpy as np

from .GetAttPositionArff import GetAttPositionArff


def GetAcceleration(data, attributes, attSpeed, attDir, windowWidth):
    c_minConf = 0.75
    step = math.ceil(windowWidth / 2)

    acceleration = np.zeros((data.shape[0],), dtype=float)

    timeInd = GetAttPositionArff(attributes, 'time')
    confInd = GetAttPositionArff(attributes, 'confidence')
    speedInd = GetAttPositionArff(attributes, attSpeed)
    dirInd = GetAttPositionArff(attributes, attDir)

    for i in range(data.shape[0]):
        if data[i, confInd] < c_minConf:
            continue

        if step == windowWidth:
            startPos = i - step
            endPos = i
        else:
            startPos = i - step
            endPos = i + step

        if startPos < 0 or data[startPos, confInd] < c_minConf:
            startPos = i
        if endPos >= data.shape[0] or data[endPos, confInd] < c_minConf:
            endPos = i

        if startPos == endPos:
            continue

        velStartX = data[startPos, speedInd] * math.cos(data[startPos, dirInd])
        velStartY = data[startPos, speedInd] * math.sin(data[startPos, dirInd])

        velEndX = data[endPos, speedInd] * math.cos(data[endPos, dirInd])
        velEndY = data[endPos, speedInd] * math.sin(data[endPos, dirInd])

        deltaT = (data[endPos, timeInd] - data[startPos, timeInd]) / 1000000

        accX = (velEndX - velStartX) / deltaT
        accY = (velEndY - velStartY) / deltaT

        acceleration[i] = math.sqrt(accX ** 2 + accY ** 2)

    return acceleration
