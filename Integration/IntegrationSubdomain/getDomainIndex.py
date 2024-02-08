def getDomainIndex(coord):
    # Initialize domain boundaries
    physical_domain1 = [0, 1, 0]
    physical_domain2 = [7/3, 3, 0]
    fictious_domain = [1, 7/3, 0]

    # Check if the point is in the physical domain 1
    if physical_domain1[0] <= coord <= physical_domain1[1]:
        value = 0  # Physical domain 1
    # Check if the point is in the fictitious domain
    elif fictious_domain[0] <= coord <= fictious_domain[1]:
        value = 1  # Fictitious domain
    # Check if the point is in the physical domain 2
    elif physical_domain2[0] <= coord <= physical_domain2[1]:
        value = 0  # Physical domain 2
    else:
        value = -1

    return value