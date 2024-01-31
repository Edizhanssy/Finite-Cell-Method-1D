import numpy as np

def legendre_polynomial(n, x):
    """ Compute the n-th Legendre polynomial at x. """
    if n == 0:
        return 1
    elif n == 1:
        return x
    else:
        return ((2*n - 1)*x*legendre_polynomial(n-1, x) - (n - 1)*legendre_polynomial(n-2, x)) / n

def derivative_legendre_polynomial(n, x):
    """ Compute the derivative of the n-th Legendre polynomial at x recursively. """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return ((2*n - 1) * (legendre_polynomial(n-1, x) + x * derivative_legendre_polynomial(n-1, x)) - n * derivative_legendre_polynomial(n-2, x)) / n

def evalDerivOfPhi(i, xi):
    """ Compute the derivative for the given index i and coordinate xi. """
    return 1 / np.sqrt(4 * i - 2) * (derivative_legendre_polynomial(i, xi) - derivative_legendre_polynomial(i - 2, xi))

def evalEdgeModesDeriv(PolynomialDegree, xi):
    """ Compute the edge modes derivatives for coordinate xi. """
    EdgeModesDeriv = np.zeros(PolynomialDegree - 1)
    for i in range(1, PolynomialDegree):
        EdgeModesDeriv[i - 1] = evalDerivOfPhi(i + 1, xi)
    return EdgeModesDeriv

def evalNodalModesDeriv():
    """ Compute the derivatives of the nodal modes. """
    dN1 = -0.5
    dN2 = 0.5
    return np.array([dN1, dN2])

def evalDerivOfShapeFunct(PolynomialDegree, xi):
    """ Compute the derivative of the shape function N at coordinate xi. """
    NodalModesDeriv = evalNodalModesDeriv()
    EdgeModesDeriv = evalEdgeModesDeriv(PolynomialDegree, xi)
    return np.concatenate([NodalModesDeriv, EdgeModesDeriv])







