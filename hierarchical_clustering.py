import copy
from weighted_modularity import get_modularity, get_partial_modularity2
from weighted_network import Network


def hierarchical_clustering(network):
    n_nodes = network.get_node_count()
    adj_list = network.get_adj_list()
    com_adj_list = copy.deepcopy(adj_list)
    loops = network.get_loops()
    outer = network.get_outer()
    n_communities = n_nodes
    adj_matrix = generate_adjacency_matrix(adj_list, n_nodes)
    similarity = calculate_similarity(adj_matrix, n_nodes)
    similarity.sort(key=lambda triple: triple[2])
    partition = [i for i in range(n_nodes)]
    community = [[i] for i in range(n_nodes)]
    modularity = get_modularity(network, partition)
    max_modularity = modularity
    best_partition = format_communities(community)
    for pair in similarity:
        if n_communities == 1:
            break
        if partition[pair[0]] != partition[pair[1]]:
            n_communities -= 1
            part1 = partition[pair[0]]
            part2 = partition[pair[1]]
            common = com_adj_list[part1].get(part2, 0)
            new_inner = loops[part1] + loops[part2] + common
            new_outer = outer[part1] + outer[part2] - 2 * common
            modularity += get_partial_modularity2(network.get_edge_count(), partition[pair[0]],
                                                  partition[pair[1]], loops, outer, new_inner, new_outer)
            merge_communities(pair[0], pair[1], partition, community, com_adj_list, loops, outer)
            if modularity > max_modularity:
                max_modularity = modularity
                best_partition = copy.deepcopy(community)
    return format_communities(best_partition), max_modularity


def merge_communities(node1, node2, partition, community, com_adj_list, loops, outer):
    part1, part2 = partition[node1], partition[node2]
    if len(community[part1]) < len(community[part2]):
        part1, part2 = part2, part1
    common = com_adj_list[part1].get(part2, 0)
    loops[part1] += loops[part2] + common
    outer[part1] += outer[part2] - 2 * common
    if part1 in com_adj_list[part2]:
        del com_adj_list[part2][part1]
        del com_adj_list[part1][part2]
    for com, weight in com_adj_list[part2].items():
        del com_adj_list[com][part2]
        com_adj_list[com][part1] = com_adj_list[com].get(part1, 0) + weight
        com_adj_list[part1][com] = com_adj_list[part1].get(com, 0) + weight
    for node in community[part2]:
        partition[node] = part1
    community[part1].extend(community[part2])
    community[part2] = []


def generate_adjacency_matrix(adj_list, n_nodes):
    adj_matrix = [[0 for _ in range(n_nodes)] for _ in range(n_nodes)]
    for node1 in range(n_nodes):
        for node2 in adj_list[node1]:
            adj_matrix[node1][node2] = 1
    return adj_matrix


def calculate_similarity(adj_matrix, n_nodes):
    similarity = []
    for node1 in range(n_nodes):
        for node2 in range(node1 + 1, n_nodes):
            similarity.append((node1, node2, distance(adj_matrix[node1], adj_matrix[node2], node1, node2)))
    return similarity


#  calculates Hamming distance between two binary vectors
def distance(vec1, vec2, ind1, ind2):
    dist = 0
    for i in range(len(vec1)):
        if i != ind1 and i != ind2 and vec1[i] != vec2[i]:
            dist += 1
    return dist


def format_communities(community):
    formated_community = []
    for i in range(len(community)):
        if community[i]:
            formated_community.append(community[i])
    return formated_community

# network = Network([0, 1, 2, 3, 4], [(0, 1), (1, 2), (0, 3)])
# print(hierarchical_clustering(network))
