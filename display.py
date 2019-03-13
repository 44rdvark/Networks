import networkx as nx
import matplotlib.pyplot as plt

color = ["red", "green", "blue", "purple", "yellow", "orange", "cyan", "grey", "pink", "black"]


def display(network, partitioning):
    graph = nx.Graph()
    n_nodes = network.get_node_count()
    adj_list = network.get_adj_list()
    graph.add_nodes_from([n for [n] in network.get_nodes()])
    graph.add_edges_from([(i, j) for i in range(n_nodes) for (j, _) in adj_list[i] if i < j])
    color_map = n_nodes * [0]
    for i in range(n_nodes):
        color_map[i] = color[partitioning[i]]

    nx.draw(graph, node_color=color_map)
    plt.show()
