import matplotlib.pyplot as plt

from config import Config
from fcm_solver import run

if __name__ == '__main__':
    cfg = Config()
    xf0, xf1 = cfg.fictitious_span
    res = run(cfg)
    u = res['u']

    print('domain boundaries in local coordinates [-1, 1]: ',
          [(cfg.to_local(a), cfg.to_local(b)) for a, b, _ in cfg.domains])
    print('the total Degree of Freedom of the whole domain: ', res['DOF'])
    print(f"nodal DOF force sum = {res['nodal_force_sum']:.3e}   expected ~0")
    print('the ill-conditioning of the constrained stiffness matrix: ', res['kappa'])
    print(f"u(0)   = {u[0.0]:12.6e}   expected  0")
    print(f"u(1)   = {u[xf0]:12.6e}   expected -3.9789e-03")
    print(f"u(7/3) = {u[xf1]:12.6e}   expected -1")
    print(f"u(3)   = {u[cfg.L]:12.6e}   expected -1")
    print(f"mean strain in fictitious = {res['mean_strain_disp']:8.5f}   expected -0.74702")
    print(f"mean strain (from strain field) = {res['mean_strain_field']:8.5f}   expected -0.74702")
    print('element 1 right end:', res['strains'][res['samples'] - 1],
          '| element 2 left end:', res['strains'][res['samples']])

    for pos, eps in res['per_element']:
        plt.plot(pos, eps, lw=1.2, color='tab:blue')
    plt.axhline(-0.75, ls='--', lw=0.8, color='gray')
    plt.axvspan(xf0, xf1, alpha=0.12, color='gray')
    plt.xlabel('Global Position')
    plt.ylabel('Axial strain')
    plt.title('Axial Strain Distribution along the uni-axial rod')
    plt.grid(True)
    plt.savefig('../figures/axial_strain.png', dpi=150)
    plt.show()





