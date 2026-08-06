"""C++ portunun dogrulama icin kullanacagi referans degerleri uretir."""
import os
import numpy as np

from config import Config
from fcm_solver import solve
from Element.ShapeFunctions.calcDerivativeofShapeFunction import (
    legendre_and_derivs, evalShapeFunct, evalDerivOfShapeFunct)
from Element.StiffnessMatrix.ElementalStiffness import calculate_element_stiffness
from Element.ForceVector.assembleGlobalForceVector import assemble_Force_Vector
from Integration.GaussQuadrature.GaussCoordinates import GaussQuadratureCoordinates
from Integration.GaussQuadrature.GaussWeights import GaussQuadratureWeights

from paths import REFDIR

XI = [-1.0, -0.9, -0.5, -0.3, 0.0, 0.1, 0.3, 0.7, 0.95, 1.0]


def dump(name, header, rows):
    with open(os.path.join(REFDIR, name), 'w') as f:
        f.write('# ' + header + '\n')
        for r in rows:
            f.write(' '.join('%.17g' % v if isinstance(v, float) else str(v)
                             for v in r) + '\n')
    print(f'{name:22s} {len(rows):6d} rows')


cfg = Config()

rows = []
for xi in XI:
    P, dP = legendre_and_derivs(cfg.p, xi)
    for n in range(cfg.p + 1):
        rows.append((n, xi, float(P[n]), float(dP[n])))
dump('legendre.txt', 'n xi P dP', rows)

rows = []
for xi in XI:
    N, dN = evalShapeFunct(cfg.p, xi), evalDerivOfShapeFunct(cfg.p, xi)
    for i in range(len(N)):
        rows.append((cfg.p, xi, i, float(N[i]), float(dN[i])))
dump('shapefunc.txt', 'p xi i N dN', rows)

rows = []
for n in sorted(Config._GAUSS_N):
    pts, wts = GaussQuadratureCoordinates(n), GaussQuadratureWeights(n)
    assert len(pts) == n and len(wts) == n, f'n={n} tabloda eksik'
    for i in range(len(pts)):
        rows.append((n, i, float(pts[i]), float(wts[i])))
dump('gauss.txt', 'n i point weight', rows)

res = solve(cfg)

rows = []
for e, lm in enumerate(res['LtoG']):
    for i, d in enumerate(np.array(lm).flatten()):
        rows.append((e, i, int(d)))
dump('ltog_1d.txt', 'element i dof', rows)

rows = []
for e, q in enumerate(res['quads']):
    for i in range(q.xi.size):
        rows.append((e, i, float(q.xi[i]), float(q.w[i]),
                     float(q.x[i]), float(q.mat[i])))
dump('quadrature_1d.txt', 'element i xi w x mat', rows)

rows = []
for e, (el, q) in enumerate(zip(res['elements'], res['quads'])):
    Ke = calculate_element_stiffness(el, cfg, q)
    for i in range(Ke.shape[0]):
        for j in range(Ke.shape[1]):
            rows.append((e, i, j, float(Ke[i, j])))
dump('stiffness_1d.txt', 'element i j Ke', rows)

F = assemble_Force_Vector(res['elements'], res['DOF'], res['LtoG'], cfg, res['quads'])
dump('force_1d.txt', 'dof F', [(i, float(F[i, 0])) for i in range(F.shape[0])])

dump('solution_1d.txt', 'dof u',
     [(i, float(res['solution'][i])) for i in range(res['solution'].size)])

print(f"\nDOF={res['DOF']}  kappa={res['kappa']:.15g}  "
      f"subdomains={[q.n_subdomains for q in res['quads']]}")