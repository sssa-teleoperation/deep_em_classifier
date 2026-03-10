import math

import numpy as np

from .GetAttPositionArff import GetAttPositionArff


def GetVelocity(data, attributes, windowWidth):
    c_minConf = 0.75
    step = math.ceil(windowWidth / 2)

    speed = np.zeros((data.shape[0],), dtype=float)
    direction = np.zeros((data.shape[0],), dtype=float)

    timeInd = GetAttPositionArff(attributes, 'time')
    xInd = GetAttPositionArff(attributes, 'x')
    yInd = GetAttPositionArff(attributes, 'y')
    confInd = GetAttPositionArff(attributes, 'confidence')

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

        amplitude = math.sqrt(
            (data[endPos, xInd] - data[startPos, xInd]) ** 2
            + (data[endPos, yInd] - data[startPos, yInd]) ** 2
        )
        delta_t = (data[endPos, timeInd] - data[startPos, timeInd]) / 1000000
        speed[i] = amplitude / delta_t

        direction[i] = math.atan2(
            data[endPos, yInd] - data[startPos, yInd],
            data[endPos, xInd] - data[startPos, xInd],
        )

    return speed, direction
