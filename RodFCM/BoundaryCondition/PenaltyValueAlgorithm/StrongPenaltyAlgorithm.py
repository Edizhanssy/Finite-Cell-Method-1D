
import numpy as np
from scipy.sparse import lil_matrix

class StrongPenaltyAlgorihtm():

    def __init__(self, PenaltyValue):
        self.PenaltyValue = PenaltyValue

    def modifyLinearSystem(self, globalIdsToConstraint, prescribedValues, K, F):

        K = lil_matrix.tolil(K)

        diagonalIndices = (globalIdsToConstraint-1)*(np.shape(K)[0] + 1)

        if diagonalIndices >= K.shape[0]:
            K_flat = K.flatten()
            K_flat[diagonalIndices] = K_flat[diagonalIndices] + self.PenaltyValue
            K = K_flat.reshape(31, 31)
            rhsPenaltyTerm = np.tile(self.PenaltyValue * prescribedValues, (1, F.shape[1]))

            F[globalIdsToConstraint-1, :] = F[globalIdsToConstraint-1, :] + rhsPenaltyTerm
            return K, F

        # Update the diagonal values of K
        K[diagonalIndices,diagonalIndices] = K[diagonalIndices,diagonalIndices] + self.PenaltyValue

        rhsPenaltyTerm = np.tile(self.PenaltyValue * prescribedValues, (1, F.shape[1]))

        F[globalIdsToConstraint-1,:] = F[globalIdsToConstraint-1,:] + rhsPenaltyTerm

        return K, F









