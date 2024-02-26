from Element.Dof import Dof
# the Node object !
class Node:
    def __init__(self, coords, dof_dimension):
        self.coords = coords
        self.dof_dimension = dof_dimension
        self.dofs = [Dof() for _ in range(dof_dimension)]

    def get_dof(self):
        return self.dofs


