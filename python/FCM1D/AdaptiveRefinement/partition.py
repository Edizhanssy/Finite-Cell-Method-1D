import numpy as np
from Integration.IntegrationSubdomain.DomainIndexofSeedPoint import DomainIndexForSeedPoint


def checkIntersection(index_geometry, line, cfg):
    number_of_seed_points = 11
    seed_points = np.linspace(-1, 1, number_of_seed_points)
    initial = DomainIndexForSeedPoint(seed_points[0], index_geometry, line, cfg)
    for i in range(number_of_seed_points):
        if DomainIndexForSeedPoint(seed_points[i], index_geometry, line, cfg) != initial:
            return True
    return False


def RecursivePartitioning(line_segment, domain_boundaries, cfg, depth=0):
    if checkIntersection(domain_boundaries, line_segment, cfg) and depth < cfg.max_depth:
        mid_point = (line_segment[0] + line_segment[1]) / 2
        return (RecursivePartitioning((line_segment[0], mid_point), domain_boundaries, cfg, depth + 1)
                + RecursivePartitioning((mid_point, line_segment[1]), domain_boundaries, cfg, depth + 1))
    return [line_segment]


def partition(geometry, cfg):
    return RecursivePartitioning([-1, 1], geometry, cfg, 0)


