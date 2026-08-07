//
// Created by Edizhan Yildiz on 06.08.26.
//

#ifndef FINITE_CELL_METHOD_LEGENDRE_H
#define FINITE_CELL_METHOD_LEGENDRE_H
#pragma once
#include <vector>

namespace fcm {

    struct LegendreValues {
        std::vector<double> P;
        std::vector<double> dP;
    };

    LegendreValues legendre_and_derivs(int n_max, double xi);

    std::vector<double> shape_functions(int p, double xi);
    std::vector<double> shape_function_derivs(int p, double xi);

}

#endif //FINITE_CELL_METHOD_LEGENDRE_H