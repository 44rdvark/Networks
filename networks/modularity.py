def get_modularity2(adj_list, partition):
    n_nodes = len(adj_list)
    n_edges = sum(len(adj_list[i]) for i in range(n_nodes)) / 2
    n_communities = max(partition) + 1
    inner_degs = n_communities * [0]
    total_degs = n_communities * [0]
    for node in range(n_nodes):
        total_degs[partition[node]] += len(adj_list[node])
    for node1 in range(n_nodes):
        part = partition[node1]
        for node2 in adj_list[node1]:
            if node1 < node2 and part == partition[node2]:
                inner_degs[part] += 1
    modularity = 0
    for i in range(n_communities):
        modularity += inner_degs[i] / n_edges - total_degs[i] * total_degs[i] / (4 * n_edges * n_edges)
    return modularity


def get_modularity(network, partition):
    adj_list = network.get_adj_list()
    n_nodes = network.get_node_count()
    n_communities = max(partition) + 1
    n_edges = network.get_edge_count()
    loops = network.get_loops()
    inner_degs = n_communities * [0]
    total_degs = n_communities * [0]
    for node in range(n_nodes):
        total_degs[partition[node]] += 2 * loops[node]
        inner_degs[partition[node]] += loops[node]
    for node1 in range(n_nodes):
        for weight in adj_list[node1].values():
            total_degs[partition[node1]] += weight
    for i in range(n_communities):
        total_degs[i] /= 2 * n_edges
    for node1 in range(n_nodes):
        part = partition[node1]
        for (node2, weight) in adj_list[node1].items():
            if node1 < node2 and part == partition[node2]:
                inner_degs[part] += weight
    for i in range(n_communities):
        inner_degs[i] /= n_edges
    modularity = 0
    for i in range(0, n_communities):
        modularity += inner_degs[i] - total_degs[i] * total_degs[i]
    return modularity


def get_modularity_fast(network, n_communities, inner_degs, outer_degs):
    n_edges = network.get_edge_count()
    modularity = 0
    for i in range(0, n_communities):
        modularity += inner_degs[i] / n_edges - ((outer_degs[i] + inner_degs[i]) / (2 * n_edges)) ** 2
    return modularity


def get_modularity_change(n_edges, com1, com2, inner_degs, outer_degs):
    return (inner_degs[com1] + inner_degs[com2]) / n_edges \
           - ((outer_degs[com1] + inner_degs[com1]) / (2 * n_edges)) ** 2 \
           - ((outer_degs[com2] + inner_degs[com2]) / (2 * n_edges)) ** 2


def get_modularity_change2(n_edges, com1, com2, inner_degs, outer_degs, new_inner, new_outer):
    return new_inner / n_edges - ((2 * new_inner + new_outer) / (2 * n_edges)) ** 2 \
           - ((inner_degs[com1] + inner_degs[com2]) / n_edges
              - ((outer_degs[com1] + 2 * inner_degs[com1]) / (2 * n_edges)) ** 2
              - ((outer_degs[com2] + 2 * inner_degs[com2]) / (2 * n_edges)) ** 2)
