#taken from http://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
import numpy as np


def polygonArea(x,y):
    '''
    Calculate the area of a polygon given as x(...),y(...)
    Implementation of Shoelace formula
    '''
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))


if __name__ == '__main__':
    x = np.arange(0,1,0.001)
    y = np.sqrt(1-x**2)
    print polygonArea(x,y)