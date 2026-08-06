#pragma once
#include <array>
#include <vector>

#include "fcm/fcm1d/config.hpp"

namespace fcm {

struct Element1D {
    int id;
    std::array<double, 2> local;    // eleman-yerel aralik (asagida kullanilmiyor, sadakat icin)
    std::array<double, 2> global_;  // global koordinatlar
};

struct Mesh {
    std::vector<double>            node_local;  // dugumlerin yerel koordinatlari
    std::vector<int>               node_dof;    // 1-tabanli DOF id
    std::vector<std::vector<int>>  edge_dof;    // kenar basina ic mod DOF id'leri (1-tabanli)
    std::vector<Element1D>         elements;
    std::vector<std::vector<int>>  ltog;        // eleman basina n_modes adet 0-tabanli DOF
    int n_dof = 0;
};

Mesh build_mesh(const Config& cfg);

}  // namespace fcm