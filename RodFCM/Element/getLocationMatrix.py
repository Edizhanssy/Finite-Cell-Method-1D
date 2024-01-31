import numpy as np

def setup_location_matrix_topology(topology, space_dimension, N, d, polynomial_degree, location_matrix):
    number_of_topology_dofs = (polynomial_degree - 2) ** space_dimension
    for i in range(len(topology)):
        dof_handle = topology[i].get_dof()
        # Process each DOF for the topology item and update the location matrix
        for j in range(number_of_topology_dofs):
            if j < len(dof_handle):
                index = N + j + (i) * number_of_topology_dofs + (d-1) * polynomial_degree
                location_matrix[index] = dof_handle[j+(d-1)*number_of_topology_dofs].id-1
    return N

def setup_location_matrices(nodes, edges, polynomial_degree, dof_dimension):
    location_matrices = []
    N = 0
    for d in range(1, dof_dimension+1):
        location_matrix = np.zeros([polynomial_degree], dtype=int)

        setup_location_matrix_topology(nodes, 0, N, d, polynomial_degree, location_matrix)
        N += len(nodes)
        setup_location_matrix_topology([edges], 1, N, d, polynomial_degree, location_matrix)
        N = N + len([edges])*(polynomial_degree-2)

        location_matrices.append(location_matrix.tolist())

    return location_matrices

def setupPerElement(nodes, edges, polynomial_degree, dof_dimension, numberOfXDivision):

    GlobalLocationMatrix = []

    for i in range(numberOfXDivision):
        NodePair = [nodes[i], nodes[i+1]]
        OneEdge = edges[i]

        loca = setup_location_matrices(NodePair, OneEdge, polynomial_degree, dof_dimension)
        GlobalLocationMatrix.append(loca)

    return GlobalLocationMatrix














