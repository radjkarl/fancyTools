import numpy as np

class DynamicMovingAverage(object):
    '''
    calc. the mean of the last n values, see http://en.wikipedia.org/wiki/Moving_average
    
    Update one value at a time.
    
    :param n: number of the last values to calc the mean from
    '''
    def __init__(self, n):
        self.maxQuantity = n # middle until this quantity is reached
        self.reset()


    def reset(self):
        self.value = 0.0
        self._quantity = 0


    def update(self, signal):
        ##dependent to the size of the cluster (v = old + (new-old)/size_cluser))
        if self._quantity < self.maxQuantity:
            self._quantity += 1
        self.value += (signal - self.value) / self._quantity
        return self.value



def staticMovingAverage(arr, fineness=10):
    '''
    smooth [arr] using moving average
    '''
    s0 = arr.shape[0]
    window_len = int(round(int(s0/fineness)))
    s=np.r_[arr[window_len-1:0:-1],arr,arr[-1:-window_len:-1]]
    w=np.ones(window_len,'d')
    return np.convolve(w/w.sum(),s,mode='valid')[:s0]
