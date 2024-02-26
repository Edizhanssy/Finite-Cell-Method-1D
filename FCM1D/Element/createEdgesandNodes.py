from Element.Node import Node
from Element.Edge import Edge
from Element.Element import Element

# based upon the given division aspects, the overall domain is discretized initially as elements. In our case,
# our domain is initially has two elements.
def create_nodes_on_line(start_point, end_point, num_divisions):
    x_increment = (end_point - start_point) / num_divisions
    nodes = []
    for i in range(num_divisions+1):
        coordinate = start_point + i * x_increment
        nodes.append(Node((coordinate,), 1))  # Assuming DOF dimension is 1
    return nodes
def create_edges_on_line(nodes):
    edges = []
    for i in range(len(nodes)-1):
        NodePair = [nodes[i], nodes[i+1]]
        edge = Edge(NodePair, 16, 1) # 16 is our polynomial degree, 1 is our dof of an edge
        edges.append(edge)
    return edges

def create_nodes_and_edges(elements, x_divisions):
    all_nodes = []
    all_edges = []
    new_elements = []
    for element in elements:
        # Create nodes and edges for the element
        nodes = create_nodes_on_line(element.local_coordinates[0], element.local_coordinates[1], x_divisions)
        edges = create_edges_on_line(nodes)
        # Add nodes and edges to the global list
        all_nodes.append(nodes)
        all_edges.append(edges)
        # Calculate the increment for each sub-element's global coordinate
        global_increment = (element.global_coordinates[1] - element.global_coordinates[0]) / x_divisions
        # Create new elements based on these nodes and edges
        for i in range(len(edges)):
            start_global = element.global_coordinates[0] + i * global_increment
            end_global = start_global + global_increment
            new_element_global_coords = (start_global, end_global)
            new_element = Element(element.id * 10 + i, (nodes[i].coords[0], nodes[i+1].coords[0]), new_element_global_coords)
            new_elements.append(new_element)
    return all_nodes, all_edges, new_elements
