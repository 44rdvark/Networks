## An overview of algorithms for community detection in networks
My BSc thesis in *Computer Science - IT Analyst* written at Jagiellonian University in 2019.

The paper outlines common properties of networks, formalizes the concept of community detection by introducing a measure known as modularity and provides descriptions of the most popular modularity maximization algorithms, and their pseudocodes. Finally, it includes multiple tests and their analysis, showcasing how different algorithms compare in terms of execution time and the quality of partitions detected. The paper also exemplifies the existence of a resolution limit - the fact that modularity maximization algorithms fail to detect communities smaller than a certain scale. Lastly, it includes a thorough analysis of how the vertex ordering of the network impacts the execution time of Blondel et al. algorithm and provides a useful heuristic for improving it.
### Contents
This project consists of:
1. [The thesis](thesis.pdf) itself
2. [The implementations of algorithms](networks/algorithms) described in it, which include:
- Blondel et al. algorithm
- Clauset-Newman-Moore algorithm
- Girvan-Newman algorithm
- hierarchical clustering algorithm
3. [The tests](networks/test) allowing for comparison of the algorithms' execution time and accuracy in finging proper community detcomposition of networks. Those include:
- randomized tests - run on networks generated in accordance with Girvan-Newman ([paper](https://arxiv.org/abs/cond-mat/0112110)) and Toivonen et al. models ([paper](https://arxiv.org/abs/physics/0601114))
- real-world tests - run on real-world networks taken from [Mark Newman's website](http://www-personal.umich.edu/~mejn/netdata/) and [Stanford Large Networks Dataset Collection](http://snap.stanford.edu/data/)
- resolution limit test - exemplifying the existence of a so called resolution limit in community detection
### Running the project
In order to test the algorithms, use Python 3 to run the scripts located in subdirectories of *networks/test* directory. They do not take any arguments but some require the [networkx library](https://networkx.github.io/) to load contents of .gml files with network data. The descriptions of what the scripts do is provided in comments to respective test files.

The algorithms can also be run directly by executing corresponding functions in each of the four files in *networks/algorithms* directory. They each take two arguments - a list of integers from 0 to n representing nodes of the network and a list of pairs of integers from 0 to n representing its edges. Each of the algorithms returns two values: a list of lists representing communities found by the algorithm and the modularity value of the community partition found.
