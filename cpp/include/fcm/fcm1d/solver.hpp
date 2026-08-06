#pragma once
#include <vector>

#include "fcm/fcm1d/assembly.hpp"
#include "fcm/fcm1d/config.hpp"
#include "fcm/fcm1d/mesh.hpp"
#include "fcm/fcm1d/quadrature.hpp"

namespace fcm {

struct SolveResult {
    Mesh                           mesh;
    std::vector<ElementQuadrature> quads;
    DenseMatrix                    K;   // sinir kosullari uygulanmis
    std::vector<double>            F;   // sinir kosullari uygulanmis
    std::vector<double>            u;
    double                         nodal_force_sum = 0.0;
};

SolveResult solve(const Config& cfg);

double displacement_at(const Config& cfg, const Mesh& m,
                       const std::vector<double>& u, double x);

struct StrainField {
    std::vector<double> pos;
    std::vector<double> eps;
};

StrainField strain_field(const Config& cfg, const Mesh& m,
                         const std::vector<double>& u, int samples = 400);

}  // namespace fcm