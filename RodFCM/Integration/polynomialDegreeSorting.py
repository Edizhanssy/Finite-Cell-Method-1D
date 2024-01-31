
class PolynomialDegreeSorting:
    internal_counter = 0

    def __init__(self, nodes, edges, polynomial_degree, dof_dimension):
        self.nodes = nodes
        self.edges = edges
        self.polynomial_degree = polynomial_degree
        self.dof_dimension = dof_dimension

    def assign_dofs_to_nodes(self):
        nodal_dof_counter = PolynomialDegreeSorting.internal_counter
        for node in self.nodes:
            dof_handle = node.get_dof()
            for current_dof_dimension in range(self.dof_dimension):
                if current_dof_dimension < len(dof_handle):
                    dof_handle[current_dof_dimension].id = nodal_dof_counter + 1
                    nodal_dof_counter += 1
        return nodal_dof_counter

    def assign_dofs_to_topology(self, topology, current_dof_dimension, current_polynomial_degree, total_dof_counter,
                                polynomial_degree, topology_space_dimension):
        dof_counter = total_dof_counter
        for item in topology:
            dof_handle = item.get_dof()

            # Calculate the start and end indices for the range
            start_index = (current_polynomial_degree - 2) ** topology_space_dimension
            end_index = (current_polynomial_degree - 1) ** topology_space_dimension

            for i in range(start_index, end_index):
                dof_index = i + (current_dof_dimension - 1) * ((polynomial_degree - 1) ** topology_space_dimension)
                if dof_index < len(dof_handle):
                    dof_handle[dof_index].id = dof_counter + 1
                    dof_counter += 1

        return dof_counter

    def assign_dofs(self):
        PolynomialDegreeSorting.internal_counter = 0
        PolynomialDegreeSorting.internal_counter = self.assign_dofs_to_nodes()

        # Assign DOFs to edges - only once per edge
        for current_polynomial_degree in range(2, self.polynomial_degree + 1):
            PolynomialDegreeSorting.internal_counter = self.assign_dofs_to_topology(self.edges, 1,
                                                                                    current_polynomial_degree,
                                                                                    PolynomialDegreeSorting.internal_counter,
                                                                                    self.polynomial_degree, 1)

        return PolynomialDegreeSorting.internal_counter
