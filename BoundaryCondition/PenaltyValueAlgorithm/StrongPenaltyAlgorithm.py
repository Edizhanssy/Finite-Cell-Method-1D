import numpy as np

# The penalty value approach is used to append the strong penalty algorithms
# The strong penalty algorithm is used to apply the boundary conditions to the both Stiffness Matrix and Force Vector
# I have tried to use the structure avaliable in the FCMLAB for the strong form. If you need more validated, and the application on
# both 2-D and 3-D cases, please refer to Readme.md file.
class StrongPenaltyAlgorithm:
    def __init__(self, PenaltyValue):
        self.PenaltyValue = PenaltyValue
    def StrongPenalty(self, globalIdsToConstraint, Values, K, F):
        original_shape = K.shape  # the original shape of the stiffness matrix is gained
        diagonalIndices = (globalIdsToConstraint - 1) * (np.shape(K)[0] + 1)
        K_flat = K.flatten()
        K_flat[diagonalIndices] += self.PenaltyValue
        # the original shape is used
        K = K_flat.reshape(original_shape)
        rhsPenaltyTerm = np.tile(self.PenaltyValue * Values, (1, F.shape[1]))
        rhsPenaltyTerm = rhsPenaltyTerm.flatten()
        F[globalIdsToConstraint - 1, :] += rhsPenaltyTerm
        return K, F










