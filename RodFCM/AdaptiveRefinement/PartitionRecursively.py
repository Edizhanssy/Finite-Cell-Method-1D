import numpy as np

def is_intersected(seed_points, domain_boundaries, line_segment):

    initial_domain_index = get_domain_index(seed_points[0], domain_boundaries)
    for point in seed_points:
        current_domain_index = get_domain_index(point, domain_boundaries)
        if initial_domain_index != current_domain_index:
            return True
    return False

def get_domain_index(point, domain_boundaries):

    for index, (start, end) in enumerate(domain_boundaries):
        if start <= point <= end:
            return 0 if index in [0, 2] else 1  # Returns 0 for physical, 1 for fictitious
    return -1  # Point is outside the domain boundaries

def partition_recursively(line_segment, domain_boundaries, depth=0, max_depth=20):
    sub_domains = []
    if is_intersected(np.linspace(line_segment[0], line_segment[1], 11), domain_boundaries, line_segment) and depth < max_depth:
        mid_point = (line_segment[0] + line_segment[1]) / 2
        left_segment = (line_segment[0], mid_point)
        right_segment = (mid_point, line_segment[1])
        sub_domains += partition_recursively(left_segment, domain_boundaries, depth + 1, max_depth)
        sub_domains += partition_recursively(right_segment, domain_boundaries, depth + 1, max_depth)
    else:
        sub_domains.append(line_segment)
    return sub_domains

def partition_element(element, local_domain_boundaries, E, ScalingFactor):
    start_local, end_local = element.local_coordinates

    # Define nodes
    nodes = [start_local, end_local]

    # Define element boundaries
    element_boundaries = [
        (max(start_local, start), min(end_local, end))
        for start, end in local_domain_boundaries
        if not (end < start_local or start > end_local)
    ]

    # Partition recursively and get subdomains (edges)
    edges = partition_recursively((start_local, end_local), element_boundaries)

    element.add_subdomain(element.local_coordinates, 1, ScalingFactor, 0)

    # Add properties to each subdomain (edge)
    for edge_coords in edges:
        midpoint = (edge_coords[0] + edge_coords[1]) / 2
        domain_index = get_domain_index(midpoint, local_domain_boundaries)
        element.add_subdomain(edge_coords, E, ScalingFactor, domain_index)

    # Return nodes and edges for DOF assignment
    return element



