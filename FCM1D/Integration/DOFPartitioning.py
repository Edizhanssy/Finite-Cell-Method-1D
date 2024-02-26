# This code is for assigning the Degree of freedom of the nodes and edges. I used the similar principle as in the
# FCMLAB code, please for more detailed, and more proper implementation refer to the reference [1] in readme.
class DOFPartitioning:

    dof_index = 0
    def __init__(self, nodes, edges, PolynomialDegree, dimensions_of_dof):
        self.nodes = nodes
        self.edges = edges
        self.polynomial_degree = PolynomialDegree # polynomial degree of the problem
        self.dimensions_of_dof = dimensions_of_dof # for each node, there will be one degree of freedom
    def increment_dof_index(self):
        DOFPartitioning.dof_index += 1
        return DOFPartitioning.dof_index

    def distribute_dofs_nodes(self):
        for node in self.nodes:
            dof_node = node.get_dof()
            for dof_id in range(self.dimensions_of_dof):
                if dof_id < len(dof_node):
                    dof_node[dof_id].id = self.increment_dof_index()
    def allocate_dofs_to_edges(self, edge_topology, dof_dimension, polynomial_degree):
        start_index = (polynomial_degree - 2)
        end_index = (polynomial_degree - 1)
        # Precompute the dof_index offset once instead of in each iteration
        dof_index_offset = (dof_dimension - 1) * (self.polynomial_degree - 1)
        for edge in edge_topology:
            dof_edge = edge.get_dof()
            # Iteration is carried out from the start to the end index and assign DOFs to edge
            for i in range(start_index, end_index):
                dof_index = i + dof_index_offset
                if dof_index < len(dof_edge):
                    dof_edge[dof_index].id = self.increment_dof_index()
    def assign_all_dofs(self):
        DOFPartitioning.dof_index = 0
        # the dofs are distributed to the nodes
        self.distribute_dofs_nodes()
        # the dofs are distributed to the edges
        for k in range(2, self.polynomial_degree + 1):
            self.allocate_dofs_to_edges(self.edges, 1, k)
        return DOFPartitioning.dof_index
