import copy

from weighted_modularity import get_modularity, get_modularity_fast


# TODO make it so that network is preserved
def blondel(network):
    improvement_outer = True
    while improvement_outer:
        improvement_outer = False
        adj_list = network.get_adj_list()
        n_nodes = network.get_node_count()
        partition = [i for i in range(n_nodes)]
        loops = network.get_loops()
        outer = network.get_outer()
        com_loops = copy.deepcopy(loops)
        com_outer = copy.deepcopy(outer)
        community = [[i] for i in range(n_nodes)]
        max_modularity = get_modularity_fast(network, n_nodes, com_loops, com_outer)
        improvement = True
        while improvement:
            improvement = False
            for node1 in range(n_nodes):
                for node2 in adj_list[node1]:
                    if partition[node1] != partition[node2]:
                        old_community_id = partition[node1]
                        partition[node1] = partition[node2]
                        community_id = partition[node2]
                        common = count_common_edges(community[community_id], node1, adj_list)
                        old_common = count_common_edges(community[old_community_id], node1, adj_list)
                        com_loops[community_id] += loops[node1] + common
                        com_outer[community_id] += outer[node1] - common
                        com_loops[old_community_id] -= loops[node1] + old_common
                        com_outer[old_community_id] -= outer[node1] - old_common
                        modularity = get_modularity_fast(network, n_nodes, com_loops, com_outer)
                        if modularity > max_modularity:
                            max_modularity = modularity
                            improvement = True
                            improvement_outer = True
                            community[partition[node2]].append(node1)
                        else:
                            partition[node1] = old_community_id
                            com_loops[community_id] -= loops[node1] + common
                            com_outer[community_id] -= outer[node1] - common
                            com_loops[old_community_id] += loops[node1] + old_common
                            com_outer[old_community_id] += outer[node1] - old_common
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


# sum the weights of edges between a node and a community
def count_common_edges(community, node, adj_list):
    sum = 0
    for community_node in community:
        sum += adj_list[node].get(community_node, 0)
    return sum
