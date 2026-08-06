import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIGDIR = os.path.join(REPO_ROOT, 'figures')
RESULTDIR = os.path.join(REPO_ROOT, 'results')
REFDIR = os.path.join(REPO_ROOT, 'reference')

for _d in (FIGDIR, RESULTDIR, REFDIR):
    os.makedirs(_d, exist_ok=True)