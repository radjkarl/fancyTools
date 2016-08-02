import numpy as np


def polyFitIgnoringOutliers(x, y, deg=2, niter=3, nstd=2, return_outliers=False):
    '''Returns:
        (np.poly1d): callable function of polynomial fit excluding all outliers
    Args:
        deg (int): degree of polynomial fit
        n_iter (int): do linear regression n times
                      successive removing
        nstd (float): exclude outliers, if their deviation
            is > [nstd] * standard deviation
        return_outliers (bool): also return outlier positions as 2. arg
    '''
    if return_outliers:
        a = all_outliers = np.zeros_like(y,dtype=bool)
    for i in range(niter):
        poly = np.polyfit(x, y, deg)
        p = np.poly1d(poly)
        if i == niter - 1:
            break
        y_fit = p(x)
        dy = y-y_fit
        std = (dy**2).mean()**0.5
        inliers = abs(dy) < nstd*std
        if return_outliers:
            a[~inliers] = True

        if inliers.sum() > deg+1:
            x = x[inliers]
            y = y[inliers]
            if return_outliers:
                a = a[inliers]
        else:
            break
    if return_outliers:
        return p, all_outliers
    return p



if __name__ == '__main__':
    import pylab as plt
    import sys

    x = np.arange(100)
    y = x**2.0

    # add noise:
    y += np.random.rand(100) * 3

    # add some outliers:
    pos = np.random.randint(0, 10, 100) > 4
    vals = np.random.rand(pos.sum())*2000
    y[pos] = vals

    x2 = x[::3]
    y2 = y[::3]

    # ACTION
    p = polyFitIgnoringOutliers(x2, y2)
    y_fit = p(x)

    if 'no_window' not in sys.argv:
        plt.plot(x2, y2, label='values')
        plt.plot(x, y_fit, label='fit ignoring outliers')
        plt.legend()
        plt.show()
