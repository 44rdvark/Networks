import time

import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman as gn
from clauset_newman_moore import clauset_newman_moore
from display import display
from evaluate_partition import evaluate
from random import shuffle, uniform

from girvan_newman import girvan_newman
from modularity import get_modularity
from cnm_network import CNMNetwork
from network import Network
from hierarchical_clustering import hierarchical_clustering
from blondel import blondel
import community
import copy


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


g = nx.read_gml('karate.gml', label='id')
comp = gn(g)
for c in comp:
    print(c)
nodes = list(g.nodes())
edges = list(g.edges())
downscale(nodes, edges)
#nodes, edges, partitioning = generate_random_network2(10, 10, 0.9, 0.1)
print(girvan_newman(nodes, edges))
'''
g = nx.read_gml('lesmis.gml', label='id')
(network, partitioning) = generate_random_network(30, 100, 0.8, 0.2)
print(network.get_edge_count())
nodes = list(g.nodes())
edges = list(g.edges())
print(len(nodes), len(edges))
#downscale(nodes, edges)
#network = Network(nodes, edges)
cnm_network = network.to_cnm_network()
graph = network.to_networkx_graph()
start = time.time()
#old_network = copy.deepcopy(network)
output = blondel(network)
end = time.time()
print("time:", end - start)
partitioning = get_partitioning(output)
print("modularity:", get_modularity(network, partitioning))
start = time.time()
out, mod = clauset_newman_moore(cnm_network)
print(community.modularity(community.best_partition(g), g))
end = time.time()
print("time", end - start)
print("modularity:", mod)
'''