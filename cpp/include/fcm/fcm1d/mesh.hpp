#pragma once
#include <array>
#include <vector>

#include "fcm/fcm1d/config.hpp"

namespace fcm {

struct Element1D {
    int id;
    std::array<double, 2> local;    // elemental coordinates
    std::array<double, 2> global_;  // global coordinates
};

struct Mesh {
    std::vector<double>            node_local;
    std::vector<int>               node_dof;
    std::vector<std::vector<int>>  edge_dof;
    std::vector<Element1D>         elements;
    std::vector<std::vector<int>>  ltog;
    int n_dof = 0;
};

Mesh build_mesh(const Config& cfg);

}