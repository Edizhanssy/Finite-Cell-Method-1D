import numpy as np
def legendre_polynomial(n, x):
    if n == 0:
        return 1
    elif n == 1:
        return x
    else:
        return ((2*n - 1)*x*legendre_polynomial(n-1, x) - (n - 1)*legendre_polynomial(n-2, x)) / n
def derivative_legendre_polynomial(n, x):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return ((2*n - 1) * (legendre_polynomial(n-1, x) + x * derivative_legendre_polynomial(n-1, x)) - n * derivative_legendre_polynomial(n-2, x)) / n
def evalDerivOfN(i, xi):
    return 1 / np.sqrt(4 * i - 2) * (derivative_legendre_polynomial(i, xi) - derivative_legendre_polynomial(i - 2, xi))
def evalEdgeModesDeriv(PolynomialDegree, xi):
    EdgeModesDeriv = np.zeros(PolynomialDegree - 1)
    for i in range(1, PolynomialDegree):
        EdgeModesDeriv[i - 1] = evalDerivOfN(i + 1, xi)
    return EdgeModesDeriv
def evalNodalModesDeriv():
    dN1 = -0.5
    dN2 = 0.5
    return np.array([dN1, dN2])
def evalDerivOfShapeFunct(PolynomialDegree, xi):
    NodalModesDeriv = evalNodalModesDeriv()
    EdgeModesDeriv = evalEdgeModesDeriv(PolynomialDegree, xi)
    return np.concatenate([NodalModesDeriv, EdgeModesDeriv])







