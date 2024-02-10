from AdaptiveRefinement.partition import partition
from Integration.IntegrationSubdomain.SubDomainIntegration import SubDomainIntegration

# the integration of the subdomain is carried out in this function !
def integrate(integrand, domain):
    # the subdomains are obtained with using partition function
    sub_domains = partition(domain)
    # Integrate over the first subdomain
    result = SubDomainIntegration(sub_domains[0], integrand, domain)
    # Iterate over remaining subdomains
    for i in range(1, len(sub_domains)):
        result += SubDomainIntegration(sub_domains[i], integrand, domain)
    return result





