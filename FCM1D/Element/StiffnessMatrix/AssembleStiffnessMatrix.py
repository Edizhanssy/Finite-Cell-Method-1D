import numpy as np
from Element.StiffnessMatrix.ElementalStiffness import calculate_element_stiffness

# the global stiffness matrix is constructed in this code !
def assemble_global_stiffness_matrix(elements, DOF, LtoG, cfg):
    K_global = np.zeros((DOF, DOF))
    for i, element in enumerate(elements):
        Ke = calculate_element_stiffness(element, cfg)
        K_global = ElementMatrixIntoGlobalMatrix(Ke, LtoG[i], K_global)
    return K_global

def ElementMatrixIntoGlobalMatrix(element_matrix, location_matrix, global_matrix):
    loc = np.array(location_matrix).flatten()  # the 2-d array of the location matrix is flattened to 1-d array !
    global_matrix[np.ix_(loc, loc)] += element_matrix
    return global_matrix






