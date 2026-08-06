#pragma once
#include <cstddef>
#include <vector>

#include "fcm/fcm1d/config.hpp"
#include "fcm/fcm1d/mesh.hpp"
#include "fcm/fcm1d/quadrature.hpp"

namespace fcm {

struct DenseMatrix {
    int n = 0;
    std::vector<double> a;
    DenseMatrix() = default;
    explicit DenseMatrix(int n_)
        : n(n_), a(static_cast<std::size_t>(n_) * n_, 0.0) {}
    double& operator()(int i, int j) { return a[static_cast<std::size_t>(i) * n + j]; }
    double  operator()(int i, int j) const { return a[static_cast<std::size_t>(i) * n + j]; }
};

std::vector<double> element_stiffness(const Element1D& el, const Config& cfg,
                                      const ElementQuadrature& q);
std::vector<double> element_force(const Config& cfg, const ElementQuadrature& q);

DenseMatrix         assemble_stiffness(const Mesh& m, const Config& cfg,
                                       const std::vector<ElementQuadrature>& quads);
std::vector<double> assemble_force(const Mesh& m, const Config& cfg,
                                   const std::vector<ElementQuadrature>& quads);

}