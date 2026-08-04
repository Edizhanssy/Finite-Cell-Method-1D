from Integration.IntegrationSubdomain.LocalToGlobal import LocalToGlobal
from Integration.IntegrationSubdomain.calcDeterminantJacobian import calcDeterminantJacobian
from Integration.IntegrationSubdomain.calcDetJacobiandomain import calcDetJacobianDomain
from Integration.GaussQuadrature.GaussWeights import GaussQuadratureWeights
from Integration.GaussQuadrature.GaussCoordinates import GaussQuadratureCoordinates

def SubDomainIntegration(subdomain, integrand, element, cfg):
    localPoints = GaussQuadratureCoordinates(cfg.n_gauss)
    localWeights = GaussQuadratureWeights(cfg.n_gauss)
    intresult = None
    for i in range(len(localPoints)):
        point, weight = getIntegrationPoint(localPoints[i], localWeights[i], subdomain, element)
        contribution = integrand(point) * weight
        intresult = contribution if intresult is None else intresult + contribution
    return intresult

def getIntegrationPoint(localPoint, localWeights, subDomain, element):
    # in this function the integration points will be obtained via mapping the gauss points to the each sub-domain
    # the global coordinates of the element
    a = element.global_coordinates
    # the integration point of the corresponding gauss point
    point = LocalToGlobal(localPoint, subDomain)
    # the integration weight of the corresponding integration point
    weight = localWeights * calcDeterminantJacobian(localPoint, subDomain) * calcDetJacobianDomain(a, point)
    return point, weight