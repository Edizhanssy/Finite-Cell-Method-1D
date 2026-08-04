from Integration.IntegrationSubdomain.LocalToGlobal import LocalToGlobal


def DomainIndexForSeedPoint(seedPoint, support, indexGeometry, cfg):
    localCoord = LocalToGlobal(seedPoint, indexGeometry)
    globalCoord = LocalToGlobal(localCoord, support.global_coordinates)
    return cfg.domain_index(globalCoord)


