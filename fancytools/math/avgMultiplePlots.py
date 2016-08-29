import numpy as np

def avgMultiplePlots(data, nsample=None):
    '''
    return the average (x,y) for a set of multiple x,y arrays
    which can have a different length and resolution
    
    data = ((xvals,yvals),(),,,)
    assumes that x values are sorted
    '''
    xmin = min([x[0] for x,_ in data])
    xmax = max([x[-1] for x,_ in data])
    if nsample is None:
        nsample = max([len(x) for x,_ in data])
    
    xArr = np.linspace(xmin,xmax,nsample)
    interpol = [np.interp(xArr, x,y, 
                          left=np.nan, right=np.nan
                          ) for x,y in data]
    return xArr, np.nanmean(interpol, axis=0)


if __name__ == '__main__':
    import pylab as plt
    
    x0 = [1,2,3,4]
    y0 = [2,3,4,5]
    x1 = [2,3,4,5,8]
    y1 = [5,6,7,8,10]
    xa,ya = avgMultiplePlots( ((x0,y0), (x1,y1)) )
    
    plt.plot(x0,y0)
    plt.plot(x1,y1)
    plt.plot(xa,ya, 'o-')
    plt.show()