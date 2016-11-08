# coding=utf-8
import numpy as np
from scipy.stats import linregress


def linRegressUsingMasked2dArrays(xVals, arrays, badMask=None, 
                                  zeroOffset=False,
                                  calcError=False):
    """
    if you have multiple 2d arrays each with position given by
    xVals[array-index]
    and you want to do a linear regression on all cells
    but you also might mask different areas in each 2darray

    zeroOffset - whether plot goest through origin

    returns ascent, offset, RMS-error
    """
    assert arrays.ndim == 3, 'need multiple 2d arrays'
    if badMask is not None:
        assert arrays.shape == badMask.shape, 'mask needs to have same shape'

    s = arrays.shape
    # flatten to create array of 1d arrays:
    y = arrays.reshape(s[0], s[1] * s[2]).astype(float)
    s = s[1:]
    if zeroOffset:
        A = np.array(xVals)[:,np.newaxis]
        ascent = solution = np.linalg.lstsq(A, y)[0].reshape(s)
        offset = 0
    else:
        A = np.vstack([xVals, np.ones(len(xVals))]).T
        # solve linear regression:
        solution = np.linalg.lstsq(A, y)[0]   
        offset = solution[1].reshape(s)
        ascent = solution[0].reshape(s)
    
    if badMask is not None:
        # do linear regression for all masked areas
        # trying to find multiple 2d arrays that are not masked together
        x, y = np.where(np.sum(badMask, axis=0))
        for xi, yi in zip(x, y):
            valid = ~badMask[:, xi, yi]
            try:
                if zeroOffset:
                    A = x[valid,np.newaxis]
                    asc = np.linalg.lstsq(A, arrays[valid, xi, yi])[0]
                else:
                    asc, offs = linregress(x[valid], arrays[valid, xi, yi])[:2]
                    offset[xi, yi] = offs
                ascent[xi, yi] = asc
                
            except ValueError:
                #if e.g. input is empty
                ascent[xi, yi] = np.nan
                if not zeroOffset:
                    offset[xi, yi] = np.nan
    if calcError:
        # calculate RMSE of the regression:
        error = np.empty(shape=arrays.shape)
        for n, (y, x) in enumerate(zip(arrays, xVals)):
            error[n] = (y - (x * ascent + offset))**2
        error = error.mean(axis=0)**0.5
    else:
        error = None

    return ascent, offset, error

# TODO: test case
