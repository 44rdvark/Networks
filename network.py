import networkx as nx

from cnm_network import CNMNetwork


class Network(object):

    def __init__(self, nodes, edges):
        self.__n_nodes = len(nodes)
        self.__n_edges = len(edges)
        self.__edges = edges
        self.__nodes = [[n] for n in nodes]
        self.__loops = [0] * self.__n_nodes  # total weight of all loops going out of vertex
        self.__outer = [0] * self.__n_nodes  # total weight of all non-loops going out of vertex
        self.__adj_list = [{} for _ in range(self.__n_nodes)]
        for (v1, v2) in edges:
            self.__adj_list[v1][v2] = 1
            self.__adj_list[v2][v1] = 1
            self.__outer[v1] += 1
            self.__outer[v2] += 1

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

    def get_outer(self):
        return self.__outer

    # merges nodes belonging to the same partition
    def merge_nodes(self, partition):
        m = max(partition) + 1
        adj_list = [{} for _ in range(m)]
        loops = [0] * m
        outer = [0] * m
        for node in range(self.__n_nodes):
            loops[partition[node]] += self.__loops[node]
            outer[partition[node]] += self.__outer[node]
        for node1 in range(self.__n_nodes):
            part1 = partition[node1]
            for node2, weight in self.__adj_list[node1].items():
                part2 = partition[node2]
                if part1 != part2:
                    adj_list[part1][part2] = adj_list[part1].get(part2, 0) + weight
                else:
                    loops[part1] += weight
                    outer[part1] -= weight
        nodes = [[] for _ in range(m)]
        for node in range(self.__n_nodes):
            nodes[partition[node]].extend(self.__nodes[node])
        self.__n_nodes = m
        self.__nodes = nodes
        self.__adj_list = adj_list
        self.__loops = loops
        self.__outer = outer

    # for testing
    def to_cnm_network(self):
        return CNMNetwork(self.__nodes, self.__edges)

    # for testing
    def to_networkx_graph(self):
        g = nx.Graph()
        for n in range(self.__n_nodes):
            g.add_node(n)
            for m in self.__adj_list[n]:
                g.add_edge(n, m)
        return g
