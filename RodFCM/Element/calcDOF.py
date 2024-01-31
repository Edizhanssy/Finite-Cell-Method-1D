
def calcDOF(elements, PolynomialDegree):
    num_internal_nodes = (len(elements)) * (PolynomialDegree)
    num_boundary_nodes = 1  # Start and end nodes
    num_global_dofs = num_internal_nodes + num_boundary_nodes

    return num_global_dofs



