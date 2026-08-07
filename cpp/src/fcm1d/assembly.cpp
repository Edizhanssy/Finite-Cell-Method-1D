#include "fcm/fcm1d/assembly.hpp"

#include "fcm/core/legendre.hpp"

namespace fcm {

std::vector<double> element_stiffness(const Element1D& el, const Config& cfg,
                                      const ElementQuadrature& q) {
    const int    nm = cfg.n_modes();
    const double EA = cfg.E * cfg.A;
    const double J  = 0.5 * (el.global_[1] - el.global_[0]);

    std::vector<double> Ke(static_cast<std::size_t>(nm) * nm, 0.0);
    std::vector<double> B(static_cast<std::size_t>(nm));

    for (std::size_t k = 0; k < q.xi.size(); ++k) {
        const std::vector<double> dN = shape_function_derivs(cfg.p, q.xi[k]);
        for (int i = 0; i < nm; ++i) B[static_cast<std::size_t>(i)] = dN[static_cast<std::size_t>(i)] / J;

        const double Mat = EA * q.mat[k];
        const double w   = q.w[k];
        for (int i = 0; i < nm; ++i) {
            const double ti = B[static_cast<std::size_t>(i)] * Mat;
            for (int j = 0; j < nm; ++j)
                Ke[static_cast<std::size_t>(i) * nm + j] +=
                    (ti * B[static_cast<std::size_t>(j)]) * w;
        }
    }
    return Ke;
}

std::vector<double> element_force(const Config& cfg, const ElementQuadrature& q) {
    const int nm = cfg.n_modes();
    std::vector<double> Fe(static_cast<std::size_t>(nm), 0.0);

    for (std::size_t k = 0; k < q.xi.size(); ++k) {
        const std::vector<double> N = shape_functions(cfg.p, q.xi[k]);
        const double f = cfg.body_load(q.x[k]);
        const double w = q.w[k];
        for (int i = 0; i < nm; ++i)
            Fe[static_cast<std::size_t>(i)] += (N[static_cast<std::size_t>(i)] * f) * w;
    }
    return Fe;
}

DenseMatrix assemble_stiffness(const Mesh& m, const Config& cfg,
                               const std::vector<ElementQuadrature>& quads) {
    DenseMatrix K(m.n_dof);
    const int nm = cfg.n_modes();
    for (std::size_t e = 0; e < m.elements.size(); ++e) {
        const std::vector<double> Ke = element_stiffness(m.elements[e], cfg, quads[e]);
        const std::vector<int>&   L  = m.ltog[e];
        for (int i = 0; i < nm; ++i)
            for (int j = 0; j < nm; ++j)
                K(L[static_cast<std::size_t>(i)], L[static_cast<std::size_t>(j)]) +=
                    Ke[static_cast<std::size_t>(i) * nm + j];
    }
    return K;
}

std::vector<double> assemble_force(const Mesh& m, const Config& cfg,
                                   const std::vector<ElementQuadrature>& quads) {
    std::vector<double> F(static_cast<std::size_t>(m.n_dof), 0.0);
    const int nm = cfg.n_modes();
    for (std::size_t e = 0; e < m.elements.size(); ++e) {
        const std::vector<double> Fe = element_force(cfg, quads[e]);
        const std::vector<int>&   L  = m.ltog[e];
        for (int i = 0; i < nm; ++i)
            F[static_cast<std::size_t>(L[static_cast<std::size_t>(i)])] +=
                Fe[static_cast<std::size_t>(i)];
    }
    return F;
}

}