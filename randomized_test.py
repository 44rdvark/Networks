import copy

from bruteforce import maximize_modularity
from display import display
from evaluate_partition import evaluate
from random import shuffle, uniform
from weighted_network import Network
from blondel import blondel
import community


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

print("0")
(network, partitioning) = generate_random_network(100, 10, 0.8, 0.2)
print("0")
graph = network.to_networkx_graph()
#display(network, partitioning)
#old_network = copy.deepcopy(network)
print("a")
old_partitioning = partitioning
output = blondel(network)
#partitioning = get_partitioning(output)
#display(old_network, partitioning)
#print(output)
#external_part = partition_dict_to_list(community.best_partition(graph))
print("b")
print(evaluate(old_partitioning, partitioning))
print(evaluate(old_partitioning, external_part))


#(best_partition, max_modularity) = maximize_modularity(network, [], network.get_node_count())
#print(max_modularity, evaluate(partitioning, best_partition))
#display(network, best_partition)
