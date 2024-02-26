
def LocalToGlobal(localCoords, subdomain):
    FirstCoordinates = subdomain[0]
    SecondCoordinates = subdomain[1]
    GlobalCoords = 0.5*((1-localCoords)*FirstCoordinates+(1+localCoords)*SecondCoordinates)
    return GlobalCoords






