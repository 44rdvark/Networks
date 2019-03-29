import copy
from collections import deque

from modularity import get_modularity2
from betweenness_centrality import update_betweenness_centrality


def girvan_newman(nodes, edges):
    n_nodes = len(nodes)
    adj_list = [set() for _ in range(n_nodes)]
    for edge in edges:
        adj_list[edge[0]].add(edge[1])
        adj_list[edge[1]].add(edge[0])
    original_adj_list = copy.deepcopy(adj_list)
    centrality = [[0] * n_nodes for _ in range(n_nodes)]
    max_centrality = [None] * n_nodes
    n_components, partition = assign_components(adj_list, n_nodes)
    best_partition = copy.deepcopy(partition)
    max_modularity = get_modularity2(original_adj_list, partition)
    while n_components != n_nodes:
        update_betweenness_centrality(adj_list, centrality, nodes)
        update_max_centrality(centrality, max_centrality, nodes)
        absolute_max = max(max_centrality)
        edge = (absolute_max[1], absolute_max[2])  # edge to be removed
        adj_list[edge[0]].remove(edge[1])
        adj_list[edge[1]].remove(edge[0])
        component1 = get_connected_component(adj_list, edge[0], n_nodes)
        nodes = component1
        if edge[1] not in component1:
            component2 = get_connected_component(adj_list, edge[1], n_nodes)
            for node in component2:
                partition[node] = n_components
            n_components += 1
            modularity = get_modularity2(original_adj_list, partition)
            if modularity > max_modularity:
                max_modularity = modularity
                best_partition = copy.deepcopy(partition)
            nodes.extend(component2)
    return max_modularity, best_partition


def update_max_centrality(centrality, max_centrality, nodes):
    for node1 in nodes:
        m = (-1, -1, -1)
        for node2 in nodes:
            if centrality[node1][node2] and centrality[node1][node2] >= m[0]:
                m = (centrality[node1][node2], node1, node2)
        max_centrality[node1] = m


def get_connected_component(adj_list, node, n_nodes):
    visited = [False] * n_nodes
    visited[node] = True
    connected_component = []
    queue = deque()
    queue.append(node)
    while queue:
        node1 = queue.popleft()
        connected_component.append(node1)
        for node2 in adj_list[node1]:
            if not visited[node2]:
                visited[node2] = True
                queue.append(node2)
    return connected_component


def assign_components(adj_list, n_nodes):
    components = [None] * n_nodes
    queue = deque()
    label = 0
    for node1 in range(n_nodes):
        if components[node1] is None:
            queue.append(node1)
            components[node1] = label
            while queue:
                node1 = queue.popleft()
                for node2 in adj_list[node1]:
                    if components[node2] is None:
                        components[node2] = label
                        queue.append(node2)
            label += 1
    return label, components
