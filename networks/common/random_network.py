
# initializes random network with equally sized communities
# returns nodes and edges of generated network and expected partitioning
from random import shuffle, uniform, sample


def generate_synthetic_network(n_communities, community_size, prob_inner, prob_outer):
    n_nodes = n_communities * community_size
    nodes = list(range(n_nodes))
    edges = []
    partitioning = list(range(n_communities)) * community_size
    shuffle(partitioning)
    for i in range(0, n_nodes):
        for j in range(i + 1, n_nodes):
            rand = uniform(0, 1)
            if partitioning[i] == partitioning[j] and rand <= prob_inner \
                    or partitioning[i] != partitioning[j] and rand <= prob_outer:
                edges.append((i, j))
    return nodes, edges, partitioning


def generate_social_network(nodes, adj_list, goal_nodes, prob_prim, prob_sec):
    for i in range(1, len(prob_prim)):
        prob_prim[i] += prob_prim[i - 1]
    for i in range(1, len(prob_sec)):
        prob_sec[i] += prob_sec[i - 1]
    while goal_nodes - len(nodes) > 0:
        r_prim = uniform(0, 1)
        r_sec = uniform(0, 1)
        prim = sec = 0
        while r_prim > prob_prim[prim]:
            prim += 1
        while r_sec > prob_sec[sec]:
            sec += 1
        prim += 1
        cont_prim = sample(nodes, min(len(nodes), prim))
        cont_sec = []
        for n in cont_prim:
            adj = adj_list[n]
            for k in cont_prim:
                adj.discard(k)
            for s in cont_sec:
                adj.discard(s)
            cont_sec.extend(sample(list(adj), min(len(adj), sec)))
        nodes.append(len(nodes))
        cont_prim.extend(cont_sec)
        adj_list.append(set(cont_prim))
        for i in adj_list[len(adj_list) - 1]:
            adj_list[i].add(len(adj_list) - 1)
    edges = []
    for i in range(len(adj_list)):
        for j in adj_list[i]:
            if i < j:
                edges.append((i, j))
    return nodes, edges

