import copy

from networks.modularity import get_modularity_change


# TODO make it so that network is preserved
def blondel(network):
    tmp_network = copy.deepcopy(network)
    improvement_outer = True
    while improvement_outer:
        improvement_outer = False
        adj_list = tmp_network.get_adj_list()
        com_adj_list = copy.deepcopy(adj_list)
        n_nodes = tmp_network.get_node_count()
        n_edges = tmp_network.get_edge_count()
        partition = [i for i in range(n_nodes)]
        loops = tmp_network.get_loops()
        outer = tmp_network.get_outer()
        com_loops = copy.deepcopy(loops)
        com_outer = copy.deepcopy(outer)
        community = [set([i]) for i in range(n_nodes)]
        improvement = True
        while improvement:
            improvement = False
            for node1 in range(n_nodes):
                old_common = com_adj_list[node1].get(partition[node1], 0)
                for node2 in adj_list[node1]:
                    if partition[node1] != partition[node2]:
                        old_community_id = partition[node1]
                        partition[node1] = partition[node2]
                        community_id = partition[node2]
                        modularity1 = get_modularity_change(n_edges, community_id, old_community_id,
                                                            com_loops, com_outer)
                        common = com_adj_list[node1][community_id]
                        com_loops[community_id] += loops[node1] + common
                        com_outer[community_id] += outer[node1] - common
                        com_loops[old_community_id] -= loops[node1] + old_common
                        com_outer[old_community_id] -= outer[node1] - old_common
                        modularity2 = get_modularity_change(n_edges, community_id, old_community_id,
                                                            com_loops, com_outer)
                        if modularity2 > modularity1:
                            improvement = True
                            improvement_outer = True
                            community[community_id].add(node1)
                            community[old_community_id].remove(node1)
                            update_community_adjacency(com_adj_list, adj_list, node1, community_id, old_community_id)
                            old_common = common
                        else:
                            partition[node1] = old_community_id
                            com_loops[community_id] -= loops[node1] + common
                            com_outer[community_id] -= outer[node1] - common
                            com_loops[old_community_id] += loops[node1] + old_common
                            com_outer[old_community_id] += outer[node1] - old_common
        partition = relabel(partition)
        tmp_network.merge_nodes(partition)
    return tmp_network.get_nodes()


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


def update_community_adjacency(com_adj_list, adj_list, node, community, old_community):
    for neighbour, weight in adj_list[node].items():
        com_adj_list[neighbour][community] = com_adj_list[neighbour].get(community, 0) + weight
        if com_adj_list[neighbour][old_community] == weight:
            del com_adj_list[neighbour][old_community]
        else:
            com_adj_list[neighbour][old_community] -= weight

