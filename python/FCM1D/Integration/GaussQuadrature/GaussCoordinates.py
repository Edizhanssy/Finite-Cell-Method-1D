import numpy as np
from functools import lru_cache


@lru_cache(maxsize=None)
def _rule(n):
    x, w = np.polynomial.legendre.leggauss(int(n))
    x.setflags(write=False)
    w.setflags(write=False)
    return x, w


def GaussQuadratureCoordinates(GO):
    return _rule(GO)[0]