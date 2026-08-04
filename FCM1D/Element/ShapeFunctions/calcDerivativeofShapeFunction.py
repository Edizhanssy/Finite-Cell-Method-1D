import numpy as np

def legendre_and_derivs(n_max, xi):
    n_max = int(n_max)
    P = np.zeros(n_max + 1)
    dP = np.zeros(n_max + 1)
    P[0], dP[0] = 1.0, 0.0
    if n_max >= 1:
        P[1], dP[1] = xi, 1.0
    for n in range(2, n_max + 1):
        P[n] = ((2*n - 1) * xi * P[n-1] - (n - 1) * P[n-2]) / n
        dP[n] = ((2*n - 1) * (P[n-1] + xi * dP[n-1]) - (n - 1) * dP[n-2]) / n
    return P, dP


def legendre_polynomial(n, x):
    P, _ = legendre_and_derivs(n, x)
    return P[n]


def derivative_legendre_polynomial(n, x):
    _, dP = legendre_and_derivs(n, x)
    return dP[n]


def evalDerivOfN(i, xi):
    _, dP = legendre_and_derivs(i, xi)
    return (dP[i] - dP[i - 2]) / np.sqrt(4 * i - 2)


def evalNodalModesDeriv():
    return np.array([-0.5, 0.5])


def evalEdgeModesDeriv(PolynomialDegree, xi):
    p = int(PolynomialDegree)
    _, dP = legendre_and_derivs(p, xi)
    modes = np.zeros(p - 1)
    for i in range(1, p):
        n = i + 1                      # n = 2 .. p
        modes[i - 1] = (dP[n] - dP[n - 2]) / np.sqrt(4 * n - 2)
    return modes


def evalDerivOfShapeFunct(PolynomialDegree, xi):
    return np.concatenate([evalNodalModesDeriv(),
                           evalEdgeModesDeriv(PolynomialDegree, xi)])







