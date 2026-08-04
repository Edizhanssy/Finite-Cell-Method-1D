import numpy as np
from numpy.polynomial import legendre as Leg
from Element.ShapeFunctions.calcDerivativeofShapeFunction import (
    legendre_polynomial, derivative_legendre_polynomial)

xi = 0.3
print(f"{'n':>3} {'P (kod)':>13} {'P (numpy)':>13} {'dP (kod)':>13} {'dP (numpy)':>13}")
for n in range(8):
    b = Leg.Legendre.basis(n)
    print(f"{n:3d} {legendre_polynomial(n, xi):13.8f} {b(xi):13.8f} "
          f"{derivative_legendre_polynomial(n, xi):13.8f} {b.deriv()(xi):13.8f}")