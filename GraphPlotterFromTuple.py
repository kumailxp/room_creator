from Coordinate import *
from Utils import *
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import math

class GraphPlotterFromTuple:
    def __init__(self, final_layout) -> None:
        self.final_layout = final_layout

    def get_subplot_layout(self):
        array_len = len(self.final_layout)
        rows = int(math.sqrt(array_len))
        extra_col = 0 if array_len%rows  == 0 else 1
        cols = extra_col + int(array_len/rows)
        return rows, cols

    def plot(self):
        sub_layout = self.get_subplot_layout()
        subplot_row, subplot_col = sub_layout
        fig, ax = plt.subplots(subplot_col, subplot_row, picker=True)
        fig.suptitle(f"Rooms plots")

        id = 0

        final_layout_len = len(self.final_layout)
        for c in range(0, subplot_col):
            for r in range(0, subplot_row):
                if id > final_layout_len - 1:
                    ax[c][r].imshow(self.get_empty_block())
                else:
                    #print(self.room_rgb_layout[id])
                    ax[c][r].imshow(self.get_rgb_array(id))
                ax[c][r].set_axis_off()
                id += 1
        plt.axis('off')

    def show(self):
        plt.show()

    def get_rgb_array(self, id):
        result = []
        room = self.final_layout[id]
        for byte in room:
            result.append([converter_dictionary[r] for r in byte]) 
        return result

    def get_empty_block(self):
        result = []
        room_template = self.final_layout[0]
        for byte in room_template:
             result.append([RGB.White for _ in byte]) 
        return result
