import networkx as nx
import matplotlib.pyplot as plt

color = ["red", "green", "yellow", "cyan", "grey", "orange", "wheat", "olive", "purple", "blue", "pink", "lime",
         "fuchsia", "lightgrey", "skyblue", "lightblue", "plum", "lightseagreen"]

pos = None


def display(nodes, edges, communities):
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    n_nodes = len(nodes)
    partitioning = get_partitioning(communities, n_nodes)
    color_map = n_nodes * [0]
    for i in range(n_nodes):
        color_map[i] = color[partitioning[i]]
    global pos
    if pos is None:
        pos = nx.spring_layout(graph)
    nx.draw(graph, with_labels=True, node_color=color_map, pos=pos)
    plt.show()


def get_partitioning(communities, n_nodes):
    partitioning = [0] * n_nodes
    for i in range(len(communities)):
        for node in communities[i]:
            partitioning[node] = i
    return partitioning
