import numpy as np
from Element.StiffnessMatrix.ElementalStiffness import calculate_element_stiffness

# the global stiffness matrix is constructed in this code !
def assemble_global_stiffness_matrix(elements, PolynomialDegree, DOF, LtoG):
    total_dofs = DOF
    K_global = np.zeros((total_dofs, total_dofs))  # Initialize global stiffness matrix
    # for each element, the elemental stiffness matrices are obtained !
    for i, element in enumerate(elements):
        Ke = calculate_element_stiffness(element, PolynomialDegree)
        # the location matrix of the domain
        LM = LtoG
        # the element matrix is mapped to the global stiffness matrix !
        K_global = ElementMatrixIntoGlobalMatrix(Ke, LM[i], K_global)
    return K_global

def ElementMatrixIntoGlobalMatrix(element_matrix, location_matrix, global_matrix):
    loc = np.array(location_matrix).flatten()  # the 2-d array of the location matrix is flattened to 1-d array !
    global_matrix[np.ix_(loc, loc)] += element_matrix
    return global_matrix






