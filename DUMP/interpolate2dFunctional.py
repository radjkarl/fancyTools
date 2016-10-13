'''
Created on 8 Jul 2015

@author: elkb4
'''
from __future__ import division
from past.utils import old_div
import numpy as np

from scipy.optimize import curve_fit
from scipy.ndimage.interpolation import zoom


# OLD: current solution fancytools.utils.fit2dArrayToFN

def vignettingEq(xxx_todo_changeme, f=100, alpha=0, Xi=0, tau=0, cx=50, cy=50):
    '''
    Vignetting equation using the KARL-WEISS-MODEL
    see http://research.microsoft.com/en-us/people/stevelin/vignetting.pdf

    f - focal length
    alpha - coefficient in the geometric vignetting factor
    Xi - tilt factor of a planar scene
    tau - rotation angle of a planar scene
    cx - image center, x
    cy - image center, y
    '''
    (x, y) = xxx_todo_changeme
    dist = ((x - cx)**2 + (y - cy)**2)**0.5

    A = old_div(1.0, (1 + (old_div(dist, f))**2)**2)
    G = (1 - alpha * dist)
    T = np.cos(tau) * (1 + (old_div(np.tan(tau), f))
                       * (x * np.sin(Xi) - y * np.cos(Xi)))**3

    return A * G * T


def fitVignettingEq(arr, mask, scale_factor=0.1):
    mask = np.logical_not(mask)

    # SCALE TO DECREASE AMOUNT OF POINTS TO FIT:
    small = zoom(arr, scale_factor)
    mask = zoom(mask, scale_factor)
    mask[mask < 0.5] = 0
    mask = mask.astype(bool)
    # USE ONLY VALID POINTS:
    y, x = np.where(mask)
    z = small[mask]
    # INITIAL GUESS:
    guess = (
        small.shape[0] *
        0.7,
        0,
        0,
        0,
        small.shape[0] /
        2.0,
        small.shape[1] /
        2.0)
    # FIT:
    parameters, cov_matrix = curve_fit(vignettingEq, (x, y), z, guess)
    # ERROR:
    perr = np.sqrt(np.diag(cov_matrix))
    # SCALE FACTOR:
    # BUILD ARRAY FROM FUNCTION:
    # SCALE FACTOR:
    fx = old_div(float(small.shape[0]), arr.shape[0])
    fy = old_div(float(small.shape[1]), arr.shape[1])
    # BUILD ARRAY FROM FUNCTION:
    rebuilt = np.fromfunction(
        lambda x, y: vignettingEq(
            (y * fy, x * fx), *parameters), arr.shape)
    return rebuilt, perr


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # TODO:
    # make work again - no external references
#     arr = np.load('C:\\Users\\elkb4\\Desktop\\Programming\\git\\imgprocessor\\imgProcessor\\cameraCalibration\\test.npy')
#     arr-=np.min(arr)
#     arr/=np.max(arr)
#
#     mask= np.logical_and(arr>=0.82754858, arr <= 0.82754859)
#
#
#     out, error = fitVignettingEq(arr, mask, scale_factor=0.1)
#
#
#     arr2 = arr.copy()
#     arr2[mask] = out[mask]
#
#
#     #generell luecken mit fn ausfuellen
#     #diese file in sensitiv. modul rein
#     #sens. cALC FN UNTERTEILEN UND MIT MEHR OPTIONS AUSSTATTEN - OB Z:B: LEERSTELLEN MIT FN GEFITTET WERDEN SOLLEN
#     #UND WIE gross smooth its
#     #fuer vergleich der unterschielichen lens, opesp. ueber parameter
#
#     #an eupvsec atricle arbeiten
#     #besser anfangen vignetting zu beschreiben
#     #in artivle microsoft article mention ...
#
#
#     #PLOT
#     plt.figure(1)
#     plt.imshow(arr)
#
#
#     plt.clim(0.3,1)
#
#     plt.figure(2)
#     plt.imshow(out)
#     plt.colorbar()
#     plt.clim(0.3,1)
#
#
#
#     plt.figure(3)
#     plt.imshow(arr2)
#     plt.colorbar()
#     plt.clim(0.3,1)
#
#     plt.show()
