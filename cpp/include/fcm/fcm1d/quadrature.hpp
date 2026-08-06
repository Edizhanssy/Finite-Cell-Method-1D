#pragma once
#include <vector>

#include "fcm/fcm1d/config.hpp"
#include "fcm/fcm1d/mesh.hpp"

namespace fcm {

/// Geometriye bagli, integrand'dan bagimsiz. Eleman basina bir kez uretilir.
struct ElementQuadrature {
    std::vector<double> xi;    // eleman-yerel koordinat [-1,1]
    std::vector<double> w;     // agirlik (alt-domain + eleman Jacobian'lari dahil)
    std::vector<double> x;     // global koordinat
    std::vector<double> mat;   // malzeme carpani: 1.0 veya alpha
    int n_subdomains = 0;
};

ElementQuadrature build_element_quadrature(const Element1D& el, const Config& cfg);

}