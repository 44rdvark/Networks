from delta_mod import DeltaMod
from max_heap import MaxHeap

COMMUNITY_HEAP = 0
GLOBAL_HEAP = 1


class CNMNetwork(object):

    def __init__(self, nodes, edges):
        self.__n_nodes = len(nodes)
        self.__n_edges = len(edges)
        self.__nodes = [[n] for n in nodes]
        self.__community_edges = [0] * self.__n_nodes  # total weight of all edges going out of a community
        self.__adj_list = [{} for _ in range(self.__n_nodes)]
        self.__community_heaps = [None] * self.__n_nodes
        self.__deltas = [[] for _ in range(self.__n_nodes)]
        self.__global_heap = MaxHeap([], GLOBAL_HEAP)
        for (v1, v2) in edges:
            self.__community_edges[v1] += 1
            self.__community_edges[v2] += 1

        for (v1, v2) in edges:
            if v1 > v2:
                v1, v2 = v2, v1
            position1 = len(self.__deltas[v1])
            position2 = len(self.__deltas[v2])
            delta_mod = 1 / self.__n_edges - self.__community_edges[v1] * self.__community_edges[v2] \
                        / (2 * self.__n_edges * self.__n_edges)
            self.__deltas[v1].append(DeltaMod(delta_mod, (v1, v2)))
            self.__deltas[v2].append(DeltaMod(delta_mod, (v2, v1)))
            self.__adj_list[v1][v2] = position1
            self.__adj_list[v2][v1] = position2

        for i in range(self.__n_nodes):
            self.__community_heaps[i] = MaxHeap(self.__deltas[i], COMMUNITY_HEAP)
            if not self.__community_heaps[i].empty():
                self.__global_heap.push(self.__community_heaps[i].top())

        for i in range(self.__n_nodes):
            self.__community_edges[i] /= 2 * self.__n_edges

    def get_nodes(self):
        return self.__nodes

    def get_node_count(self):
        return self.__n_nodes

    def get_edge_count(self):
        return self.__n_edges

    def get_adj_list(self):
        return self.__adj_list

    def get_community_edges(self):
        return self.__community_edges

    def get_global_heap(self):
        return self.__global_heap

    def get_community_heaps(self):
        return self.__community_heaps

    def get_deltas(self):
        return self.__deltas

