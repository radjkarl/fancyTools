import numpy as np
from numba import jit


def findMax(arr):
    '''
    in comparison to argrelmax() more simple and  reliable peak finder
    '''
    out = np.zeros(shape=arr.shape, dtype=bool)
    _calcMax(arr, out)
    return out


@jit(nopython=True) 
def _calcMax(arr, out):
    g0 = arr.shape[0]

    up = False
    last = arr[0]
    for i in xrange(1,g0):
        
        px = arr[i]
        if up and px < last:
            out[i-1] = True
            up = False
        elif px > last:
            up = True
        last = px
         

def findMin(arr):
    '''
    in comparison to argrelmax() more simple and  reliable peak finder
    '''
    out = np.zeros(shape=arr.shape, dtype=bool)
    _calcMin(arr, out)
    return out


@jit(nopython=True) 
def _calcMin(arr, out):
    g0 = arr.shape[0]

    down = False
    last = arr[0]
    for i in xrange(1,g0):
        
        px = arr[i]
        if down and px > last:
            out[i-1] = True
            down = False
        elif px < last:
            down = True
        last = px


if __name__ == '__main__':

    a = np.array([0,0,1,2,2,3,2,4,3,2,2,3,3,3,1])
    #peaks values...
    assert np.allclose( a[findMax(a)], [3,4,3] )
    assert np.allclose( a[findMin(a)], [2,2]   )
 