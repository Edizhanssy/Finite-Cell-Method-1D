"""Yakinsama figurleri: p ve quadrature derinligi."""
import csv
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from paths import FIGDIR, RESULTDIR


def read(name):
    with open(os.path.join(RESULTDIR, name)) as f:
        return list(csv.DictReader(f))


pr = read('sweep_p.csv')
p = np.array([int(r['p']) for r in pr])
ep = np.array([float(r['rel_err']) for r in pr])

dr = read('sweep_depth.csv')
d = np.array([int(r['depth']) for r in dr])
ed = np.abs(np.array([float(r['force_residual']) for r in dr]))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

ax1.loglog(p, ep, 'o-', label='measured')
C = ep[-1] * p[-1] ** 3
ax1.loglog(p, C * p.astype(float) ** -3.0, 'k--', lw=0.9, label=r'$p^{-3}$')
ax1.axvline(6, color='gray', lw=0.8, ls=':')
ax1.annotate('smooth part\nresolved', xy=(3.6, 2e-6), fontsize=8, color='gray')
ax1.annotate('singularity-limited', xy=(9, 3e-8), fontsize=8, color='gray')
ax1.set_xlabel('polynomial degree $p$')
ax1.set_ylabel('relative error in $\\bar\\varepsilon_{fict}$')
ax1.set_title('p-refinement')
ax1.grid(True, which='both', alpha=0.3)
ax1.legend()

ax2.semilogy(d, ed, 'o-', label='measured')
C2 = ed[-1] * 4.0 ** d[-1]
ax2.semilogy(d, C2 * 4.0 ** (-d.astype(float)), 'k--', lw=0.9, label=r'$h^{2}$')
ax2.set_xlabel('bisection depth')
ax2.set_ylabel('residual nodal force')
ax2.set_title('quadrature refinement')
ax2.grid(True, which='both', alpha=0.3)
ax2.legend()

plt.tight_layout()
out = os.path.join(FIGDIR, 'convergence.png')
plt.savefig(out, dpi=150)
print('saved:', out)