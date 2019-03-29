from delta_mod import DeltaMod
from max_heap import MaxHeap
from hierarchical_clustering import format_communities


def clauset_newman_moore(network):
    n_nodes = network.get_node_count()
    community_edges = network.get_community_edges()
    global_heap = network.get_global_heap()
    community_heaps = network.get_community_heaps()
    adj_list = network.get_adj_list()
    deltas = network.get_deltas()
    modularity = 0
    for edges in community_edges:
        modularity -= edges * edges
    partitioning = [[i] for i in range(n_nodes)]
    while not global_heap.empty() and global_heap.top().get_value() > 0:
        top = global_heap.pop()
        coms = top.get_nodes()
        modularity += top.get_value()
        merge_communities(coms, community_edges, community_heaps,
                          global_heap, adj_list, deltas, partitioning)
    return format_communities(partitioning), modularity


def merge_communities(coms, community_edges, community_heaps, global_heap,
                      adj_list, deltas, partitioning):
    adj1, adj2 = adj_list[coms[0]], adj_list[coms[1]]
    deltas1, deltas2 = deltas[coms[0]], deltas[coms[1]]
    adj_row = []
    new_adj = {}
    partitioning[coms[0]].extend(partitioning[coms[1]])
    partitioning[coms[1]] = None
    global_heap.remove(community_heaps[coms[1]].top().get_position(1))
    del adj1[coms[1]]
    del adj2[coms[0]]
    for com, pos2 in adj2.items():
        pos1 = adj1.get(com, None)
        if pos1 is not None:
            delta_mod = deltas1[pos1].get_value() + deltas2[pos2].get_value()
        else:
            delta_mod = deltas2[pos2].get_value() - 2 * community_edges[coms[0]] * community_edges[com]
        adj_row.append(DeltaMod(delta_mod, (coms[0], com)))
        top1 = community_heaps[com].top()
        if pos1 is not None:
            remove_from_heap(coms[0], adj_list[com], deltas[com], community_heaps[com], global_heap)
        insertion_pos = remove_from_heap(coms[1], adj_list[com], deltas[com], community_heaps[com], global_heap)
        insert_to_heap(com, coms[0], insertion_pos, delta_mod, adj_list[com], deltas[com], community_heaps[com])
        top2 = community_heaps[com].top()
        if top1 is not top2:
            global_heap.remove(top1.get_position(1))
            global_heap.push(top2)
    for com, pos1 in adj1.items():
        if com not in adj2:
            delta_mod = deltas1[pos1].get_value() - 2 * community_edges[coms[1]] * community_edges[com]
            adj_row.append(DeltaMod(delta_mod, (coms[0], com)))
            top1 = community_heaps[com].top()
            insertion_pos = remove_from_heap(coms[0], adj_list[com], deltas[com], community_heaps[com], global_heap)
            insert_to_heap(com, coms[0], insertion_pos, delta_mod, adj_list[com], deltas[com], community_heaps[com])
            top2 = community_heaps[com].top()
            if top1 is not top2:
                global_heap.remove(top1.get_position(1))
                global_heap.push(top2)
    for i in range(len(adj_row)):
        new_adj[adj_row[i].get_nodes()[1]] = i
    adj_list[coms[0]] = new_adj
    deltas[coms[0]] = adj_row
    adj_list[coms[1]] = None
    community_heaps[coms[0]] = MaxHeap(adj_row, 0)
    community_heaps[coms[1]] = None
    if not community_heaps[coms[0]].empty():
        global_heap.push(community_heaps[coms[0]].top())
    community_edges[coms[0]] += community_edges[coms[1]]
    return


def insert_to_heap(com, com1, pos, delta_mod, adj, deltas, heap):
    deltas[pos] = DeltaMod(delta_mod, (com, com1))
    adj[com1] = pos
    heap.push(deltas[pos])


def remove_from_heap(com1, adj, deltas, com_heap, global_heap):
    pos = adj[com1]
    com_heap.remove(deltas[pos].get_position(0))
    del adj[com1]
    return pos

