import math
import matplotlib
import matplotlib.pyplot as plt
from Utils import *
from Rooms.Room import *

matplotlib.use('TkAgg')


class GraphPlotter:

    def __init__(self, room_layout, room_map: Room, source_node):
        self.room_rgb_layout = [self.get_rgb_array(b) for b in room_layout]
        self.room_map = room_map
        self.source_node = source_node

    def plot(self):
        sub_layout = self.get_subplot_layout()
        subplot_row, subplot_col = sub_layout
        fig, ax = plt.subplots(subplot_col, subplot_row, picker=True)
        fig.suptitle(
            f"Rooms for plotting from source node: {self.source_node}, core block: {self.room_map.core_block}")

        id = 0

        room_rgb_layout_len = len(self.room_rgb_layout)
        for c in range(0, subplot_col):
            for r in range(0, subplot_row):
                if id > room_rgb_layout_len - 1:
                    ax[c][r].imshow(self.get_empty_rgb())
                else:
                    ax[c][r].imshow(self.room_rgb_layout[id])
                ax[c][r].set_axis_off()
                id += 1
        plt.axis('off')

    def show(self):
        plt.show()

    def get_subplot_layout(self):
        array_len = len(self.room_rgb_layout)
        rows = int(math.sqrt(array_len))
        extra_col = 0 if array_len % rows == 0 else 1
        cols = extra_col + int(array_len/rows)
        return rows, cols

    def get_rgb_array(self, single_room_layout: Room):
        rgb_array = single_room_layout.coordinate_map
        for _, coordinate in single_room_layout.node_map.items():
            x, y = coordinate
            rgb_array[x][y] = converter_dictionary[single_room_layout.coordinate_map[x][y]]
        return rgb_array

    def get_empty_rgb(self):
        rgb_array = self.room_map.coordinate_map
        for _, coordinate in self.room_map.node_map.items():
            x, y = coordinate
            rgb_array[x][y] = RGB.White
        return rgb_array
