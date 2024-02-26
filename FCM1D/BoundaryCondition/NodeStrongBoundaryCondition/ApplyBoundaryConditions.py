
def ApplyBoundaryConditions(mesh, StiffnessMatrix, ForceVector, BoundaryConditions):
    # the number of boundary conditions are taken for appending them both stiffness matrix and force vector !
    lengthBC = len(BoundaryConditions)
    for MeshId in range(len(mesh)-1):
        for i in range(lengthBC):
            StiffnessMatrix, ForceVector = BoundaryConditions[i].appendBcs(mesh[i], StiffnessMatrix, ForceVector)
    return StiffnessMatrix, ForceVector

