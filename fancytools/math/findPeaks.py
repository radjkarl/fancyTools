'''
Created on 8 Aug 2016

@author: elkb4
'''
import numpy as np
from numba import jit


def findMax(arr):
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
#     import sys
#     import pylab as plt

    
    a = np.array([0,0,1,2,2,3,2,4,3,2,2,3,3,3,1])
    print a[findMax(a)]
    print a[findMin(a)]
    
#     
# #     import doctest
# #     doctest.testmod()
# 
#     from fancytools.os.PathStr import PathStr
#     import imgProcessor
#     from imgProcessor.imgIO import imread
#     from scipy.ndimage.filters import maximum_filter
# 
#     p = PathStr(imgProcessor.__file__).dirname().join(
#                 'media', 'electroluminescence')
# 
# 
#     img = imread(p.join('EL_cell_cracked.png'), 'gray')
#     
#     bn = maximum_filter(#<-- make lines bold
#             localizedMaximum(-img, thresh=30, min_increase=10, max_length=10)
#             ,3)
# 
#     if 'no_window' not in sys.argv:
#         plt.figure('image')
#         plt.imshow(img)
#         plt.colorbar()
#         plt.figure('binarized')
#         plt.imshow(bn)        
#         plt.show()