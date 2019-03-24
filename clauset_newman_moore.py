from delta_mod import DeltaMod


def clauset_newman_moore(network):
    n_nodes = network.get_node_count()
    community_edges = network.get_community_edges()
    global_heap = network.get_global_heap()
    community_heaps = network.get_community_heaps()
    adj_list = network.get_adj_list()
    delta_modularities = network.get_delta_modularities()
    modularity = sum(community_edges)
    partitioning = [[i] for i in range(n_nodes)]
    while not global_heap.empty() and global_heap.top() > 0:
        top = global_heap.pop()
        com1, com2 = top.get_nodes()
        positions = top.get_positions()
        pos1, pos2 = positions[0], positions[1]
        heap1, heap2 = community_heaps[com1], community_heaps[com2]
        adj1, adj2 = adj_list[com1], adj_list[com2]
        deltas1, deltas2 = delta_modularities[com1], delta_modularities[com2]
        neighbours = []
        new_adj = {}
        modularity += top.get_value()
        community_edges[com1] += community_edges[com2]
        partitioning[com1].append(partitioning[com2])
        partitioning[com2] = 0
        global_heap.remove(pos1)
        global_heap.remove(pos2)
        del adj1[com2]
        del adj2[com1]
        for com, pos2 in adj2.items():
            pos1 = adj1.get(com, None)
            if pos1 is not None:
                delta_mod = deltas1[pos1].get_value() + deltas2[pos2].get_value()
            else:
                delta_mod = deltas2[pos2].get_value() - 2 * community_edges[com1] * community_edges[com2]
            neighbours.append(DeltaMod(delta_mod, (com1, com), len(neighbours)))

    return

def merge_communities():
    return
