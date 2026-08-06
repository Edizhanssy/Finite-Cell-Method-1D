//
// Created by Edizhan Yildiz on 06.08.26.
//

#include "fcm/core/legendre.hpp"

#include <cmath>
#include <stdexcept>

namespace fcm {

    LegendreValues legendre_and_derivs(int n_max, double xi) {
        if (n_max < 0) throw std::invalid_argument("legendre_and_derivs: n_max < 0");

        LegendreValues v;
        v.P.assign(static_cast<std::size_t>(n_max) + 1, 0.0);
        v.dP.assign(static_cast<std::size_t>(n_max) + 1, 0.0);

        v.P[0]  = 1.0;
        v.dP[0] = 0.0;
        if (n_max >= 1) {
            v.P[1]  = xi;
            v.dP[1] = 1.0;
        }
        for (int n = 2; n <= n_max; ++n) {
            const double dn = static_cast<double>(n);
            v.P[n]  = ((2.0 * dn - 1.0) * xi * v.P[n - 1]
                       - (dn - 1.0) * v.P[n - 2]) / dn;
            v.dP[n] = ((2.0 * dn - 1.0) * (v.P[n - 1] + xi * v.dP[n - 1])
                       - (dn - 1.0) * v.dP[n - 2]) / dn;
        }
        return v;
    }

    std::vector<double> shape_functions(int p, double xi) {
        if (p < 1) throw std::invalid_argument("shape_functions: p < 1");
        const LegendreValues v = legendre_and_derivs(p, xi);

        std::vector<double> N(static_cast<std::size_t>(p) + 1);
        N[0] = 0.5 * (1.0 - xi);
        N[1] = 0.5 * (1.0 + xi);
        for (int i = 1; i < p; ++i) {
            const int n = i + 1;                       // n = 2 .. p
            N[static_cast<std::size_t>(i) + 1] =
                (v.P[n] - v.P[n - 2]) / std::sqrt(4.0 * n - 2.0);
        }
        return N;
    }

    std::vector<double> shape_function_derivs(int p, double xi) {
        if (p < 1) throw std::invalid_argument("shape_function_derivs: p < 1");
        const LegendreValues v = legendre_and_derivs(p, xi);

        std::vector<double> dN(static_cast<std::size_t>(p) + 1);
        dN[0] = -0.5;
        dN[1] =  0.5;
        for (int i = 1; i < p; ++i) {
            const int n = i + 1;
            dN[static_cast<std::size_t>(i) + 1] =
                (v.dP[n] - v.dP[n - 2]) / std::sqrt(4.0 * n - 2.0);
        }
        return dN;
    }

}
