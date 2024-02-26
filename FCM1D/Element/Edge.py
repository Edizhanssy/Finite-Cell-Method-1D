from Element.Dof import Dof
# the Edge object !
class Edge:
    def __init__(self, nodes, polynomial_degree, dof_dimension):
        self.nodes = nodes
        self.polynomial_degree = polynomial_degree
        self.dof_dimension = dof_dimension
        self.dofs = [Dof() for _ in range(dof_dimension * (polynomial_degree - 2))]

    def get_dof(self):
        return self.dofs



