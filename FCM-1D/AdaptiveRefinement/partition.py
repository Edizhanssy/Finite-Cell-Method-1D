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
def RecursivePartitioning(line_segment, domain_boundaries, support, depth=0, max_depth=10):
    sub_domains = []
    # if intersection exist, element and subdomains are further divided from their middle and identified them as
    # new subdomains. The procedure is carried out until there will be no called 'cut-cells' avaliable in the domain.
    # if the max depth is reached the partitioning will be stopped !
    if checkIntersection(domain_boundaries, line_segment) and depth < max_depth:
        mid_point = (line_segment[0] + line_segment[1]) / 2
        left_segment = (line_segment[0], mid_point)
        right_segment = (mid_point, line_segment[1])
        sub_domains += RecursivePartitioning(left_segment, domain_boundaries, support, depth + 1, max_depth)
        sub_domains += RecursivePartitioning(right_segment, domain_boundaries, support, depth + 1, max_depth)
    else:
        sub_domains.append(line_segment)
    return sub_domains

def partition(geometry):
    subDomains = []
    # the depth is initially start from 0
    depthCounter = 0
    # the domain index of the element is obtained in our case the element has [-1, 1]
    indexGeometry = [-1, 1]
    # the recursive partitioning of the corresponding element is carried out and subdomains are obtained !
    subDomains = RecursivePartitioning(indexGeometry, geometry, subDomains, depthCounter)
    return subDomains


