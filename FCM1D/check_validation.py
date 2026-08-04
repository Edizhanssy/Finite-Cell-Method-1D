import os, re, subprocess, sys

env = dict(os.environ, MPLBACKEND='Agg')
res = subprocess.run([sys.executable, '1DFCM.py'],
                     capture_output=True, text=True, env=env)
out = res.stdout

def grab(label):
    m = re.search(re.escape(label) + r'\s*=?\s*(-?\d+\.?\d*(?:[eE][-+]?\d+)?)', out)
    if not m:
        print(f'CANNOT FIND: {label}\n--- stdout ---\n{out}\n--- stderr ---\n{res.stderr}')
        sys.exit(2)
    return float(m.group(1))

CHECKS = [
    ('u(0)',                            0.0,           1e-10),
    ('u(1)',                           -3.978887e-03,  1e-8),
    ('u(7/3)',                         -1.0,           1e-6),
    ('u(3)',                           -1.0,           1e-6),
    ('mean strain in fictitious',      -0.74702,       1e-5),
    ('mean strain (from strain field)',-0.74693,       1e-4),
]

ok = True
for label, expected, tol in CHECKS:
    got = grab(label)
    good = abs(got - expected) <= tol
    ok &= good
    print(f'{"PASS" if good else "FAIL"}  {label:34s} {got: .8e}  expected {expected: .8e}')

print('--- ALL PASSED ---' if ok else '--- REGRESSION ---')
sys.exit(0 if ok else 1)
