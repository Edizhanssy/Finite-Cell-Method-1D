class DOFPartitioning:
    dof_sequence_index = 0

    def __init__(self, vertex_nodes, boundary_edges, degree_of_polynomial, dimensions_of_dof):
        self.vertex_nodes = vertex_nodes
        self.boundary_edges = boundary_edges
        self.degree_of_polynomial = degree_of_polynomial
        self.dimensions_of_dof = dimensions_of_dof

    def distribute_dofs_among_nodes(self):
        node_dof_index = DOFPartitioning.dof_sequence_index
        for node in self.vertex_nodes:
            dof_registry = node.get_dof()
            for dof_id in range(self.dimensions_of_dof):
                if dof_id < len(dof_registry):
                    dof_registry[dof_id].id = node_dof_index + 1
                    node_dof_index += 1
        DOFPartitioning.dof_sequence_index = node_dof_index

    def allocate_dofs_to_edges(self, edge_topology, dof_dimension, poly_degree_current, dof_start_count, degree_of_polynomial, dimensionality):
        edge_dof_counter = dof_start_count
        for edge in edge_topology:
            dof_registry = edge.get_dof()
            start_index = (poly_degree_current - 2) ** dimensionality
            end_index = (poly_degree_current - 1) ** dimensionality
            for i in range(start_index, end_index):
                dof_index = i + (dof_dimension - 1) * ((degree_of_polynomial - 1) ** dimensionality)
                if dof_index < len(dof_registry):
                    dof_registry[dof_index].id = edge_dof_counter + 1
                    edge_dof_counter += 1
        DOFPartitioning.dof_sequence_index = edge_dof_counter

    def assign_all_dofs(self):
        DOFPartitioning.dof_sequence_index = 0
        self.distribute_dofs_among_nodes()
        for current_polynomial_degree in range(2, self.degree_of_polynomial + 1):
            self.allocate_dofs_to_edges(self.boundary_edges, 1, current_polynomial_degree, DOFPartitioning.dof_sequence_index, self.degree_of_polynomial, 1)
        return DOFPartitioning.dof_sequence_index

