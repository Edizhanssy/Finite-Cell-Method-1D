import numpy as np
from Integration.IntegrationSubdomain.DomainIndexofSeedPoint import DomainIndexForSeedPoint

# the point inclusion test is carried out in this function
def checkIntersection(index_geometry, line):
    # input: the domain index [-1, 1], the corresponding element
    # 11 number of seedpoints will be attained to the element and if there is an transition between the previous domain
    # and current domain, the algorithm will be the check = True, otherwise, check = False
    number_of_seed_points = 11
    seed_points = np.linspace(-1, 1, number_of_seed_points)

    initial_domain_index = DomainIndexForSeedPoint(seed_points[0], index_geometry, line)
    check = False

    for i in range(number_of_seed_points):
        current_domain_index = DomainIndexForSeedPoint(seed_points[i], index_geometry, line)
        if initial_domain_index != current_domain_index:
            check = True
            break

    return check

# Recursively partition the element
def RecursivePartitioning(line_segment, domain_boundaries, depth=0, max_depth=10):
    if checkIntersection(domain_boundaries, line_segment) and depth < max_depth:
        mid_point = (line_segment[0] + line_segment[1]) / 2
        left_segment = (line_segment[0], mid_point)
        right_segment = (mid_point, line_segment[1])
        return (RecursivePartitioning(left_segment, domain_boundaries, depth + 1, max_depth)
                + RecursivePartitioning(right_segment, domain_boundaries, depth + 1, max_depth))
    return [line_segment]


def partition(geometry):
    return RecursivePartitioning([-1, 1], geometry, 0)


