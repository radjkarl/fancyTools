import numpy as np

def avgMultiplePlots(data, calc_mean=True, calc_std=False, 
                     calc_density=False, nsample=None):
    '''
    return the average (x,y) for a set of multiple x,y arrays
    which can have a different length and resolution
    
    data = ((xvals,yvals),(),,,)
    assumes that x values are sorted
    '''
    xArr, yArr = bringPlotOverSameX(data, nsample)
    out = [xArr]
    if calc_mean:
        out.append(np.nanmean(yArr, axis=0))
    if calc_std:
        out.append(np.nanstd(yArr, axis=0))
    if calc_density:
        out.append( len(yArr) - np.isnan(yArr).sum(axis=0) )
    return tuple(out)



def bringPlotOverSameX(data, nsample=None):
    '''
    bring all plots (x,y)
    to same x value base
    '''
    x0 = [x[0] for x,_ in data]
    x1 = [x[-1] for x,_ in data]
 
    xmin = min(np.min(x0), np.min(x1))
    xmax = max(np.max(x0), np.max(x1))
       
    if nsample is None:
        #calc from mean point density:
        pn_per_dist = np.mean([ len(x) / float(abs(x[0]-x[-1])) 
                                for x,_ in data ])
        #...and max distance:
        nsample = round( pn_per_dist*abs(xmax-xmin) )
        
    xArr = np.linspace(xmin,xmax,nsample)

    if x0[0]> x1[0]:
        #values are reverse sorted
        interpol = [np.interp(xArr, x[::-1],y[::-1],
                    left=np.nan, right=np.nan) for x,y in data]  
    else:
        interpol = [np.interp(xArr, x,y,
                    left=np.nan, right=np.nan) for x,y in data]   
    return xArr, interpol



if __name__ == '__main__':
    import pylab as plt
    
    x0 = [1,2.2,3,4.2]
    y0 = [2,3,4,5]
    x1 = [1.4, 3.5, 4.5, 4.7, 4.9]
    y1 = [5  , 6  , 7  , 8  , 10]
    xa,ya = avgMultiplePlots( ((x0,y0), (x1,y1)) )
    
    plt.plot(x0,y0, 'o-')
    plt.plot(x1,y1, 'o-')
    plt.plot(xa,ya, 'o-', label='average')
    plt.show()