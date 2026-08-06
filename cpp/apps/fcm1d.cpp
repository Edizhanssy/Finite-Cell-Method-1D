#include <cmath>
#include <cstdio>
#include <vector>
#include <array>
#include "fcm/fcm1d/solver.hpp"
#include <algorithm>
#include <cstdlib>

int main(int argc, char** argv) {
    const fcm::Config cfg;
    const fcm::SolveResult r = fcm::solve(cfg);
    const std::array<double, 2> fs = cfg.fictitious_span();
    const int reps = (argc > 1) ? std::atoi(argv[1]) : 0;

    const double u0 = fcm::displacement_at(cfg, r.mesh, r.u, 0.0);
    const double u1 = fcm::displacement_at(cfg, r.mesh, r.u, fs[0]);
    const double u2 = fcm::displacement_at(cfg, r.mesh, r.u, fs[1]);
    const double u3 = fcm::displacement_at(cfg, r.mesh, r.u, cfg.L);

    const fcm::StrainField f = fcm::strain_field(cfg, r.mesh, r.u);
    double integral = 0.0;
    for (std::size_t k = 1; k < f.pos.size(); ++k) {
        if (f.pos[k - 1] < fs[0] || f.pos[k] > fs[1]) continue;
        integral += 0.5 * (f.eps[k - 1] + f.eps[k]) * (f.pos[k] - f.pos[k - 1]);
    }

    const double mean_field = integral / (fs[1] - fs[0]);
    const double mean_disp  = (u2 - u1) / (fs[1] - fs[0]);

    std::printf("the total Degree of Freedom of the whole domain:  %d\n", r.mesh.n_dof);
    std::printf("nodal DOF force sum = %.3e   expected ~0\n", r.nodal_force_sum);
    std::printf("u(0)   = %12.6e   expected  0\n", u0);
    std::printf("u(1)   = %12.6e   expected -3.9789e-03\n", u1);
    std::printf("u(7/3) = %12.6e   expected -1\n", u2);
    std::printf("u(3)   = %12.6e   expected -1\n", u3);

    std::printf("timing (single run, s):  mesh %.6f  quad %.6f  asm %.6f  solve %.6f  total %.6f\n",
                r.t.mesh, r.t.quadrature, r.t.assembly, r.t.bc_solve, r.t.total);

    if (reps > 0) {
        fcm::Timings best{1e9, 1e9, 1e9, 1e9, 1e9};
        for (int i = 0; i < reps; ++i) {
            const fcm::SolveResult s = fcm::solve(cfg);
            best.mesh       = std::min(best.mesh,       s.t.mesh);
            best.quadrature = std::min(best.quadrature, s.t.quadrature);
            best.assembly   = std::min(best.assembly,   s.t.assembly);
            best.bc_solve   = std::min(best.bc_solve,   s.t.bc_solve);
            best.total      = std::min(best.total,      s.t.total);
        }
        std::printf("timing (min of %d, s):   mesh %.6f  quad %.6f  asm %.6f  solve %.6f  total %.6f\n",
                    reps, best.mesh, best.quadrature, best.assembly, best.bc_solve, best.total);
    }

    std::printf("mean strain in fictitious = %8.5f   expected -0.74702\n", mean_disp);
    std::printf("mean strain (from strain field) = %8.5f   expected -0.74702\n", mean_field);
    return 0;
}
