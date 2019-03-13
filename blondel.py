from weighted_modularity import get_modularity


# TODO make it so that network is preserved
def blondel(network):
    improvement_outer = True
    while improvement_outer:
        improvement_outer = False
        adj_list = network.get_adj_list()
        n_nodes = network.get_node_count()
        partition = [i for i in range(n_nodes)]
        max_modularity = get_modularity(network, partition)
        improvement = True
        while improvement:
            improvement = False
            for node1 in range(n_nodes):
                for (node2, _) in adj_list[node1]:
                    if partition[node1] != partition[node2]:
                        old_partition = partition[node1]
                        partition[node1] = partition[node2]
                        modularity = get_modularity(network, partition)
                        if modularity > max_modularity:
                            max_modularity = modularity
                            improvement = True
                            improvement_outer = True
                        else:
                            partition[node1] = old_partition
        partition = relabel(partition)
        network.merge_nodes(partition)
    return network.get_nodes()


# change partition labels so that they're within range [0, partition count)
def relabel(partition):
    length = len(partition)
    min_label = 0
    labels = [None for _ in range(length)]
    for i in range(length):
        if labels[partition[i]] is None:
            labels[partition[i]] = min_label
            min_label += 1
    for i in range(length):
        partition[i] = labels[partition[i]]
    return partition

#network = Network([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (3, 5), (6, 7), (7, 8), (6, 8)])
#print(blondel(network))