from Element.StiffnessMatrix.calcStiffnessMatrix import calculate_stiffness_matrix
import numpy as np

def calculate_element_stiffness(element, PolynomialDegree):
    Ke = np.zeros((PolynomialDegree, PolynomialDegree))  # Initialize element stiffness matrix
    # the stiffness matrix of the overall element
    Ke_sub = calculate_stiffness_matrix(element, PolynomialDegree)
    Ke += Ke_sub
    return Ke


