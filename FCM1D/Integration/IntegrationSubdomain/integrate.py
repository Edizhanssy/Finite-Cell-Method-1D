from AdaptiveRefinement.partition import partition
from Integration.IntegrationSubdomain.SubDomainIntegration import SubDomainIntegration


def integrate(integrand, domain, cfg):
    result = None
    for sub in partition(domain, cfg):
        contribution = SubDomainIntegration(sub, integrand, domain, cfg)
        result = contribution if result is None else result + contribution
    return result





