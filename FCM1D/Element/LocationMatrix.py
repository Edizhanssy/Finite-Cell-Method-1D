import numpy as np

def update_location_matrix(topology_items, space_dim, global_index_start, dof_dim, poly_degree, loc_matrix):
    # Calculate the number of DOFs for each topology item based on space dimension and polynomial degree
    topo_dofs = (poly_degree - 2) ** space_dim
    for i, item in enumerate(topology_items):
        dof_handle = item.get_dof()
        for j in range(topo_dofs):
            if j < len(dof_handle):
                index = global_index_start + j + i * topo_dofs + (dof_dim - 1) * poly_degree
                loc_matrix[index] = dof_handle[j + (dof_dim - 1) * topo_dofs].id - 1

    return global_index_start

def setup_location_matrices(nodes, edges, polynomial_degree, dof_dimension):
    location_matrices = []
    N = 0
    for d in range(1, dof_dimension+1):
        location_matrix = np.zeros([polynomial_degree], dtype=int)
        update_location_matrix(nodes, 0, N, d, polynomial_degree, location_matrix)
        N += len(nodes)
        update_location_matrix([edges], 1, N, d, polynomial_degree, location_matrix)
        N = N + len([edges])*(polynomial_degree-2)
        location_matrices.append(location_matrix.tolist())
    return location_matrices

# The location matrix for each element is obtained from this function.
# I have used the similar structure in the FCMLAB code since my previous approach were not giving the desired results
# for constructing the shape function. please for more information refer to readme file
# My first approach: since it is an 1-d problem, I tried to make the simple approach for linearly connecting the nodes as location matrix
# since we are using p-version FEM; however, this apporach does not give the desired result. Please for more detailed implementation refer to
# reference [1] in readme file !
def setupPerElement(nodes, edges, polynomial_degree, dof_dimension, numberOfXDivision):
    GlobalLocationMatrix = []
    for i in range(numberOfXDivision):
        NodePair = [nodes[i], nodes[i+1]]
        OneEdge = edges[i]
        loca = setup_location_matrices(NodePair, OneEdge, polynomial_degree, dof_dimension)
        GlobalLocationMatrix.append(loca)
    return GlobalLocationMatrix














