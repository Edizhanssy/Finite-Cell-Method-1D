import csv
from dataclasses import replace

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from config import Config
from fcm_solver import run


def analytic_mean_strain(cfg):
    EA = cfg.E * cfg.A
    Lp = sum(x1 - x0 for x0, x1, m in cfg.domains if m == 0)
    xf0, xf1 = cfg.fictitious_span
    Lf = xf1 - xf0
    I = cfg.load_amp / cfg.load_freq
    return (cfg.disp_load + I / EA) / (cfg.alpha * Lp / EA + Lf / EA)


base = Config()
limit = analytic_mean_strain(replace(base, alpha=0.0))
rows = []

for a in np.logspace(-1, -14, 27):
    cfg = replace(base, alpha=float(a))
    res = run(cfg, samples=200)
    exact = analytic_mean_strain(cfg)
    num = res['mean_strain_disp']
    row = dict(alpha=float(a), kappa=res['kappa'], num=num, exact=exact,
               err_num=abs(num - exact) / abs(exact),
               err_model=abs(exact - limit) / abs(limit),
               err_total=abs(num - limit) / abs(limit))
    rows.append(row)
    print(f"a={a:8.1e}  k={row['kappa']:10.3e}  mean={num: .8f}  "
          f"exact={exact: .8f}  e_num={row['err_num']:.2e}  e_mod={row['err_model']:.2e}")

with open('sweep_alpha.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

al = np.array([r['alpha'] for r in rows])
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

ax1.loglog(al, [r['kappa'] for r in rows], 'o-')
ax1.set_xlabel(r'$\alpha$'); ax1.set_ylabel(r'$\kappa(K)$')
ax1.set_title('Condition number'); ax1.grid(True, which='both', alpha=0.3)
ax1.invert_xaxis()

ax2.loglog(al, [r['err_model'] for r in rows], 's--', label='modelling error')
ax2.loglog(al, [r['err_num'] for r in rows], '^--', label='numerical error')
ax2.loglog(al, [r['err_total'] for r in rows], 'o-', label='total')
ax2.set_xlabel(r'$\alpha$'); ax2.set_ylabel('relative error')
ax2.set_title('Error trade-off'); ax2.grid(True, which='both', alpha=0.3)
ax2.legend(); ax2.invert_xaxis()

plt.tight_layout()
plt.savefig('alpha_sweep.png', dpi=150)
print('saved: alpha_sweep.png')