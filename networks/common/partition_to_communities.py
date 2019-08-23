def get_partitioning(communities):
    n_nodes = sum(len(c) for c in communities)
    partitioning = [0] * n_nodes
    for i in range(len(communities)):
        for node in communities[i]:
            partitioning[node] = i
    return partitioning

