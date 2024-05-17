# noinspection PyPackageRequirements
import numpy as np
# noinspection PyPackageRequirements
from numpy import ndarray as nd


def _y(vector: nd) -> nd:
    """Solution Vector (Y) for the generalized linear solution X*b=Y"""
    y = 2 * (2 * vector[0:-1] + vector[1:])
    y[0] = vector[0] + 2 * vector[1]
    y[-1] = 8 * vector[-2] + vector[-1]

    return y


def _a(c: nd, d: nd) -> nd:
    n = len(d)
    a = np.zeros((n,))
    a[-1] = d[-1]
    for i in range(n - 2, -1, -1):
        a[i] = (d[i] - c[i] * a[i + 1])

    return a


def _b(a: nd, vector: nd):
    b = np.zeros((len(vector) - 1,))
    b[:-1] = 2 * vector[1:-1] - a[1:]
    b[-1] = (a[-1] + vector[-1]) / 2

    return b


def _c(vector: nd):
    c = 0.5
    yield c

    for i in range(1, len(vector)-2):
        c = 1 / (4 - c)
        yield c


def _d(vector: nd, c: nd):
    n = len(vector) - 1
    y = _y(vector)

    d = y[0] / 2
    yield d

    for i in range(1, n - 1):
        d = (y[i] - d) / (4 - c[i - 1])
        yield d

    yield (y[-1] - 2 * d) / (7 - 2 * c[-1])


def interpolate(vector: nd) -> tuple[nd, nd]:
    """
    Use Thomas Algorithm to solve the tridiagonal system xb=y.
    """

    c = np.array(list(_c(vector)))
    d = np.array(list(_d(vector, c)))

    a = _a(c, d)
    b = _b(a, vector)

    return a, b
