def get_modularity(nodes, edges, partition):
    n_nodes = len(nodes)
    n_edges = len(edges)
    adj_list = [[] for _ in range(n_nodes)]
    for edge in edges:
        adj_list[edge[0]].append(edge[1])
        adj_list[edge[1]].append(edge[0])
    n_communities = max(partition) + 1
    inner_degs = n_communities * [0]
    total_degs = n_communities * [0]
    for node1 in range(n_nodes):
        total_degs[partition[node1]] += len(adj_list[node1])
    for i in range(n_communities):
        total_degs[i] /= 2 * n_edges
    for node1 in range(n_nodes):
        part = partition[node1]
        for node2 in adj_list[node1]:
            if node1 < node2 and part == partition[node2]:
                inner_degs[partition[node1]] += 1
    for i in range(n_communities):
        inner_degs[i] /= n_edges
    modularity = 0
    for i in range(0, n_communities):
        modularity += inner_degs[i] - total_degs[i] * total_degs[i]
    return modularity
