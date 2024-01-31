
def ApplyBoundaryConditions(mesh, StiffnessMatrix, ForceVector, BoundaryConditions):

    lengthBC = len(BoundaryConditions)

    for MeshId in range(len(mesh)-1):
        for i in range(lengthBC):
            StiffnessMatrix, ForceVector = BoundaryConditions[i].modifyLinearSystem(mesh[i], StiffnessMatrix, ForceVector)

    return StiffnessMatrix, ForceVector

