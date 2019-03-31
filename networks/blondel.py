from copy import deepcopy


def blondel(nodes, edges):
    n_nodes = len(nodes)
    n_edges = len(edges)
    communities = [[n] for n in nodes]
    loops = [0] * n_nodes  # total weight of all loops going out of vertex
    outer = [0] * n_nodes  # total weight of all non-loops going out of vertex
    adj_list = [{} for _ in range(n_nodes)]
    for (v1, v2) in edges:
        adj_list[v1][v2] = 1
        adj_list[v2][v1] = 1
        outer[v1] += 1
        outer[v2] += 1
    modularity = sum(-out * out / (4 * n_edges * n_edges) for out in outer)
    improvement_outer = True
    while improvement_outer:
        improvement_outer = False
        com_adj_list = deepcopy(adj_list)
        partition = [i for i in range(n_nodes)]
        com_loops = deepcopy(loops)
        com_outer = deepcopy(outer)
        community = [{i} for i in range(n_nodes)]
        improvement = True
        while improvement:
            improvement = False
            for node1 in range(n_nodes):
                old_common = com_adj_list[node1].get(partition[node1], 0)
                best_delta = 0
                best_community = None
                old_community_id = partition[node1]
                for node2 in adj_list[node1]:
                    if partition[node1] != partition[node2]:
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
                        if modularity2 - modularity1 > best_delta:
                            best_delta = modularity2 - modularity1
                            best_community = community_id
                        partition[node1] = old_community_id
                        com_loops[community_id] -= loops[node1] + common
                        com_outer[community_id] -= outer[node1] - common
                        com_loops[old_community_id] += loops[node1] + old_common
                        com_outer[old_community_id] += outer[node1] - old_common
                if best_delta > 0:
                    improvement = True
                    improvement_outer = True
                    modularity += best_delta
                    partition[node1] = best_community
                    common = com_adj_list[node1][best_community]
                    com_loops[best_community] += loops[node1] + common
                    com_outer[best_community] += outer[node1] - common
                    com_loops[old_community_id] -= loops[node1] + old_common
                    com_outer[old_community_id] -= outer[node1] - old_common
                    community[best_community].add(node1)
                    community[old_community_id].remove(node1)
                    update_community_adjacency(com_adj_list, adj_list, node1, best_community, old_community_id)

        partition = relabel(partition)
        n_nodes, adj_list, loops, outer, communities = merge_nodes(partition, adj_list, loops, outer, communities)
    return communities, modularity


def merge_nodes(partition, adj_list, loops, outer, communities):
    m = max(partition) + 1
    n_nodes = len(adj_list)
    new_adj_list = [{} for _ in range(m)]
    new_loops = [0] * m
    new_outer = [0] * m
    for node in range(n_nodes):
        new_loops[partition[node]] += loops[node]
        new_outer[partition[node]] += outer[node]
    for node1 in range(n_nodes):
        part1 = partition[node1]
        for node2, weight in adj_list[node1].items():
            part2 = partition[node2]
            if part1 != part2:
                new_adj_list[part1][part2] = new_adj_list[part1].get(part2, 0) + weight
            else:
                new_loops[part1] += weight
                new_outer[part1] -= weight
    new_communities = [[] for _ in range(m)]
    for node in range(n_nodes):
        new_communities[partition[node]].extend(communities[node])
    return m, new_adj_list, new_loops, new_outer, new_communities


def get_modularity_change(n_edges, com1, com2, inner_degs, outer_degs):
    return (inner_degs[com1] + inner_degs[com2]) / n_edges \
           - ((outer_degs[com1] + inner_degs[com1]) / (2 * n_edges)) ** 2 \
           - ((outer_degs[com2] + inner_degs[com2]) / (2 * n_edges)) ** 2


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

