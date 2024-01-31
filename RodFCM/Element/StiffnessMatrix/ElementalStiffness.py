
from Element.StiffnessMatrix.calcStiffnessMatrix import calcStiffnessMatrix
import numpy as np

def calculate_element_stiffness(element, PolynomialDegree):

    Ke = np.zeros((PolynomialDegree, PolynomialDegree))  # Initialize element stiffness matrix

    Ke_sub = calcStiffnessMatrix(element, PolynomialDegree)
    Ke += Ke_sub

    return Ke


