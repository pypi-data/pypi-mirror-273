"""
Python 2 and 3 code to generate 4 and 5 digit NACA profiles

The NACA airfoils are airfoil shapes for aircraft wings developed
by the National Advisory Committee for Aeronautics (NACA).
The shape of the NACA airfoils is described using a series of
digits following the word "NACA". The parameters in the numerical
code can be entered into equations to precisely generate the
cross-section of the airfoil and calculate its properties.
    https://en.wikipedia.org/wiki/NACA_airfoil

Pots of the Matlab code available here:
    http://www.mathworks.com/matlabcentral/fileexchange/19915-naca-4-digit-airfoil-generator
    http://www.mathworks.com/matlabcentral/fileexchange/23241-naca-5-digit-airfoil-generator

Copyright (C) 2011 by Dirk Gorissen <dgorissen@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from math import atan
from math import cos, sin
from math import pi
from math import pow
from math import sqrt

import numpy as np
import pyvista as pv


def linspace(start, stop, np):
    """
    Emulate Matlab linspace
    """
    return [start + (stop - start) * i / (np - 1) for i in range(np)]


def interpolate(xa, ya, queryPoints):
    """
    A cubic spline interpolation on a given set of points (x,y)
    Recalculates everything on every call which is far from efficient but does the job for now
    should eventually be replaced by an external helper class
    """

    # PreCompute() from Paint Mono which in turn adapted:
    # NUMERICAL RECIPES IN C: THE ART OF SCIENTIFIC COMPUTING
    # ISBN 0-521-43108-5, page 113, section 3.3.
    # http://paint-mono.googlecode.com/svn/trunk/src/PdnLib/SplineInterpolator.cs

    # number of points
    n = len(xa)
    u, y2 = [0] * n, [0] * n

    for i in range(1, n - 1):
        # This is the decomposition loop of the tridiagonal algorithm.
        # y2 and u are used for temporary storage of the decomposed factors.

        wx = xa[i + 1] - xa[i - 1]
        sig = (xa[i] - xa[i - 1]) / wx
        p = sig * y2[i - 1] + 2.0

        y2[i] = (sig - 1.0) / p

        ddydx = (ya[i + 1] - ya[i]) / (xa[i + 1] - xa[i]) - (ya[i] - ya[i - 1]) / (xa[i] - xa[i - 1])

        u[i] = (6.0 * ddydx / wx - sig * u[i - 1]) / p

    y2[n - 1] = 0

    # This is the backsubstitution loop of the tridiagonal algorithm
    # ((int i = n - 2; i >= 0; --i):
    for i in range(n - 2, -1, -1):
        y2[i] = y2[i] * y2[i + 1] + u[i]

    # interpolate() adapted from Paint Mono which in turn adapted:
    # NUMERICAL RECIPES IN C: THE ART OF SCIENTIFIC COMPUTING
    # ISBN 0-521-43108-5, page 113, section 3.3.
    # http://paint-mono.googlecode.com/svn/trunk/src/PdnLib/SplineInterpolator.cs

    results = [0] * n

    # loop over all query points
    for i in range(len(queryPoints)):
        # bisection. This is optimal if sequential calls to this
        # routine are at random values of x. If sequential calls
        # are in order, and closely spaced, one would do better
        # to store previous values of klo and khi and test if

        klo = 0
        khi = n - 1

        while (khi - klo > 1):
            k = (khi + klo) >> 1
            if (xa[k] > queryPoints[i]):
                khi = k
            else:
                klo = k

        h = xa[khi] - xa[klo]
        a = (xa[khi] - queryPoints[i]) / h
        b = (queryPoints[i] - xa[klo]) / h

        # Cubic spline polynomial is now evaluated.
        results[i] = a * ya[klo] + b * ya[khi] + ((a * a * a - a) * y2[klo] + (b * b * b - b) * y2[khi]) * (h * h) / 6.0

    return results


def naca4(number, n, finite_te=False, half_cosine_spacing=False):
    """
    Returns 2*n+1 points in [0 1] for the given 4 digit NACA number string
    """

    m = float(number[0]) / 100.0
    p = float(number[1]) / 10.0
    t = float(number[2:]) / 100.0

    a0 = +0.2969
    a1 = -0.1260
    a2 = -0.3516
    a3 = +0.2843

    if finite_te:
        a4 = -0.1015  # For finite thick TE
    else:
        a4 = -0.1036  # For zero thick TE

    if half_cosine_spacing:
        beta = linspace(0.0, pi, n + 1)
        x = [(0.5 * (1.0 - cos(xx))) for xx in beta]  # Half cosine based spacing
    else:
        x = linspace(0.0, 1.0, n + 1)

    yt = [5 * t * (a0 * sqrt(xx) + a1 * xx + a2 * pow(xx, 2) + a3 * pow(xx, 3) + a4 * pow(xx, 4)) for xx in x]

    xc1 = [xx for xx in x if xx <= p]
    xc2 = [xx for xx in x if xx > p]

    if p == 0:
        xu = x
        yu = yt

        xl = x
        yl = [-xx for xx in yt]

        xc = xc1 + xc2
        zc = [0] * len(xc)
    else:
        yc1 = [m / pow(p, 2) * xx * (2 * p - xx) for xx in xc1]
        yc2 = [m / pow(1 - p, 2) * (1 - 2 * p + xx) * (1 - xx) for xx in xc2]
        zc = yc1 + yc2

        dyc1_dx = [m / pow(p, 2) * (2 * p - 2 * xx) for xx in xc1]
        dyc2_dx = [m / pow(1 - p, 2) * (2 * p - 2 * xx) for xx in xc2]
        dyc_dx = dyc1_dx + dyc2_dx

        theta = [atan(xx) for xx in dyc_dx]

        xu = [xx - yy * sin(zz) for xx, yy, zz in zip(x, yt, theta)]
        yu = [xx + yy * cos(zz) for xx, yy, zz in zip(zc, yt, theta)]

        xl = [xx + yy * sin(zz) for xx, yy, zz in zip(x, yt, theta)]
        yl = [xx - yy * cos(zz) for xx, yy, zz in zip(zc, yt, theta)]

    X = xu[::-1] + xl[1:]
    Z = yu[::-1] + yl[1:]

    return X, Z


def naca5(number, n, finite_te=False, half_cosine_spacing=False):
    """
    Returns 2*n+1 points in [0 1] for the given 5 digit NACA number string
    """

    naca1 = int(number[0])
    naca23 = int(number[1:3])
    naca45 = int(number[3:])

    cld = naca1 * (3.0 / 2.0) / 10.0
    p = 0.5 * naca23 / 100.0
    t = naca45 / 100.0

    a0 = +0.2969
    a1 = -0.1260
    a2 = -0.3516
    a3 = +0.2843

    if finite_te:
        a4 = -0.1015  # For finite thickness trailing edge
    else:
        a4 = -0.1036  # For zero thickness trailing edge

    if half_cosine_spacing:
        beta = linspace(0.0, pi, n + 1)
        x = [(0.5 * (1.0 - cos(x))) for x in beta]  # Half cosine based spacing
    else:
        x = linspace(0.0, 1.0, n + 1)

    yt = [5 * t * (a0 * sqrt(xx) + a1 * xx + a2 * pow(xx, 2) + a3 * pow(xx, 3) + a4 * pow(xx, 4)) for xx in x]

    P = [0.05, 0.1, 0.15, 0.2, 0.25]
    M = [0.0580, 0.1260, 0.2025, 0.2900, 0.3910]
    K = [361.4, 51.64, 15.957, 6.643, 3.230]

    m = interpolate(P, M, [p])[0]
    k1 = interpolate(M, K, [m])[0]

    xc1 = [xx for xx in x if xx <= p]
    xc2 = [xx for xx in x if xx > p]
    xc = xc1 + xc2

    if p == 0:
        xu = x
        yu = yt

        xl = x
        yl = [-x for x in yt]

        zc = [0] * len(xc)
    else:
        yc1 = [k1 / 6.0 * (pow(xx, 3) - 3 * m * pow(xx, 2) + pow(m, 2) * (3 - m) * xx) for xx in xc1]
        yc2 = [k1 / 6.0 * pow(m, 3) * (1 - xx) for xx in xc2]
        zc = [cld / 0.3 * xx for xx in yc1 + yc2]

        dyc1_dx = [cld / 0.3 * (1.0 / 6.0) * k1 * (3 * pow(xx, 2) - 6 * m * xx + pow(m, 2) * (3 - m)) for xx in xc1]
        dyc2_dx = [cld / 0.3 * (1.0 / 6.0) * k1 * pow(m, 3)] * len(xc2)

        dyc_dx = dyc1_dx + dyc2_dx
        theta = [atan(xx) for xx in dyc_dx]

        xu = [xx - yy * sin(zz) for xx, yy, zz in zip(x, yt, theta)]
        yu = [xx + yy * cos(zz) for xx, yy, zz in zip(zc, yt, theta)]

        xl = [xx + yy * sin(zz) for xx, yy, zz in zip(x, yt, theta)]
        yl = [xx - yy * cos(zz) for xx, yy, zz in zip(zc, yt, theta)]

    X = xu[::-1] + xl[1:]
    Z = yu[::-1] + yl[1:]

    return X, Z


def naca(number, n, finite_te=False, half_cosine_spacing=True):
    if len(number) == 4:
        X, Y = naca4(number, n, finite_te, half_cosine_spacing)
    elif len(number) == 5:
        X, Y = naca5(number, n, finite_te, half_cosine_spacing)
    else:
        raise Exception

    # delete last point as it is defined twice

    """
    fix for trailing_edge finite_TE
    """
    if finite_te:
        points = np.stack((X, Y, np.zeros(len(X)))).T
        pointa = np.array([X[0], Y[0], 0])
        pointb = np.array([X[-1], Y[-1], 0])
        center = (pointb - pointa) / 2 + pointa
        arc = pv.CircularArc(pointa, pointb, center, negative=True)
        arcpts = arc.points[1:-2]
        points = np.vstack([points, arcpts[::-1]])
        X, Y = points[::, 0], points[::, 1]
        """
        # Creating equally spaced 100 data in range 0 to 2*pi
        theta = np.linspace(0, 2 * np.pi, 100)

        # Setting radius
        radius = 5

        # Generating x and y data
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        """
    points = np.stack([X, Y, np.zeros(len(X))]).T
    poly = pv.PolyData(points)
    poly = poly.clean(tolerance=1e-6)
    return poly.points[::, 0], poly.points[::, 1]
