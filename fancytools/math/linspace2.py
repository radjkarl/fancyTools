# -*- coding: utf-8 -*-
from __future__ import division

from numpy import linspace

def linspace2(a, b, n, dtype=None):
	'''similar to numpy.linspace but excluding the boundaries
	
	this is the normal numpy.linspace:
	
	>>> print linspace(0,1,5)
	[ 0.    0.25  0.5   0.75  1.  ]
	
	and this gives excludes the boundaries:
	
	>>> print linspace2(0,1,5)
	[ 0.1  0.3  0.5  0.7  0.9]
	'''
	a = linspace(a, b, n+1, dtype=dtype)[:-1]
	if len(a) > 1:
		diff01 = ((a[1]-a[0])/2).astype(a.dtype)
		a += diff01
	return a


if __name__ == "__main__":
	import doctest
	doctest.testmod()