#pragma once
#include <array>
#include <vector>

#include "fcm/fcm1d/config.hpp"
#include "fcm/fcm1d/mesh.hpp"

namespace fcm {

inline double local_to_global(double xi, const std::array<double, 2>& seg) {
    return 0.5 * ((1.0 - xi) * seg[0] + (1.0 + xi) * seg[1]);
}

std::vector<std::array<double, 2>> partition_element(const Element1D& el, const Config& cfg);

}