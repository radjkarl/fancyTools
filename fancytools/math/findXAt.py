import numpy as np
from scipy import interpolate

def findXAt(xArr, yArr, yVal):
    '''
    return all x values where y would be equal to given yVal
    if arrays are spline interpolated
    '''
    yArr = yArr-yVal
    if len(yArr) < 5:
        xn = np.linspace(xArr[0],xArr[-1],5)
        yArr = np.interp(xn, xArr, yArr)
        xArr = xn
    f = interpolate.UnivariateSpline(xArr, yArr)
 
    try:
        return f.roots()[0]
    except IndexError:
        #sometimes fails... // that one is unclean, but ... well TODO
        i = np.argmax(yArr<0)
        x0 = xArr[i-1]
        x1 = xArr[i]
        return 0.5 * (x0 + x1)

        
        
        