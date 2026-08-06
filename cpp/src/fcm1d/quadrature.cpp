#include "fcm/fcm1d/quadrature.hpp"

#include <cmath>

#include "fcm/core/gauss.hpp"
#include "fcm/fcm1d/partition.hpp"

namespace fcm {

    ElementQuadrature build_element_quadrature(const Element1D& el, const Config& cfg) {
        const GaussRule rule = gauss_legendre(cfg.n_gauss());
        const std::vector<std::array<double, 2>> subs = partition_element(el, cfg);

        const double j_elem = 0.5 * std::fabs(el.global_[0] - el.global_[1]);

        ElementQuadrature q;
        q.n_subdomains = static_cast<int>(subs.size());
        const std::size_t total = subs.size() * rule.points.size();
        q.xi.reserve(total);
        q.w.reserve(total);
        q.x.reserve(total);
        q.mat.reserve(total);

        for (const std::array<double, 2>& sub : subs) {
            const double j_sub = 0.5 * std::fabs(sub[0] - sub[1]);
            for (std::size_t k = 0; k < rule.points.size(); ++k) {
                const double xi = local_to_global(rule.points[k], sub);
                const double w  = rule.weights[k] * j_sub * j_elem;
                const double xg = local_to_global(xi, el.global_);
                q.xi.push_back(xi);
                q.w.push_back(w);
                q.x.push_back(xg);
                q.mat.push_back(cfg.material_factor(cfg.domain_index(xg)));
            }
        }
        return q;
    }

}  // namespace fcm