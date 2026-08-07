//
// Created by Edizhan Yildiz on 06.08.26.
//

#ifndef FINITE_CELL_METHOD_GAUSS_H
#define FINITE_CELL_METHOD_GAUSS_H

#pragma once
#include <vector>

namespace fcm {

    struct GaussRule {
        std::vector<double> points;
        std::vector<double> weights;
    };

    GaussRule gauss_legendre(int n);

}


#endif //FINITE_CELL_METHOD_GAUSS_H