"""max_depth ve p yakinsama calismalari."""
import csv, os
from dataclasses import replace

from config import Config
from fcm_solver import run
from paths import RESULTDIR


def write_csv(name, rows):
    with open(os.path.join(RESULTDIR, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


base = Config()
xf0, xf1 = base.fictitious_span
limit = (base.disp_load + base.load_amp / base.load_freq) / (xf1 - xf0)
print(f'analytic limit = {limit:.15f}')

print(f'\n--- quadrature depth (p={base.p}, alpha={base.alpha:g}) ---')
print(f'{"depth":>6} {"subdom":>7} {"force residual":>16} {"mean":>20}')
rows = []
for d in (4, 6, 8, 10, 12, 14, 16, 18):
    r = run(replace(base, max_depth=d), samples=50)
    rows.append(dict(depth=d, subdomains=r['quads'][0].n_subdomains,
                     force_residual=r['nodal_force_sum'],
                     mean=r['mean_strain_disp']))
    print(f'{d:6d} {rows[-1]["subdomains"]:7d} '
          f'{rows[-1]["force_residual"]:16.3e} {rows[-1]["mean"]:20.14f}')
write_csv('sweep_depth.csv', rows)

pbase = replace(base, alpha=1e-12)
print('\n--- polynomial degree (alpha=1e-12) ---')
print(f'{"p":>4} {"DOF":>5} {"mean":>20} {"rel.err":>10}')
rows = []
for p in (7, 8, 10, 11, 13, 15, 20):
    r = run(replace(pbase, p=p), samples=50)
    err = abs(r['mean_strain_disp'] - limit) / abs(limit)
    rows.append(dict(p=p, dof=r['DOF'], mean=r['mean_strain_disp'], rel_err=err))
    print(f'{p:4d} {r["DOF"]:5d} {r["mean_strain_disp"]:20.14f} {err:10.2e}')
write_csv('sweep_p.csv', rows)

print(f'\nwritten: {RESULTDIR}')