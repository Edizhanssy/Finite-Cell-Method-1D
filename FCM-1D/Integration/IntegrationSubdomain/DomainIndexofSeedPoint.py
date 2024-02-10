from Integration.IntegrationSubdomain.LocalToGlobal import LocalToGlobal

# for finding the intersections, the seedpoints are append to the domain and the index of teh seed point is found according
# to the data provided by problem model !

def DomainIndexForSeedPoint(seedPoint,support,indexGeometry):
    localCoord = LocalToGlobal(seedPoint, indexGeometry)
    globalCoord = LocalToGlobal(localCoord, support.global_coordinates)
    domainIndex = getDomainIndex(globalCoord)
    return domainIndex

def getDomainIndex(coord):
    # domain boundaries !
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
        # if the point is neither in fictitious nor physical domain !
        value = -1

    return value


