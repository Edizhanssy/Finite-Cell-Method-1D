class Subdomain:
    def __init__(self, local_coordinates, E, scalingfactor, domain_index):
        self.local_coordinates = local_coordinates
        self.E = E
        self.scalingfactor = scalingfactor
        self.domain_index = domain_index
        self.global_coordinates = []

class Element:
    def __init__(self, id, global_coordinates, localCoord):
        self.id = id
        self.local_coordinates = global_coordinates
        self.subdomains = []
        self.global_coordinates = localCoord

    def add_subdomain(self, node_coordinates, E, scalingfactor, domain_index):
        subdomain = Subdomain(node_coordinates, E, scalingfactor, domain_index)
        self.subdomains.append(subdomain)



