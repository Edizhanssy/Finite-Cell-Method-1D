#pragma once
#include <vector>

#include "fcm/fcm1d/assembly.hpp"

namespace fcm {

std::vector<double> solve_dense(DenseMatrix A, std::vector<double> b);

}  // namespace fcm