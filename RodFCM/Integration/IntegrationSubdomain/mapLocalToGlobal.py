
def mapLocalToGlobal(localCoord, subdomain):

    FirstVertexCoordinates = subdomain[0]
    SecondVertexCoordinates = subdomain[1]

    GlobalCoords = 0.5*((1-localCoord)*FirstVertexCoordinates+(1+localCoord)*SecondVertexCoordinates)

    return GlobalCoords






