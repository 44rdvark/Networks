from copy import deepcopy
from collections import deque


def girvan_newman_foresight(nodes, edges, n_communities_final):
    n_nodes = len(nodes)
    adj_list = [set() for _ in range(n_nodes)]
    for edge in edges:
        adj_list[edge[0]].add(edge[1])
        adj_list[edge[1]].add(edge[0])
    original_adj_list = deepcopy(adj_list)
    centrality = [[0] * n_nodes for _ in range(n_nodes)]
    max_centrality = [None] * n_nodes
    n_components, partition = assign_components(adj_list, n_nodes)
    while n_components != n_communities_final:
        update_betweenness_centrality(adj_list, centrality, nodes)
        update_max_centrality(centrality, max_centrality, nodes)
        absolute_max = max(max_centrality)
        edge = (absolute_max[1], absolute_max[2])  # edge to be removed
        adj_list[edge[0]].remove(edge[1])
        adj_list[edge[1]].remove(edge[0])
        component1 = get_connected_component(adj_list, edge[0])
        nodes = component1
        if edge[1] not in component1:
            component2 = get_connected_component(adj_list, edge[1])
            for node in component2:
                partition[node] = n_components
            n_components += 1
            modularity = get_modularity(original_adj_list, partition)
            nodes.extend(component2)
    return to_community_list(deepcopy(partition)), modularity


def update_max_centrality(centrality, max_centrality, nodes):
    for node1 in nodes:
        m = (-1, -1, -1)
        for node2 in nodes:
            if centrality[node1][node2] and centrality[node1][node2] >= m[0]:
                m = (centrality[node1][node2], node1, node2)
        max_centrality[node1] = m


def get_connected_component(adj_list, node):
    n_nodes = len(adj_list)
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


def get_modularity(adj_list, partition):
    n_nodes = len(adj_list)
    n_edges = sum(len(adj_list[i]) for i in range(n_nodes)) / 2
    n_communities = max(partition) + 1
    inner_degs = n_communities * [0]
    total_degs = n_communities * [0]
    for node in range(n_nodes):
        total_degs[partition[node]] += len(adj_list[node])
    for node1 in range(n_nodes):
        part = partition[node1]
        for node2 in adj_list[node1]:
            if node1 < node2 and part == partition[node2]:
                inner_degs[part] += 1
    modularity = 0
    for i in range(n_communities):
        modularity += inner_degs[i] / n_edges - total_degs[i] * total_degs[i] / (4 * n_edges * n_edges)
    return modularity


#  nodes - a list of nodes of a subgraph for which betweennes has to be updated
#  centrality - a matrix where entry i, j denotes the centrality of the edge (i, j) if such edge exists
def update_betweenness_centrality(adj_list, centrality, nodes):
    n_nodes = len(adj_list)
    for node in nodes:
        for i in range(n_nodes):
            centrality[node][i] = 0
    for v in nodes:
        stack = deque()
        predecessors = [[] for _ in range(n_nodes)]  # predecessors of each node
        n_shortest = [0] * n_nodes
        n_shortest[v] = 1
        distance = [None] * n_nodes
        distance[v] = 0
        queue = deque()
        queue.append(v)
        while queue:
            u = queue.popleft()
            stack.append(u)
            for w in adj_list[u]:
                if distance[w] is None:
                    queue.append(w)
                    distance[w] = distance[u] + 1
                if distance[w] == distance[u] + 1:
                    n_shortest[w] += n_shortest[u]
                    predecessors[w].append(u)
        dependency = [0] * n_nodes
        while stack:
            w = stack.pop()
            for u in predecessors[w]:
                dependency_increase = n_shortest[u] / n_shortest[w] * (1 + dependency[w])
                dependency[u] += dependency_increase
                centrality[w][u] += dependency_increase / 2
                centrality[u][w] += dependency_increase / 2


def to_community_list(partition):
    communities = [[] for _ in range(max(partition) + 1)]
    for node in range(0, len(partition)):
        communities[partition[node]].append(node)
    return communities

