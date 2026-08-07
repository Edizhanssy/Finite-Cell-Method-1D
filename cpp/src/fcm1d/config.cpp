//
// Created by Edizhan Yildiz on 06.08.26.
//

#include "fcm/fcm1d/config.hpp"

#include <cmath>
#include <stdexcept>

namespace fcm {

    int Config::domain_index(double x) const {
        for (const DomainSpan& d : domains)
            if (d.x0 <= x && x <= d.x1) return d.material;
        return -1;
    }

    double Config::material_factor(int material) const {
        if (material == 0) return 1.0;
        if (material == 1) return alpha;
        throw std::runtime_error("undefined material id");
    }

    double Config::body_load(double x) const {
        if (load_span0 <= x && x <= load_span1)
            return load_amp * std::sin(load_freq * x);
        return 0.0;
    }

    std::array<double, 2> Config::fictitious_span() const {
        for (const DomainSpan& d : domains)
            if (d.material == 1) return {d.x0, d.x1};
        throw std::runtime_error("fictitious domain is not defined");
    }

}
