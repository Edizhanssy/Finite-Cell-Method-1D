#include "fcm/fcm1d/partition.hpp"

namespace fcm {
    namespace {

        constexpr int kSeedPoints = 11;

        bool has_intersection(const std::array<double, 2>& seg,
                              const Element1D& el, const Config& cfg) {
            int first = 0;
            for (int i = 0; i < kSeedPoints; ++i) {
                const double xi     = -1.0 + 2.0 * i / (kSeedPoints - 1);
                const double local  = local_to_global(xi, seg);
                const double global = local_to_global(local, el.global_);
                const int    idx    = cfg.domain_index(global);
                if (i == 0) first = idx;
                else if (idx != first) return true;
            }
            return false;
        }

        void recurse(const std::array<double, 2>& seg, const Element1D& el, const Config& cfg,
                     int depth, std::vector<std::array<double, 2>>& out) {
            if (depth < cfg.max_depth && has_intersection(seg, el, cfg)) {
                const double mid = 0.5 * (seg[0] + seg[1]);
                recurse({seg[0], mid}, el, cfg, depth + 1, out);
                recurse({mid, seg[1]}, el, cfg, depth + 1, out);
            } else {
                out.push_back(seg);
            }
        }

    }

    std::vector<std::array<double, 2>> partition_element(const Element1D& el, const Config& cfg) {
        std::vector<std::array<double, 2>> out;
        recurse({-1.0, 1.0}, el, cfg, 0, out);
        return out;
    }

}