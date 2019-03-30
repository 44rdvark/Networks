import time

import networkx as nx
from networks.clauset_newman_moore import clauset_newman_moore
from random import shuffle, uniform

from networks.girvan_newman import girvan_newman
from networks.modularity import get_modularity
from networks.network import Network
from networks.hierarchical_clustering import hierarchical_clustering
from networks.blondel import blondel


# initializes random network with equally sized communities
# returns generated network and expected partitioning
def generate_random_network(n_communities, community_size, prob_inner, prob_outer):
    n_nodes = n_communities * community_size
    nodes = list(range(n_nodes))
    edges = []
    partitioning = list(range(n_communities)) * community_size
    shuffle(partitioning)
    for i in range(0, n_nodes):
        for j in range(i + 1, n_nodes):
            rand = uniform(0, 1)
            if partitioning[i] == partitioning[j] and rand <= prob_inner \
                    or partitioning[i] != partitioning[j] and rand <= prob_outer:
                edges.append((i, j))
    return Network(nodes, edges), partitioning

def generate_random_network2(n_communities, community_size, prob_inner, prob_outer):
    n_nodes = n_communities * community_size
    nodes = list(range(n_nodes))
    edges = []
    partitioning = list(range(n_communities)) * community_size
    shuffle(partitioning)
    for i in range(0, n_nodes):
        for j in range(i + 1, n_nodes):
            rand = uniform(0, 1)
            if partitioning[i] == partitioning[j] and rand <= prob_inner \
                    or partitioning[i] != partitioning[j] and rand <= prob_outer:
                edges.append((i, j))
    return nodes, edges, partitioning

# for testing
def get_partitioning(nodes):
    total_nodes = max([max(nodes[i]) for i in range(len(nodes))]) + 1
    partition = [None] * total_nodes
    for i in range(len(nodes)):
        for node in nodes[i]:
            partition[node] = i
    return partition


# for testing
def partition_dict_to_list(partition):
    size = max(partition) + 1
    partition_list = size * [None]
    for x, y in partition.items():
        partition_list[x] = y
    return partition_list


def downscale(nodes, edges):
    for i in range(len(nodes)):
        nodes[i] = nodes[i] - 1
    for i in range(len(edges)):
        edges[i] = (edges[i][0] - 1, edges[i][1] - 1)
    return


g = nx.read_gml('networks/data/karate.gml', label='id')
nodes = list(g.nodes())
edges = list(g.edges())
downscale(nodes, edges)
#nodes, edges, partitioning = generate_random_network2(10, 10, 0.9, 0.1)
print(len(edges), len(nodes))

network = Network(nodes, edges)
cnm_network = network.to_cnm_network()

start = time.time()
output = blondel(network)
end = time.time()
partitioning = get_partitioning(output)
print("modularity:", get_modularity(network, partitioning))
print("time:", end - start)


start = time.time()
print("modularity: ", girvan_newman(nodes, edges)[0])
end = time.time()
print("time: ", end - start)


start = time.time()
out, mod = hierarchical_clustering(network)
end = time.time()
print("modularity:", mod)
print("time", end - start)


start = time.time()
out, mod = clauset_newman_moore(cnm_network)
end = time.time()
print("modularity:", mod)
print("time", end - start)

