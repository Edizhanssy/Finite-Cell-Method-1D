from Element.StiffnessMatrix.calcStiffnessMatrix import calculate_stiffness_matrix
import numpy as np

def calculate_element_stiffness(element, PolynomialDegree):
    return calculate_stiffness_matrix(element, PolynomialDegree)


