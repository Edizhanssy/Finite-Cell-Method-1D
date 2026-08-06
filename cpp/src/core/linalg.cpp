#include "fcm/core/linalg.hpp"

#include <cmath>
#include <stdexcept>
#include <utility>

namespace fcm {

    std::vector<double> solve_dense(DenseMatrix A, std::vector<double> b) {
        const int n = A.n;
        if (static_cast<int>(b.size()) != n)
            throw std::invalid_argument("solve_dense: boyut uyusmazligi");

        for (int k = 0; k < n; ++k) {
            int    piv  = k;
            double best = std::fabs(A(k, k));
            for (int i = k + 1; i < n; ++i) {
                const double v = std::fabs(A(i, k));
                if (v > best) { best = v; piv = i; }
            }
            if (best == 0.0) throw std::runtime_error("solve_dense: tekil matris");
            if (piv != k) {
                for (int j = 0; j < n; ++j) std::swap(A(k, j), A(piv, j));
                std::swap(b[static_cast<std::size_t>(k)], b[static_cast<std::size_t>(piv)]);
            }
            const double akk = A(k, k);
            for (int i = k + 1; i < n; ++i) {
                const double f = A(i, k) / akk;
                if (f == 0.0) continue;
                A(i, k) = 0.0;
                for (int j = k + 1; j < n; ++j) A(i, j) -= f * A(k, j);
                b[static_cast<std::size_t>(i)] -= f * b[static_cast<std::size_t>(k)];
            }
        }
        for (int i = n - 1; i >= 0; --i) {
            double s = b[static_cast<std::size_t>(i)];
            for (int j = i + 1; j < n; ++j) s -= A(i, j) * b[static_cast<std::size_t>(j)];
            b[static_cast<std::size_t>(i)] = s / A(i, i);
        }
        return b;
    }

}  // namespace fcm