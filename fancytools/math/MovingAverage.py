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

    start = arr[0] + arr[0] - arr[window_len-1:0:-1]
    end = arr[-1] + arr[-1] - arr[-1:-window_len:-1]
    s=np.r_[start,arr,end]
    w=np.ones(window_len,'d')
    w /= w.sum()
    a0 = np.convolve(w,s,mode='valid')[:s0]
    a1 = np.convolve(w,s[::-1],mode='valid')[:s0][::-1]
    return 0.5* (a0+a1)




if __name__ == '__main__':
    import pylab as plt
    n = 100
    noise = 0.1
    fineness = 10
    a = np.sin(np.linspace(0,10,n))
    a += np.random.rand(n)*noise
    a2 = staticMovingAverage(a, fineness)
    
    plt.plot(a)
    plt.plot(a2)
    plt.show()
