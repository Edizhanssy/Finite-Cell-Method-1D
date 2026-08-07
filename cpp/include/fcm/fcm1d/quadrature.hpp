#pragma once
#include <vector>

#include "fcm/fcm1d/config.hpp"
#include "fcm/fcm1d/mesh.hpp"

namespace fcm {

struct ElementQuadrature {
    std::vector<double> xi;    // element local coordinates [-1,1]
    std::vector<double> w;     // weight
    std::vector<double> x;     // global coordinates
    std::vector<double> mat;   // penalization parameter
    int n_subdomains = 0;
};

ElementQuadrature build_element_quadrature(const Element1D& el, const Config& cfg);

}