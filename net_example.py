#!/bin/python

import networkx

# G : networkx.Graph = networkx.complete_graph(3)
# print(G.size())
# print(G.number_of_edges())
# print(G.nodes())
# G.remove_edge(1,2)
# print(G.edges())


edges = [(0, 1), (0, 3), (3, 4), (3, 6), (6, 7), (1, 2), (1, 4), (4, 5), (4, 7), (7, 8), (2, 5), (5, 8)]

G : networkx.Graph = networkx.Graph()
G.add_edges_from(edges)
print(G.size())
print(G.nodes())
print("all paths")
for path in networkx.all_simple_paths(G, source=0, target=1):
    print(path)

G.remove_node(0)
for path in networkx.all_simple_paths(G, source=2, target=1):
    print(path)
for path in networkx.all_simple_paths(G, source=4, target=1):
    print(path)