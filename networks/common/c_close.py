from copy import deepcopy


def c_close(nodes, edges, c):
    n_nodes = len(nodes)
    new_edges = deepcopy(edges)
    adj_matrix = [[0 for _ in range(n_nodes)] for _ in range(n_nodes)]
    for edge in edges:
        adj_matrix[edge[0]][edge[1]] += 1
        adj_matrix[edge[1]][edge[0]] += 1
    for node1 in nodes:
        for node2 in nodes:
            if node1 < node2 and adj_matrix[node1][node2] == 0 and common_neighbours(node1, node2, adj_matrix) >= c:
                new_edges.append((node1, node2))
    return new_edges


def common_neighbours(node1, node2, adj_matrix):
    common = 0
    for n in range(len(adj_matrix)):
        if adj_matrix[node1][n] == adj_matrix[node2][n] == 1:
            common += 1
    return common
