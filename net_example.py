#!/bin/python

#import networkx



class T:
    def __init__(self, value):
        self.value = value

    def __eq__(self, __o) -> bool:
        if isinstance(__o, int):
            return self.value == __o
        else:
            return self.value == __o.value


l = [T(1), T(2), T(3)]

print(1 if 4 in l else 0)
#exit(0)


# First start xserver on Windows (WSL settings)
# ./vcxsrv.exe :0 -multiwindow -clipboard -wgl -ac


# import numpy as np
# import matplotlib.pyplot as plt

# X = np.random.rand(100, 1000)
# xs = np.mean(X, axis=1)
# ys = np.std(X, axis=1)

# fig, ax = plt.subplots()
# ax.set_title('click on point to plot time series')
# line, = ax.plot(xs, ys, 'o', picker=True, pickradius=5)  # 5 points tolerance


# def onpick(event):
#     if event.artist != line:
#         return
#     n = len(event.ind)
#     if not n:
#         return
#     fig, axs = plt.subplots(n, squeeze=False)
#     for dataind, ax in zip(event.ind, axs.flat):
#         ax.plot(X[dataind])
#         ax.text(0.05, 0.9,
#                 f"$\\mu$={xs[dataind]:1.3f}\n$\\sigma$={ys[dataind]:1.3f}",
#                 transform=ax.transAxes, verticalalignment='top')
#         ax.set_ylim(-0.5, 1.5)
#     fig.show()
#     return True


# fig.canvas.mpl_connect('pick_event', onpick)
# plt.show()

# exit(1)

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pprint

matplotlib.use('TkAgg')


#subplot(r,c) provide the no. of rows and columns
f, ax = plt.subplots(2,1)

a_1 = [
        [(43, 120, 227), (66, 245, 78), (66, 245, 78)],
        [(43, 120, 227), (245, 84, 66), (66, 245, 78)],
        [(43, 120, 227), (66, 245, 78), (66, 245, 78)],
        [(43, 120, 227), (245, 84, 66), (66, 245, 78)],
      ]


a_3 = [
        [(4, 2, 1), (4, 4, 4), (4, 4, 4)],
        [(4, 4, 1), (4, 4, 2), (4, 4, 4)],
        [(4, 2, 1), (4, 4, 4), (4, 4, 4)]
      ]


a_4 = [
        [(4, 2, 1), (4, 4, 4), (4, 4, 4)],
        [(4, 4, 1), (4, 4, 2), (4, 4, 4)],
        [(4, 2, 1), (4, 4, 4), (4, 4, 5)]
      ]



a_5 = []
a_5.extend(a_1)
a_5.extend(a_1)

t_a3 = []
#pprint.pprint(a_5)
for map in a_5:
    (r1, r2, r3) = map
    t_a3.append((r1, r2, r3))

pprint.pprint(t_a3)


#pprint.pprint(len(a_5))
pprint.pprint(list(set(t_a3)))
a_2 = [[[43, 120, 227], [66, 245, 78], [66, 245, 78]], [[43, 120, 227], [245, 84, 66], [43, 120, 227]], [[43, 120, 227], [43, 120, 227], [43, 120, 227]]]

# use the created array to output your multiple images. In this case I have stacked 4 images vertically
dd = set(t_a3)
pprint.pprint(a_3)
ax[0].imshow(list(set(t_a3)))
#ax[1].imshow(a_2)

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