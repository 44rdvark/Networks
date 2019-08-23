COMMUNITY_HEAP = 0
GLOBAL_HEAP = 1

# Implementation of Clauset-Newman-Moore algorithm - refer to:
# Clauset, A., Newman, M. E. J., and Moore, C. (2004). Finding community structure
# in very large networks. Phys. Rev. E, 70(6):066111.


def clauset_newman_moore(nodes, edges):
    n_nodes = len(nodes)
    n_edges = len(edges)
    community_edges = [0] * n_nodes
    adj_list = [{} for _ in range(n_nodes)]
    community_heaps = [None] * n_nodes
    deltas = [[] for _ in range(n_nodes)]
    global_heap = MaxHeap([], GLOBAL_HEAP)

    for (v1, v2) in edges:
        community_edges[v1] += 1
        community_edges[v2] += 1

    for (v1, v2) in edges:
        if v1 > v2:
            v1, v2 = v2, v1
        position1 = len(deltas[v1])
        position2 = len(deltas[v2])
        delta_mod = 1 / n_edges - community_edges[v1] * community_edges[v2] \
                    / (2 * n_edges * n_edges)
        deltas[v1].append(DeltaMod(delta_mod, (v1, v2)))
        deltas[v2].append(DeltaMod(delta_mod, (v2, v1)))
        adj_list[v1][v2] = position1
        adj_list[v2][v1] = position2

    for i in range(n_nodes):
        community_heaps[i] = MaxHeap(deltas[i], COMMUNITY_HEAP)
        if not community_heaps[i].empty():
            global_heap.push(community_heaps[i].top())

    for i in range(n_nodes):
        community_edges[i] /= 2 * n_edges

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
    global_heap.remove(community_heaps[coms[1]].top().get_position(GLOBAL_HEAP))
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
            remove_from_heap(coms[0], adj_list[com], deltas[com], community_heaps[com])
        insertion_pos = remove_from_heap(coms[1], adj_list[com], deltas[com], community_heaps[com])
        insert_to_heap(com, coms[0], insertion_pos, delta_mod, adj_list[com], deltas[com], community_heaps[com])
        top2 = community_heaps[com].top()
        if top1 is not top2:
            global_heap.remove(top1.get_position(GLOBAL_HEAP))
            global_heap.push(top2)
    for com, pos1 in adj1.items():
        if com not in adj2:
            delta_mod = deltas1[pos1].get_value() - 2 * community_edges[coms[1]] * community_edges[com]
            adj_row.append(DeltaMod(delta_mod, (coms[0], com)))
            top1 = community_heaps[com].top()
            insertion_pos = remove_from_heap(coms[0], adj_list[com], deltas[com], community_heaps[com])
            insert_to_heap(com, coms[0], insertion_pos, delta_mod, adj_list[com], deltas[com], community_heaps[com])
            top2 = community_heaps[com].top()
            if top1 is not top2:
                global_heap.remove(top1.get_position(GLOBAL_HEAP))
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


def remove_from_heap(com1, adj, deltas, com_heap):
    pos = adj[com1]
    com_heap.remove(deltas[pos].get_position(COMMUNITY_HEAP))
    del adj[com1]
    return pos


def format_communities(partitioning):
    formated = []
    for i in range(len(partitioning)):
        if partitioning[i]:
            formated.append(partitioning[i])
    return formated


# value - value of modularity delta
# nodes - nodes representing communities between which modularity delta is calculated
# positions - positions of this DeltaMod instance in global and community heaps
class DeltaMod(object):
    def __init__(self, value, nodes):
        self.__value = value
        self.__nodes = nodes
        self.__positions = [None, None]

    def get_position(self, which):
        return self.__positions[which]

    def set_position(self, which, value):
        self.__positions[which] = value

    def get_nodes(self):
        return self.__nodes

    def set_nodes(self, nodes):
        self.__nodes = nodes

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value

    def __eq__(self, other):
        return self.__value == other.get_value()

    def __lt__(self, other):
        return self.__value < other.get_value()


#  Stores objects of type DeltaMod
#  Preserves position in heap of DeltaMod instance in DeltaMod's 'position' field
class MaxHeap:

    #  'which' field defines whether heap stores global modularity maxima or community modularity values
    def __init__(self, data, which):
        self.__heap = [item for item in data]
        for i in range(len(data)):
            data[i].set_position(which, i)
        self.__which = which
        self.__size = len(data)
        for i in range(int(len(data) / 2), -1, -1):
            self.downheap(i)

    def push(self, item):
        if len(self.__heap) == self.__size:
            self.__heap.append(item)
        else:
            self.__heap[self.__size] = item
        self.__size += 1
        item.set_position(self.__which, self.__size - 1)
        self.upheap(self.__size - 1)

    def remove(self, i):
        if i < self.__size:
            self.__size -= 1
            if i != self.__size:
                self.__swap(i, self.__size)
                self.downheap(i)

    def pop(self):
        self.__swap(0, self.__size - 1)
        self.__size -= 1
        self.downheap(0)
        return self.__heap[self.__size]

    def top(self):
        return self.__heap[0] if self.__size > 0 else None

    def size(self):
        return self.__size

    def upheap(self, i):
        p = int((i - 1) / 2)
        if i != 0 and self.__heap[p] < self.__heap[i]:
            self.__swap(i, p)
            self.upheap(p)

    def downheap(self, i):
        l, r, m = 2 * i + 1, 2 * i + 2, i
        if l < self.size() and self.__heap[l] > self.__heap[i]:
            m = l
        if r < self.size() and self.__heap[r] > self.__heap[m]:
            m = r
        if m != i:
            self.__swap(i, m)
            self.downheap(m)

    def empty(self):
        return self.__size == 0

    def __swap(self, i, j):
        self.__heap[i], self.__heap[j] = self.__heap[j], self.__heap[i]
        self.__heap[i].set_position(self.__which, i)
        self.__heap[j].set_position(self.__which, j)

    def __getitem__(self, i):
        return self.__heap[i]

    def __len__(self):
        return self.__size

