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
def create_edges_on_line(nodes, cfg):
    edges = []
    for i in range(len(nodes) - 1):
        NodePair = [nodes[i], nodes[i + 1]]
        edges.append(Edge(NodePair, cfg.n_modes, 1))
    return edges


def create_nodes_and_edges(elements, cfg):
    all_nodes, all_edges, new_elements = [], [], []
    for element in elements:
        nodes = create_nodes_on_line(element.local_coordinates[0],
                                     element.local_coordinates[1], cfg.n_elements)
        edges = create_edges_on_line(nodes, cfg)
        all_nodes.append(nodes)
        all_edges.append(edges)
        global_increment = (element.global_coordinates[1] - element.global_coordinates[0]) / cfg.n_elements
        for i in range(len(edges)):
            start_global = element.global_coordinates[0] + i * global_increment
            new_element = Element(element.id * 10 + i,
                                  (nodes[i].coords[0], nodes[i + 1].coords[0]),
                                  (start_global, start_global + global_increment))
            new_elements.append(new_element)
    return all_nodes, all_edges, new_elements
