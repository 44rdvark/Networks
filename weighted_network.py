import networkx as nx


class Network(object):

    def __init__(self, nodes, edges):
        self.__n_nodes = len(nodes)
        self.__n_edges = len(edges)
        self.__nodes = [[n] for n in nodes]
        self.__loops = [0] * self.__n_nodes
        self.__adj_list = [[] for _ in range(self.__n_nodes)]
        for (v1, v2) in edges:
            self.__adj_list[v1].append((v2, 1))
            self.__adj_list[v2].append((v1, 1))

    def get_nodes(self):
        return self.__nodes

    def get_node_count(self):
        return self.__n_nodes

    def get_edge_count(self):
        return self.__n_edges

    def get_adj_list(self):
        return self.__adj_list

    def get_loops(self):
        return self.__loops

    # merges nodes belonging to the same partition
    def merge_nodes(self, partition):
        m = max(partition) + 1
        adj_matrix = [[0 for _ in range(m)] for _ in range(m)]
        for node in range(self.__n_nodes):
            for (neighbour, weight) in self.__adj_list[node]:
                part1 = partition[node]
                part2 = partition[neighbour]
                if part1 != part2:
                    adj_matrix[part1][part2] += weight
                elif node < neighbour:
                    adj_matrix[part1][part2] += weight
        adj_list = [[] for _ in range(m)]
        loops = [0] * m
        for node in range(self.__n_nodes):
            loops[partition[node]] += self.__loops[node]
        for node1 in range(m):
            for node2 in range(m):
                if adj_matrix[node1][node2] != 0:
                    if node1 != node2:
                        adj_list[node1].append((node2, adj_matrix[node1][node2]))
                    else:
                        loops[node1] += adj_matrix[node1][node2]
        nodes = [[] for _ in range(m)]
        for node in range(self.__n_nodes):
            nodes[partition[node]].extend(self.__nodes[node])
        self.__n_nodes = m
        self.__nodes = nodes
        self.__adj_list = adj_list
        self.__loops = loops

    # for testing purposes
    def to_networkx_graph(self):
        g = nx.Graph()
        for n in range(self.__n_nodes):
            g.add_node(n)
            for m in self.__adj_list[n]:
                g.add_edge(n, m[0])
        return g
