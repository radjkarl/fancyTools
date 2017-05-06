# coding=utf-8
import numpy as np


def angleDiff(angle1, angle2, take_smaller=True):
    """
    smallest difference between 2 angles
    code from http://stackoverflow.com/questions/1878907/the-smallest-difference-between-2-angles
    """
    a = np.arctan2(np.sin(angle1 - angle2), np.cos(angle1 - angle2))
    if isinstance(a, np.ndarray) and take_smaller:
        a = np.abs(a)
        # take smaller of both possible angles:
        ab = np.abs(np.pi - a)
        with np.errstate(invalid='ignore'):
            i = a > ab
        a[i] = ab[i]
    return a
