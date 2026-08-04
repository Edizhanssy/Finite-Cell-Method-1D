from Element.StiffnessMatrix.calcStiffnessMatrix import calculate_stiffness_matrix

def calculate_element_stiffness(element, cfg):
    return calculate_stiffness_matrix(element, cfg)


