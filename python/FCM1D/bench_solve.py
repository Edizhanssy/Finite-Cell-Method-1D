"""Python ve (varsa) C++ cozucusunu min-of-N ile olcer."""
import csv
import os
import re
import subprocess
import sys
import time

from config import Config
from fcm_solver import solve
from paths import RESULTDIR

REPS = 50
cfg = Config()

r = solve(cfg)                       # isinma + DOF
dof = r['DOF']

times = []
for _ in range(REPS):
    t0 = time.perf_counter()
    solve(cfg)
    times.append(time.perf_counter() - t0)
times.sort()

py_best, py_med = times[0], times[len(times) // 2]
print(f'python  best {py_best*1e3:8.3f} ms   median {py_med*1e3:8.3f} ms   (n={REPS}, DOF={dof})')

rows = [dict(impl='python', dof=dof, reps=REPS,
             best_ms=py_best * 1e3, median_ms=py_med * 1e3,
             mesh_ms='', quad_ms='', asm_ms='', solve_ms='')]

if len(sys.argv) > 1:
    out = subprocess.run([sys.argv[1], str(REPS)], capture_output=True, text=True).stdout
    m = re.search(r'timing \(min of (\d+), s\):\s+mesh (\S+)\s+quad (\S+)\s+'
                  r'asm (\S+)\s+solve (\S+)\s+total (\S+)', out)
    if not m:
        print('C++ zamanlama satiri bulunamadi:\n' + out)
    else:
        n, mesh, quad, asm, slv, tot = m.groups()
        cpp_best = float(tot)
        print(f'c++     best {cpp_best*1e3:8.3f} ms   '
              f'(n={n})  mesh {float(mesh)*1e3:.3f}  quad {float(quad)*1e3:.3f}  '
              f'asm {float(asm)*1e3:.3f}  solve {float(slv)*1e3:.3f}')
        print(f'\nhizlanma: {py_best / cpp_best:.1f}x')
        rows.append(dict(impl='cpp', dof=dof, reps=int(n),
                         best_ms=cpp_best * 1e3, median_ms='',
                         mesh_ms=float(mesh) * 1e3, quad_ms=float(quad) * 1e3,
                         asm_ms=float(asm) * 1e3, solve_ms=float(slv) * 1e3))

with open(os.path.join(RESULTDIR, 'timing.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print(f'\nwritten: {os.path.join(RESULTDIR, "timing.csv")}')
