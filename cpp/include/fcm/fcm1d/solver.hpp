#pragma once
#include <vector>

#include "fcm/fcm1d/assembly.hpp"
#include "fcm/fcm1d/config.hpp"
#include "fcm/fcm1d/mesh.hpp"
#include "fcm/fcm1d/quadrature.hpp"

namespace fcm {

struct Timings {
    double mesh = 0.0, quadrature = 0.0, assembly = 0.0, bc_solve = 0.0, total = 0.0;
};

struct SolveResult {
    Mesh                           mesh;
    std::vector<ElementQuadrature> quads;
    DenseMatrix                    K;
    std::vector<double>            F;
    std::vector<double>            u;
    double                         nodal_force_sum = 0.0;
    Timings                        t;
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

}