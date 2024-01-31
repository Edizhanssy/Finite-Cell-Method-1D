
import numpy as np

def legendre_polynomial(n, x):
    """ Compute the n-th Legendre polynomial at x. """
    if n == 0:
        return 1
    elif n == 1:
        return x
    else:
        return ((2*n - 1)*x*legendre_polynomial(n-1, x) - (n - 1)*legendre_polynomial(n-2, x)) / n

def evalPhi(i, xi):
    """ Compute a value related to the Legendre polynomial for the given index i and coordinate xi. """
    return 1 / np.sqrt(4 * i - 2) * (legendre_polynomial(i, xi) - legendre_polynomial(i - 2, xi))

def evalShapeFunct(PolynomialDegree, xi):
    """ Compute the shape function N at coordinate xi. """
    NodalModes = evalNodalModes(xi)
    EdgeModes = evalEdgeModes(PolynomialDegree, xi)
    return np.concatenate([NodalModes, EdgeModes])

def evalNodalModes(xi):
    """ Compute the nodal modes for coordinate xi. """
    N1 = 0.5 * (1 - xi)
    N2 = 0.5 * (1 + xi)
    return np.array([N1, N2])

def evalEdgeModes(PolynomialDegree, xi):
    """ Compute the edge modes for coordinate xi. """
    EdgeModes = np.zeros(PolynomialDegree - 1)
    for i in range(1, PolynomialDegree):
        EdgeModes[i - 1] = evalPhi(i + 1, xi)
    return EdgeModes



