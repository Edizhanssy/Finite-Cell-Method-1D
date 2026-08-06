#include "fcm/fcm1d/solver.hpp"

#include "fcm/core/linalg.hpp"
#include <cmath>
#include <stdexcept>
#include "fcm/core/legendre.hpp"

namespace fcm {
    namespace {

        void apply_penalty(DenseMatrix& K, std::vector<double>& F,
                           int dof0, double value, double penalty) {
            K(dof0, dof0) += penalty;
            F[static_cast<std::size_t>(dof0)] += penalty * value;
        }

    }  // namespace

    SolveResult solve(const Config& cfg) {
        SolveResult r;
        r.mesh = build_mesh(cfg);
        for (const Element1D& el : r.mesh.elements)
            r.quads.push_back(build_element_quadrature(el, cfg));

        r.K = assemble_stiffness(r.mesh, cfg, r.quads);
        r.F = assemble_force(r.mesh, cfg, r.quads);

        for (int i = 0; i <= cfg.n_elements; ++i)
            r.nodal_force_sum += r.F[static_cast<std::size_t>(r.mesh.node_dof[static_cast<std::size_t>(i)] - 1)];

        apply_penalty(r.K, r.F, r.mesh.node_dof.front() - 1, 0.0,            cfg.penalty);
        apply_penalty(r.K, r.F, r.mesh.node_dof.back()  - 1, cfg.disp_load,  cfg.penalty);

        r.u = solve_dense(r.K, r.F);
        return r;
    }

    double displacement_at(const Config& cfg, const Mesh& m,
                       const std::vector<double>& u, double x) {
        for (std::size_t e = 0; e < m.elements.size(); ++e) {
            const double x1 = m.elements[e].global_[0];
            const double x2 = m.elements[e].global_[1];
            if (x1 - 1e-12 <= x && x <= x2 + 1e-12) {
                const double xi = 2.0 * (x - x1) / (x2 - x1) - 1.0;
                const std::vector<double> N = shape_functions(cfg.p, xi);
                double s = 0.0;
                for (int i = 0; i < cfg.n_modes(); ++i)
                    s += N[static_cast<std::size_t>(i)] *
                         u[static_cast<std::size_t>(m.ltog[e][static_cast<std::size_t>(i)])];
                return s;
            }
        }
        throw std::runtime_error("displacement_at: nokta hicbir elemanda degil");
    }

    StrainField strain_field(const Config& cfg, const Mesh& m,
                             const std::vector<double>& u, int samples) {
        StrainField f;
        for (std::size_t e = 0; e < m.elements.size(); ++e) {
            const double x1 = m.elements[e].global_[0];
            const double x2 = m.elements[e].global_[1];
            const double J  = 0.5 * (x2 - x1);
            for (int k = 0; k < samples; ++k) {
                const double xi = -1.0 + 2.0 * k / (samples - 1);
                const std::vector<double> dN = shape_function_derivs(cfg.p, xi);
                double s = 0.0;
                for (int i = 0; i < cfg.n_modes(); ++i)
                    s += dN[static_cast<std::size_t>(i)] *
                         u[static_cast<std::size_t>(m.ltog[e][static_cast<std::size_t>(i)])];
                f.pos.push_back(x1 + (xi + 1.0) * J);
                f.eps.push_back(s / J);
            }
        }
        return f;
    }


}  // namespace fcm