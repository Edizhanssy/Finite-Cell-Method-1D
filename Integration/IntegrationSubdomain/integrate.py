from AdaptiveRefinement.partition import partition
from Integration.IntegrationSubdomain.IntegrateSubDomain import integrateSubDomain


def integrate(integrand, domain):
    sub_domains = partition(domain)
    # Integrate over the first subdomain
    result = integrateSubDomain(sub_domains[0], integrand, domain)
    # Iterate over remaining subdomains
    for i in range(1, len(sub_domains)):
        result += integrateSubDomain(sub_domains[i], integrand, domain)
    return result





