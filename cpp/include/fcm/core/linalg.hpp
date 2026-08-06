#pragma once
#include <vector>

#include "fcm/fcm1d/assembly.hpp"

namespace fcm {

/// Kismi pivotlu LU ile A x = b. A ve b deger olarak alinir (kopyalanir).
std::vector<double> solve_dense(DenseMatrix A, std::vector<double> b);

}  // namespace fcm