
# in this class the boundary conditions properties, its position, the value of the boundary condition, the fixed displacement,
# the displacement on the specific node,
# direction of the boundary condition and the strong form boundary condition algorithm (For our case Penalty Value Algorithm) are illustrated.
class StrongNodeDirichletBoundaryCondition:
    def __init__(self, position, Value, Direction, StrongDirichletAlgorithm):
        self.position = position
        self.Value = Value
        self.Direction = Direction
        self.StrongDirichletAlgorithm = StrongDirichletAlgorithm

    def appendBcs(self, Node, K, F):
        # the dof of the corresponding node
        DofHandle = Node.get_dof()
        for i in range(len(DofHandle)):
            # id of the corresponding node for attending the boundary condition !
            id = DofHandle[i].id
            # the value of the boundary condition !
            Value = self.Value
            K, F = self.StrongDirichletAlgorithm.StrongPenalty(id, Value, K, F)
        return K, F























