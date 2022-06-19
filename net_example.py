#!/bin/python

#import networkx


# First start xserver on Windows (WSL settings)
# ./vcxsrv.exe :0 -multiwindow -clipboard -wgl -ac

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use('TkAgg')


#subplot(r,c) provide the no. of rows and columns
f, ax = plt.subplots(2,1)

a_1 = [
        [[43, 120, 227], [66, 245, 78], [66, 245, 78]],
        [[43, 120, 227], [245, 84, 66], [66, 245, 78]],
        [[43, 120, 227], [66, 245, 78], [66, 245, 78]]
      ]
a_2 = [[[43, 120, 227], [66, 245, 78], [66, 245, 78]], [[43, 120, 227], [245, 84, 66], [43, 120, 227]], [[43, 120, 227], [43, 120, 227], [43, 120, 227]]]

# use the created array to output your multiple images. In this case I have stacked 4 images vertically
ax[0].imshow(a_1)
ax[1].imshow(a_2)

# t = np.arange(0.0, 2.0, 0.01)
# s = 1 + np.sin(2*np.pi*t)
# plt.plot(t, s)

# plt.title('About as simple as it gets, folks')
plt.show()

exit(0)

l = [1,2,3,4,5,6,7]
def get_inner_paths(path_list):
    r = []
    for i in range(1, len(path_list)-1):
        r.append(path_list[i:])
    return r

print(get_inner_paths(l))


# G : networkx.Graph = networkx.complete_graph(3)
# print(G.size())
# print(G.number_of_edges())
# print(G.nodes())
# G.remove_edge(1,2)
# print(G.edges())


# edges = [(0, 1), (0, 3), (3, 4), (3, 6), (6, 7), (1, 2), (1, 4), (4, 5), (4, 7), (7, 8), (2, 5), (5, 8)]

# G : networkx.Graph = networkx.Graph()
# G.add_edges_from(edges)
# print(G.size())
# print(G.nodes())
# print("all paths")
# for path in networkx.all_simple_paths(G, source=0, target=1):
#     print(path)

# G.remove_node(0)
# for path in networkx.all_simple_paths(G, source=2, target=1):
#     print(path)
# for path in networkx.all_simple_paths(G, source=4, target=1):
#     print(path)