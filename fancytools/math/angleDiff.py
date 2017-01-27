# coding=utf-8
import numpy as np
from numpy import arctan2, sin, cos


def angleDiff(angle1, angle2, take_smaller=True):
    """
    smallest difference between 2 angles
    code from http://stackoverflow.com/questions/1878907/the-smallest-difference-between-2-angles
    """
    a = arctan2(sin(angle1 - angle2), cos(angle1 - angle2))
    if take_smaller:
        a = np.abs(a)
        #take smaller of both possible angles:
        ab = np.abs(np.pi-a)
        with np.errstate(invalid='ignore'):
            i = a>ab
        a[i] = ab[i]
    return a
