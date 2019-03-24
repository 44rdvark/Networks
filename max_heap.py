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

    def push(self, item):
        if len(self.__heap) == self.__size:
            self.__heap.append(item)
        else:
            self.__heap[self.__size] = item
        self.__size += 1
        item.set_position(self.__size - 1)
        self.upheap(self.__size - 1)
        return

    def pop(self):
        self.__swap(0, self.__size - 1)
        self.__size -= 1
        self.downheap(0)
        return self.__heap[self.__size]

    def top(self):
        return self.heap[0]

    def size(self):
        return self.__size

    def upheap(self, i):
        p = i / 2
        if i != 0 and self.__heap[p] < self.__heap[i]:
            self.__swap(i, p)
            self.upheap(p)

    def downheap(self, i):
        l, r = 2 * i, 2 * i + 1
        if l <= self.size() and self.__heap[l] > self.__heap[i]:
            m = l
        if r <= self.size() and self.__heap[r] > self.__heap[m]:
            m = r
        if m != i:
            self.__swap(i, m)
            self.downheap(m)

    def __swap(self, i, j):
        self.__heap[i], self.heap[j] = self.__heap[j], self.__heap[i]
        self.__heap[i].set_position(self.__which, i)
        self.__heap[j].set_position(self.__which, j)

    def __getitem__(self, i):
        return self.heap[i]

    def __len__(self):
        return self.__size
