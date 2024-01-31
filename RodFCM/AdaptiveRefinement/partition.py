import numpy as np
from Integration.getIndexGeometry import getIndexGeometry
from Integration.IntegrationSubdomain.getDomainIndexforSeedPoint import getDomainIndexForSeedPoint

def is_intersected(index_geometry, line):
    number_of_seed_points = 11
    seed_points = np.linspace(-1, 1, number_of_seed_points)

    initial_domain_index = getDomainIndexForSeedPoint(seed_points[0], index_geometry, line)
    check = False

    for i in range(1, number_of_seed_points):
        current_domain_index = getDomainIndexForSeedPoint(seed_points[i], index_geometry, line)
        if initial_domain_index != current_domain_index:
            check = True
            break

    return check

def partition_recursively(line_segment, domain_boundaries, support, depth=0, max_depth=20):
    sub_domains = []
    if is_intersected(domain_boundaries, line_segment) and depth < max_depth:
        mid_point = (line_segment[0] + line_segment[1]) / 2
        left_segment = (line_segment[0], mid_point)
        right_segment = (mid_point, line_segment[1])
        sub_domains += partition_recursively(left_segment, domain_boundaries, support, depth + 1, max_depth)
        sub_domains += partition_recursively(right_segment, domain_boundaries, support, depth + 1, max_depth)
    else:
        sub_domains.append(line_segment)
    return sub_domains

def partition(geometry):

    subDomains = []
    depthCounter = 0
    geometrytree = 1

    indexGeometry = getIndexGeometry(geometrytree)

    subDomains = partition_recursively(indexGeometry, geometry, subDomains, depthCounter)

    return subDomains


