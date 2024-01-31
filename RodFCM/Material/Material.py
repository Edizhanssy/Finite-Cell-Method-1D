
def Material(E, nu, dimension, is_fictitious, alpha):
    import numpy as np

    # Apply the penalization factor for the fictitious domain
    E_effective = alpha * E if is_fictitious else E

    if dimension == 1:
        # For 1D, return the scalar Young's modulus
        return E_effective
    elif dimension == 2:
        # For 2D, return the 2x2 material matrix for plane stress or plane strain
        material_matrix = E_effective * (np.eye(2) * (1 - nu) + np.ones((2, 2)) * nu) / (1 - nu ** 2)
        return material_matrix
    else:
        raise ValueError("Dimension must be 1 or 2.")



