import time

from display import display
from evaluate_partition import evaluate
from random import shuffle, uniform

from weighted_modularity import get_modularity
from weighted_network import Network
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


(network, partitioning) = generate_random_network(10, 10, 1, 0)
out, modularity = hierarchical_clustering(network)
print(modularity)

sum1 = sum2 = 0
#for i in range(100):
(network, partitioning) = generate_random_network(10, 100, 0.9, 0.1)
graph = network.to_networkx_graph()
#display(network, partitioning)
old_network = copy.deepcopy(network)
old_partitioning = partitioning
start = time.time()
output = blondel(network)
end = time.time()
print(end - start)
#print(output)
partitioning = get_partitioning(output)
#display(old_network, partitioning)
sum1 += get_modularity(old_network, partitioning)
start = time.time()
out, mod = hierarchical_clustering(old_network)#partition_dict_to_list(community.best_partition(graph))
end = time.time()
print(end - start)
#print(evaluate(old_partitioning, partitioning))
#print(output)
#print(evaluate(old_partitioning, external_part))
sum2 += mod

    #print(out)
    #print(output)
print(sum1, sum2)
