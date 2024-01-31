
class StrongNodeDirichletBoundaryCondition():

    def __init__(self, position, PrescribedValue, Direction, StrongDirichletAlgorithm):
        self.position = position
        self.PrescribedValue = PrescribedValue
        self.Direction = Direction
        self.StrongDirichletAlgorithm = StrongDirichletAlgorithm

    def modifyLinearSystem(self, Node, K, F):

        DofHandle = Node.get_dof()

        for i in range(len(DofHandle)):
            id = DofHandle[i].id

            Value = self.PrescribedValue

            K, F = self.StrongDirichletAlgorithm.modifyLinearSystem(id, Value, K, F)

        return K, F























