import numpy as np
from Element.StiffnessMatrix.ElementalStiffness import calculate_element_stiffness

def assemble_global_stiffness_matrix(elements, PolynomialDegree, DOF, LtoG):

    total_dofs = DOF
    K_global = np.zeros((total_dofs, total_dofs))  # Initialize global stiffness matrix

    for i, element in enumerate(elements):
        Ke = calculate_element_stiffness(element, PolynomialDegree)
        LM = LtoG
        K_global = scatterElementMatrixIntoGlobalMatrix(Ke, LM[i], K_global)

    return K_global

def scatterElementMatrixIntoGlobalMatrix(element_matrix, location_matrix, global_matrix):

    loc = np.array(location_matrix).flatten()  # Ensure each sublist is a 1D array
    global_matrix[np.ix_(loc, loc)] += element_matrix
    return global_matrix






