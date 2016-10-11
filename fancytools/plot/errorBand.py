# coding=utf-8
from __future__ import division
from __future__ import print_function

import numpy as np


def errorBand(x, yAvg, yStd, yDensity, plt, n_colors=None):
    """
    plot error-band around avg
    where colour equals to point density
    """

    dmn = yDensity.min()
    dmx = yDensity.max()

    if n_colors is None:
        n_colors = dmx - dmn + 1
    print(n_colors)
    cm = plt.cm.get_cmap('Blues', lut=n_colors)

    # normalize (0...1):
    relDensity = (yDensity - dmn) / (dmx - dmn)
    # limit the number of densities to n_colors:
    bins = np.linspace(0, 1, n_colors - 1)
    inds = np.digitize(relDensity, bins)

    i0 = 0
    try:
        while True:
            # define area length as those of the same alpha value
            v0 = inds[i0]
            am = np.argmax(inds[i0:] != v0)
            if am == 0:
                i1 = len(inds)
            else:
                i1 = i0 + am
            r = slice(i0, i1 + 1)
            col = cm(v0)
            # create polygon of color=density around average:
            plt.fill_between(x[r], yAvg[r] - yStd[r], yAvg[r] + yStd[r],
                             alpha=1,
                             edgecolor=col,  # '#3F7F4C',
                             facecolor=col,  # '#7EFF99',
                             linewidth=1)
            i0 = i1
    except IndexError:
        pass

    plt.plot(x, yAvg, 'k', color='#3F7F4C')

    # show colorbar in plot:
    sm = plt.cm.ScalarMappable(cmap=cm, norm=plt.Normalize(vmin=dmn, vmax=dmx))
    # fake up the array of the scalar mappable. Urgh...
    sm._A = []

    plt.colorbar(sm)
    plt.legend()


if __name__ == '__main__':
    import pylab as plt
    import sys

    x = np.arange(100)
    yAvg = np.sin(x * 0.2)
    yStd = np.cos(x * 0.3) * 0.7
    yDensity = (np.sin(x * 0.1) + 1) * 100

    # green plot is average
    # band is standard deviation
    # band color=number of points in that area!
    errorBand(x, yAvg, yStd, yDensity, plt)

    if 'no_window' not in sys.argv:
        plt.show()
