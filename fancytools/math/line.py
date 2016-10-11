'''
Collection of line-based functions
line given as:
    x0,y0,x1,y1 = line
'''
from __future__ import division
from __future__ import print_function


from numpy import pi, array, empty, argmax, ndarray
from math import sin, cos, atan2, hypot, acos, copysign

from fancytools.math.rotatePolygon import rotatePolygon
from fancytools.math.pointInsidePolygon import pointInsidePolygon

from numba import jit
# from numpy.linalg import norm


def cutToFitIntoPolygon(line, polygon):
    '''
    cut line so it fits into polygon
    polygon = (( x0,y0), (x1,y1) ,...)
    '''
    p0_inside = pointInsidePolygon(line[0], line[1], polygon)
    p1_inside = pointInsidePolygon(line[2], line[3], polygon)

    if not p0_inside or not p1_inside:
        for (i0, j0), (i1, j1) in zip(polygon[:-1], polygon[1:]):

            isec = segmentIntersection(line, (i0, j0, i1, j1))

            if isec is not None:
                if not p0_inside:
                    line = (isec[0], isec[1], line[2], line[3])
                    p0_inside = True
                elif not p1_inside:
                    line = (line[0], line[1], isec[0], isec[1])
                    p1_inside = True

            if p0_inside and p1_inside:
                break
    return line


@jit(nopython=True)
def sort(line):
    '''
    change point position  if x1,y0 < x0,y0
    '''
    x0, y0, x1, y1 = line
#     if (x0**2+y0**2)**0.5 < (x1**2+y1**2)**0.5:
#         return (x1,y1,x0,y0)
#     return line
#
#     if x1 < x0:
#         return (x1,y1,x0,y0)
#     return line

    turn = False

    if abs(x1 - x0) > abs(y1 - y0):
        if x1 < x0:
            turn = True
    elif y1 < y0:
        turn = True

    if turn:
        return (x1, y1, x0, y0)
      #  return line[(2,3,0,1)]
    return line
#         line[0] = x1
#         line[1] = y1
#         line[2] = x0
#         line[3] = y0


def normal(line):
    '''return the unit normal vector'''
    dx, dy = dxdy(line)
    return -dy, dx  # other normal v would be dy,-dx
    # return dxdy(line)[::-1]


@jit(nopython=True)
def length(line):
    x0, y0, x1, y1 = line
    dx = x1 - x0
    dy = y1 - y0
    return hypot(dx, dy)


def isEven(angle):
    '''
    return whether lines is either horizontal or vertical
    '''
    return angle < 0.1 or angle > 1.4


def dxdy(line):
    '''
    return normalised ascent vector
    '''
    x0, y0, x1, y1 = line
    dx = float(x1 - x0)
    dy = float(y1 - y0)
    f = hypot(dx, dy)
    return dx / f, dy / f


def ascent(line):
    x0, y0, x1, y1 = line
    try:
        return min(((y1 - y0) / (x1 - x0)), 1e10)
    except ZeroDivisionError:
        return 1e10


def angle(line):
    x0, y0, x1, y1 = line
    try:
        return atan2(float(y1) - y0, float(x1) - x0)
    except ZeroDivisionError:
        if y1 > y0:
            return - pi
        return pi


@jit(nopython=True)
def angle2(line1, line2):
    # return angle between two lines
    # from
    # http://stackoverflow.com/questions/13226038/calculating-angle-between-two-lines-in-python
    x0, y0, x1, y1 = line1
    x1 -= x0
    y1 -= y0
    x0, y0, x2, y2 = line2
    x2 -= x0
    y2 -= y0
    inner_product = x1 * x2 + y1 * y2
    len1 = hypot(x1, y1)
    len2 = hypot(x2, y2)
    a = inner_product / (len1 * len2)
    return copysign(acos(min(1, max(a, -1))), y2)


def fromAttr(mid, ang, dist):
    '''
    create from middle, angle and distance
    '''
    mx, my = mid
    dx = cos(ang) * dist * 0.5
    dy = sin(ang) * dist * 0.5
    return mx - dx, my - dy, mx + dx, my + dy


def fromAttr2(start, ang, dist):
    '''
    create from start, angle and distance
    '''
    sx, sy = start
    dx = cos(ang) * dist
    dy = sin(ang) * dist
    return sx, sy, sx + dx, sy + dy


def fromFn(ascent, offs, length=1, px=0):
    py = px * ascent + offs
    dx = length
    dy = ascent * length
    if length != 1:
        # normalize
        l = length / (dx**2 + dy**2)**0.5
        dx *= l
        dy *= l
    return px, py, px + dx, py + dy


def toFn(line):
    x0, y0 = line[:2]
    m = ascent(line)
    offs = y0 - m * x0
    return m, offs, length(line)


def merge(l1, l2):
    '''
    merge 2 lines together
    '''
    x1, y1, x2, y2 = l1
    xx1, yy1, xx2, yy2 = l2

    comb = ((x1, y1, xx1, yy1),
            (x1, y1, xx2, yy2),
            (x2, y2, xx1, yy1),
            (x2, y2, xx2, yy2))

    d = [length(c) for c in comb]
    i = argmax(d)

    dist = d[i]
    mid = middle(comb[i])

    a = (angle(l1) + angle(l2)) * 0.5
    return fromAttr(mid, a, dist)


def resize(line, factor):
    '''
    factor: relative length (1->no change, 2-> double, 0.5:half)
    '''
    a = angle(line)
    mx, my = middle(line)
    d = length(line) * factor * 0.5
    dx = cos(a) * d
    dy = sin(a) * d
    return mx - dx, my - dy, mx + dx, my + dy


@jit(nopython=True)
def middle(line):
    x0, y0, x1, y1 = line
    return (x0 + x1) / 2, (y0 + y1) / 2


def rotate(line, angle):
    x0, y0, x1, y1 = line
    p = rotatePolygon(array(((x0, y0), (x1, y1))), angle)
    return [p[0, 0], p[0, 1], p[1, 0], p[1, 1]]


def distance(line, point):
    '''
    infinite line to point or line to line distance
    is point is given as line - use middle point of that liune
    '''
    x0, y0, x1, y1 = line
    try:
        p1, p2 = point
    except ValueError:
        # line is given instead of point
        p1, p2 = middle(point)
    n1 = ascent(line)
    n2 = -1
    n0 = y0 - n1 * x0
    return abs(n1 * p1 + n2 * p2 + n0) / (n1**2 + n2**2)**0.5


def segmentDistance(line, point):
    dx, dy = distanceVector(line, point, ignoreEndpoints=False)
    return (dx**2 + dy**2)**0.5


@jit(nopython=True)
def distanceVector(line, point, ignoreEndpoints=True):
    x0, y0, x1, y1 = line
    px, py = point
    line_magnitude = length(line)
    if line_magnitude == 0:
        return px - x0, py - y0
    u = ((px - x0) * (x1 - x0) +
         (py - y0) * (y1 - y0)) / (line_magnitude ** 2)
    # closest point does not fall within the line segment,
    # take the shorter distance to an endpoint
    if u < 0.00001 or u > 1:
        if ignoreEndpoints:
            return 0, 0
        ix = length((px, py, x0, y0))
        iy = length((px, py, x1, y1))
        if ix > iy:

            ix, iy = x1, y1
        else:
            ix, iy = x0, y0
    else:
        ix = x0 + u * (x1 - x0)
        iy = y0 + u * (y1 - y0)
    return ix - px, iy - py


def segmentIntersection(line1, line2):
    i = intersection(line1, line2)
    if i is None:
        return None
    # line1 and line2 are finite:
    # check whether intersection is on both lines:
    if (pointIsBetween(line1[0:2], line1[2:], i)
            and pointIsBetween(line2[0:2], line2[2:], i)):
        return i
    return None


def pointIsBetween(startP, endP, p):
    '''
    whether point is (+-1e-6) on a straight
    line in-between two other points
    '''
    return (distancePoint(startP, p) + distancePoint(p, endP)
            - distancePoint(startP, endP) < 1e-6)


def distancePoint(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5


@jit(nopython=True)
def intersection(line1, line2):
    """
    Return the coordinates of a point of intersection given two lines.
    Return None if the lines are parallel, but non-colli_near.
    Return an arbitrary point of intersection if the lines are colli_near.

    Parameters:
    line1 and line2: lines given by 4 points (x0,y0,x1,y1).
    """
    x1, y1, x2, y2 = line1
    u1, v1, u2, v2 = line2
    (a, b), (c, d) = (x2 - x1, u1 - u2), (y2 - y1, v1 - v2)
    e, f = u1 - x1, v1 - y1
    # Solve ((a,b), (c,d)) * (t,s) = (e,f)
    denom = float(a * d - b * c)
    if _near(denom, 0):
        # parallel
        # If colli_near, the equation is solvable with t = 0.
        # When t=0, s would have to equal e/b and f/d
        if b == 0 or d == 0:
            return None
        if _near(e / b, f / d):
            # colli_near
            px = x1
            py = y1
        else:
            return None
    else:
        t = (e * d - b * f) / denom
        # s = (a*f - e*c)/denom
        px = x1 + t * (x2 - x1)
        py = y1 + t * (y2 - y1)
    return px, py


@jit(nopython=True)
def _near(a, b, rtol=1e-5, atol=1e-8):
    return abs(a - b) < (atol + rtol * abs(b))


def translate(line, ascent, offs=0):
    '''
    offs -> shifts parallel to line
    ascent -> rotate line
    '''
    # TODO: why do I have thuis factor here?
    ascent *= -2
    offs *= -2

    l0 = length(line)

    # change relative to line:
    t0 = offs  # -h+offs
    t1 = l0 * ascent + offs
    return translate2P(line, t0, t1)


def translate2P(line, t0, t1):
    a = angle(line)

#     if 0.25*pi > abs(a) or abs(a) > 0.75*pi:#isHorizontal
#         t0*=-1
#         t1*=-1

    # change in x and y:
    dx0 = -sin(a) * t0
    dx1 = -sin(a) * t1
    dy0 = cos(a) * t0
    dy1 = cos(a) * t1
    return line[0] + dx0, line[1] + dy0, line[2] + dx1, line[3] + dy1


# REMOVE?
def split(line, lines):
    '''
    split <line> into multiple sublines
    using intersection with <lines>
    '''
    out = empty((len(lines) + 1, 4))

    p1 = line[:2]
    for n, l2 in enumerate(lines):
        p2 = intersection(line, l2)
        out[n][:2] = p1
        out[n][2:] = p2
        p1 = p2
    out[n + 1][:2] = p2
    out[n + 1][2:] = line[2:]
    return out


def splitN(line, n):
    '''
    split a line n times
    returns n sublines
    '''
    x0, y0, x1, y1 = line

    out = empty((n, 4), dtype=type(line[0]))
    px, py = x0, y0
    dx = (x1 - x0) / n
    dy = (y1 - y0) / n

    for i in range(n):
        o = out[i]
        o[0] = px
        o[1] = py
        px += dx
        py += dy
        o[2] = px
        o[3] = py
    return out


def isHoriz(line):
    a = abs(angle(line))
    return 0.25 * pi > a or a > 0.75 * pi


if __name__ == '__main__':
    pass
    # TODO: generate tests


#     import pylab as plt
#     import numpy as np
#
#
# #     l0 = (0,0,10,0.5)
# #     l1 = (0,0,10,-0.5)
# #     print normal(l0), normal(l1)
# #     print ascent(l0), ascent(l1)
# #
# #
# #     l0 = (1822, 1140, 1805, 1262)
# #     print angle(l0), isHoriz(l0)
# #     plt.plot((l0[0],l0[2]),(l0[1],l0[3]),'r')
# #     plt.scatter(l0[0],l0[1])
#     l0 = (1843, 1046, 1867, 907)
# #     print angle(l0), isHoriz(l0)
# #
# #     plt.plot((l0[0],l0[2]),(l0[1],l0[3]),'r')
# #     plt.scatter(l0[0],l0[1])
# #
# #     l1 = (1624, 1372, 1730, 1380)
# #     plt.plot((l1[0],l1[2]),(l1[1],l1[3]),'g')
# #     plt.scatter(l1[0],l1[1])
# #     print angle(l1), isHoriz(l1)
# #
# #     l1 =(1879, 551, 1784, 535)
# #     plt.plot((l1[0],l1[2]),(l1[1],l1[3]),'g')
# #     plt.scatter(l1[0],l1[1])
# #     print angle(l1), isHoriz(l1)
#
#
# #     l1 = translate2P(l0,-0.186749451731, -9.05925804855)
# #
# #     plt.plot((l1[0],l1[2]),(l1[1],l1[3]),'g')
#
# #     l1 = translate2P(l0,1,0)
# #     plt.plot((l1[0],l1[2]),(l1[1],l1[3]),'g')
#
#     plt.show()
#
#     for n in np.linspace(0,np.pi,10):
#         if n:
#             l0 = translate2P(l0,n,-n)
#             print(length(l0))
#             print(l0)
#             plt.plot((l0[0],l0[2]),(l0[1],l0[3]),'g')
# #             if n :
# #                 break
#     plt.show()
#
# #     l0 = [2625,  526, 2625, 1441]
# #     l1 = [2178 , 288 ,2178 ,3021]
# #     print middle(l1)
# #     print 666, distanceVector(l0, middle(l1), ignoreEndpoints=False)
#
#     l0 = [0.,0.5,0.,1.]
#
#     l1 = [0.5,0.,1.5,0.]
#
#
#
#
#     print(angle2(l0,l1),888)
#     print(intersection(l0,l1))
#
#
#     plt.plot((l0[0],l0[2]),(l0[1],l0[3]),'r')
#     plt.plot((l1[0],l1[2]),(l1[1],l1[3]),'g')
#     plt.show()
#
#
#     ll = [[0.1,1,0.1,0],[0.3,1,0.3,0]]
#     print(splitN(l0,3))
#
#
#
# #
#     l0 = [4674 , 233 ,4651, 2892]
#     a = -0.00284855546826
#     o = 5.5832401565
# #
#     l1= translate(l0, a, o)
#     plt.plot((l0[0],l0[2]),(l0[1],l0[3]),'r')
#     plt.plot((l1[0],l1[2]),(l1[1],l1[3]),'g')
#     plt.show()
# #(4650.9517093206787, 540593.62650955946, 4673.952276003728, 537934.62651446124)
#     p0 = [0.5,0.5]
#     print(length(l0))
#     print(distanceVector(l0, p0, ignoreEndpoints=True))
