class CNMNetwork(object):

    def __init__(self, nodes, edges):
        self.__n_nodes = len(nodes)
        self.__n_edges = len(edges)
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

