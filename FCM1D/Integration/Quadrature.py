import numpy as np
from dataclasses import dataclass

from AdaptiveRefinement.partition import partition
from Integration.GaussQuadrature.GaussCoordinates import GaussQuadratureCoordinates
from Integration.GaussQuadrature.GaussWeights import GaussQuadratureWeights
from Integration.IntegrationSubdomain.LocalToGlobal import LocalToGlobal
from Integration.IntegrationSubdomain.calcDeterminantJacobian import calcDeterminantJacobian
from Integration.IntegrationSubdomain.calcDetJacobiandomain import calcDetJacobianDomain


@dataclass(frozen=True, eq=False)
class ElementQuadrature:
    xi: np.ndarray
    w: np.ndarray
    x: np.ndarray
    mat: np.ndarray
    n_subdomains: int


def build_element_quadrature(element, cfg):
    xi_ref = GaussQuadratureCoordinates(cfg.n_gauss)
    w_ref = GaussQuadratureWeights(cfg.n_gauss)
    a = element.global_coordinates

    xi, w, x, mat = [], [], [], []
    sub_domains = partition(element, cfg)
    for sub in sub_domains:
        for xr, wr in zip(xi_ref, w_ref):
            p = LocalToGlobal(xr, sub)
            weight = wr * calcDeterminantJacobian(xr, sub) * calcDetJacobianDomain(a, p)
            xg = LocalToGlobal(p, a)
            xi.append(p)
            w.append(weight)
            x.append(xg)
            mat.append(cfg.material_factor(cfg.domain_index(xg)))

    return ElementQuadrature(np.asarray(xi, dtype=float),
                             np.asarray(w, dtype=float),
                             np.asarray(x, dtype=float),
                             np.asarray(mat, dtype=float),
                             len(sub_domains))