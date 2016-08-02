import numpy as np


def radialAverage(arr, center=None):
    '''
    radial average a 2darray around a center
    if no center is given, take middle 
    '''
    #taken from http://stackoverflow.com/questions/21242011/most-efficient-way-to-calculate-radial-profile
    s0,s1 = arr.shape[:2]
    if center is None:
        center = float(s0)/2, float(s1)/2
    y, x = np.indices((s0,s1))
    r = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    r = r.astype(np.int)

    tbin = np.bincount(r.ravel(), arr.ravel())
    nr = np.bincount(r.ravel())
    radialprofile = tbin / nr
    return radialprofile 
