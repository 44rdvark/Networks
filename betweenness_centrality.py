import copy
from collections import deque
import networkx as nx

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
