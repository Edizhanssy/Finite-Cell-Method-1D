//
// Created by Edizhan Yildiz on 06.08.26.
//

#include "fcm/core/gauss.hpp"
#include "fcm/core/legendre.hpp"

#include <cmath>
#include <stdexcept>

namespace fcm {

    namespace {
        constexpr double kPi = 3.14159265358979323846;
    }

    GaussRule gauss_legendre(int n) {
        if (n < 1) throw std::invalid_argument("gauss_legendre: n < 1");

        GaussRule r;
        r.points.assign(static_cast<std::size_t>(n), 0.0);
        r.weights.assign(static_cast<std::size_t>(n), 0.0);

        const int half = (n + 1) / 2;
        for (int i = 0; i < half; ++i) {

            // Asymptotic beginning estimate!
            double x = std::cos(kPi * (static_cast<double>(i) + 0.75)
                                / (static_cast<double>(n) + 0.5));

            for (int it = 0; it < 100; ++it) {
                const LegendreValues v = legendre_and_derivs(n, x);
                const double dx = -v.P[n] / v.dP[n];
                x += dx;
                if (std::fabs(dx) < 1e-16) break;
            }

            const LegendreValues v = legendre_and_derivs(n, x);
            const double w = 2.0 / ((1.0 - x * x) * v.dP[n] * v.dP[n]);

            r.points[i]              = -x;
            r.points[n - 1 - i]      =  x;
            r.weights[i]             =  w;
            r.weights[n - 1 - i]     =  w;
        }
        return r;
    }

}