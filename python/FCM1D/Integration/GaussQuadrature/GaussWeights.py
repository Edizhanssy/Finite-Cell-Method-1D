from Integration.GaussQuadrature.GaussCoordinates import _rule


def GaussQuadratureWeights(GO):
    return _rule(GO)[1]