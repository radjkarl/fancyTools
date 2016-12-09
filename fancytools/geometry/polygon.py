'''
mostly for 2d polygons
'''
import numpy as np



def center(poly):
    return poly.mean(axis=0)


def area(x,y):
    """
    Calculate the area of a polygon given as x(...),y(...)
    Implementation of Shoelace formula
    """
    # http://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def scale(poly, factor, center=None):
    poly = np.asarray(poly)
    x = poly[:,0]
    y = poly[:,1]
    
    try: fx,fy = factor
    except TypeError: fx,fy = factor, factor
    
    if center is None:
        center = x.mean(),y.mean() 
    cx,cy = center
    
    dx = x-cx
    dy = y-cy
    
    out = np.empty_like(poly)
    out[:,0] = cx+dx*fx
    out[:,1] = cy+dy*fy

    return out


def pointInsidePolygon(x, y, poly):
    """
    Determine if a point is inside a given polygon or not
    Polygon is a list of (x,y) pairs.

    [code taken from: http://www.ariel.com.au/a/python-point-int-poly.html]

    let's make an easy square:

    >>> poly = [ (0,0),\
                 (1,0),\
                 (1,1),\
                 (0,1) ]
    >>> pointInsidePolygon(0.5,0.5, poly)
    True
    >>> pointInsidePolygon(1.5,1.5, poly)
    False
    """
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside



if __name__ == '__main__':
    import doctest
    doctest.testmod()
    x = np.arange(0, 1, 0.001)
    y = np.sqrt(1 - x**2)
    print(area(x, y))
