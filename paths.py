#!/bin/python
import time
from typing import List
import networkx
import matplotlib
import matplotlib.pyplot as plt
import math
from colored import fg, bg, attr
from numpy import array, block

matplotlib.use('TkAgg')

class BlockType:
    Core = 1
    Green = 2
    Blue = 4
    Empty = 15
    Yellow = 3
    Gray = 8

class RGB:
    Red = [245, 84, 66]
    Green = [66, 245, 78]
    Blue = [43, 120, 227]
    White = [255, 255, 255]
    Yellow = [245, 237, 12]
    Gray = [112, 112, 109]


class Coordinate:

    def __init__(self, rows, cols, core_block):
        self.coordinate_map = [ [BlockType.Empty] * rows for _ in range(0, cols)]
        cb_x, cb_y = core_block
        self.core_block = core_block
        self.core_block_node = cb_x + (cols * cb_y)
        self.rows = rows
        self.cols = cols
        self.node_map = {}
        i = 0
        for x in range(0, rows):
            for y in range(0, cols):
                self.node_map[x + (cols * y)] = (x,y)
                i += 1

    def get_rgb_array(self):
        rgb_array = self.coordinate_map
        color = RGB.White
        for _,coordinate in self.node_map.items():
            x, y = coordinate
            if self.coordinate_map[x][y] == BlockType.Core:
                color = RGB.Red
            elif self.coordinate_map[x][y] == BlockType.Green:
                color = RGB.Green
            elif self.coordinate_map[x][y] == BlockType.Blue:
                color = RGB.Blue
            elif self.coordinate_map[x][y] == BlockType.Empty:
                color = RGB.White
            elif self.coordinate_map[x][y] == BlockType.Yellow:
                color = RGB.Yellow
            elif self.coordinate_map[x][y] == BlockType.Gray:
                color = RGB.Gray
            rgb_array[x][y] = color
        return rgb_array


    def get_empty_rgb(self):
        rgb_array = self.coordinate_map
        for _,coordinate in self.node_map.items():
            x, y = coordinate
            rgb_array[x][y] = RGB.White
        return rgb_array

    def clean_map(self):
        self.coordinate_map = [ [BlockType.Empty] * self.get_num_rows() for i in range(0, self.get_num_cols())]

    def get_num_rows(self):
        return len(self.coordinate_map[0])

    def get_num_cols(self):
        return len(self.coordinate_map)

    def exception_handler(print_exception=False):
        def decorator(func):
            def inner_function(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except IndexError:
                    if print_exception:
                        print(f"{func.__name__}: Error::Coordinate out of range. Aborting.")
                except ValueError as e:
                    if print_exception:
                        print(f"{func.__name__}: Error::{str(e)}. Aborting.")
            return inner_function
        return decorator

    @exception_handler(print_exception=True)
    def set_value(self, x, y, value):
        cartesian_y = self.get_num_cols() - 1 - y
        if cartesian_y < 0:
            raise ValueError("y is outside range")
        self.coordinate_map[cartesian_y][x] = value

    @exception_handler(print_exception=True)
    def get_value(self, x, y):
        cartesian_y = self.get_num_cols() - 1 - y
        return self.coordinate_map[cartesian_y][x]

    def get_row_info(self, col):
        return self.coordinate_map[col]

    def get_row_info_as_color(self, col):
        r = ""
        for b in self.coordinate_map[col]:
            r += f"{fg(b)}{bg(b)} {attr(0)}"
        return r

    def is_left_block(self, x):
        block_x = x - 1
        return not (block_x < 0)

    def is_right_block(self, x):
        block_x = x + 1
        return block_x < (self.get_num_rows())

    def is_down_block(self, y):
        block_y = y - 1
        return not (block_y < 0)

    def is_up_block(self, y):
        block_y = y + 1
        return block_y < (self.get_num_cols())

    def get_connected_edges(self):
        paths = []

        def is_in_path_list(p_to):
            for pfrom, _ in paths:
                if pfrom == p_to:
                    return True
            return False

        for x in range(0,self.get_num_rows()):
            for y in range(0, self.get_num_cols()):
                if self.is_left_block(x):
                    p_to = (x-1, y)
                    if not is_in_path_list(p_to):
                        paths.append(((x,y), p_to))
                if self.is_right_block(x):
                    p_to = (x+1, y)
                    if not is_in_path_list(p_to):
                        paths.append(((x,y),p_to))
                if self.is_up_block(y):
                    p_to = (x, y+1)
                    if not is_in_path_list(p_to):
                        paths.append(((x,y),p_to))
                if self.is_down_block(y):
                    p_to = (x, y-1)
                    if not is_in_path_list(p_to):
                        paths.append(((x,y), p_to))

        return paths


    def get_edges_as_nodes(self):
        paths = self.get_connected_edges()
        path_as_nodes = []
        for p_from, p_to in paths:
            p_fx, p_fy = p_from
            p_tx, p_ty = p_to
            node_from = p_fx + (p_fy * self.get_num_cols())
            node_to = p_tx + (p_ty * self.get_num_cols())
            path_as_nodes.append( (node_from, node_to))
        return path_as_nodes


    def convert_to_graph(self) -> networkx.Graph:
        G : networkx.Graph = networkx.Graph()
        G.add_edges_from(self.get_edges_as_nodes())
        return G

    def __str__(self) -> str:
        r = ""
        i = 0
        for row in self.coordinate_map:
            for b in row:
                r += f"{fg(b)}{bg(b)}.{attr(0)}"
                i += 1
            r += "\n"
        
        return r


def get_inner_paths(path_list):
    r = []
    for i in range(1, len(path_list)-1):
        r.append(path_list[i:])
    return r


def create_other_area(all_nodes, room_map, area_for_room_a):
    area_for_room_b = list(set(all_nodes) - set(area_for_room_a))
    if room_map.core_block_node in area_for_room_b:
        area_for_room_b.remove(room_map.core_block_node)
    return area_for_room_b


def create_inner_rooms(all_nodes, room_map, core_connected_blocks, area_for_room_a, source_node):
    room_map_graph: networkx.Graph = room_map.convert_to_graph()
    inner_paths = get_inner_paths(area_for_room_a)
    all_inner_rooms = []
    for p in inner_paths:
        area_of_inner_room = create_other_area(all_nodes, room_map, p)
        if do_blocks_meet_criteria(room_map_graph, area_of_inner_room, core_connected_blocks):
            room_plan = create_room(all_nodes, room_map, p, area_of_inner_room, source_node)
            all_inner_rooms.append(room_plan)

    return all_inner_rooms


def create_room(all_nodes, room_map, area_for_room_a, area_for_room_b, source_node = -1):
    #print("A:", area_for_room_a, " B: ", area_for_room_b)
    new_room = Coordinate(room_map.rows, room_map.cols, room_map.core_block)

    for node in area_for_room_a:
        x, y = new_room.node_map[node]
        new_room.set_value(x, y, BlockType.Green)
    for node in area_for_room_b:
        x, y = new_room.node_map[node]
        new_room.set_value(x, y, BlockType.Blue)

    x, y = new_room.node_map[area_for_room_a[-1]]
    new_room.set_value(x, y, BlockType.Core)

    if source_node != -1:
        sx, sy = new_room.node_map[source_node]
        new_room.set_value(sx, sy, BlockType.Yellow)

    return new_room


def do_blocks_meet_criteria(room_map_graph, area_for_room_b, core_connected_blocks):
    room_b_graph: networkx.Graph =room_map_graph.subgraph(area_for_room_b)

    r = set(area_for_room_b).intersection(set(core_connected_blocks.keys()))
    if len(r) == 0:
        return False

    if not networkx.is_connected(room_b_graph):
        return False

    return True


def get_room_plan(all_nodes, core_connected_blocks, room_map, area_for_room_a, source_node):
    room_map_graph: networkx.Graph = room_map.convert_to_graph()
    area_for_room_b = create_other_area(all_nodes, room_map, area_for_room_a)

    all_rooms = []
    if do_blocks_meet_criteria(room_map_graph, area_for_room_b, core_connected_blocks):
        room_plan = create_room(all_nodes, room_map, area_for_room_a, area_for_room_b, source_node)
        all_rooms.append(room_plan)

    inner_rooms = create_inner_rooms(all_nodes, room_map, core_connected_blocks, area_for_room_a, source_node)
    for r in inner_rooms:
        all_rooms.append(r)

    return all_rooms


def get_subplot_layout(all_rgb_arrays):
    array_len = len(all_rgb_arrays)
    rows = int(math.sqrt(array_len))
    extra_col = 0 if array_len%rows  == 0 else 1
    cols = extra_col + int(array_len/rows)
    return rows, cols


def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))

def enter_figure(event):
    print('enter_figure', event.canvas.figure)
    event.canvas.figure.patch.set_facecolor('red')
    event.canvas.draw()


def onpick(event):
    thisline = event.artist
    print(thisline)
    for i in thisline:
        print(i)
    #xdata = thisline.get_xdata()
    #ydata = thisline.get_ydata()
    #ind = event.ind
    #points = tuple(zip(xdata[ind], ydata[ind]))
    print('onpick points:')


def plot_on_graph(room_map: Coordinate, source_node, all_rgb_arrays):
    print("subplot layout:", get_subplot_layout(all_rgb_arrays))
    print("num layouts", len(all_rgb_arrays))
    subplot_row, subplot_col = get_subplot_layout(all_rgb_arrays)
    fig, ax = plt.subplots(subplot_col, subplot_row, picker=True)
    #fig.canvas.mpl_connect('button_press_event', onclick)
    #fig.canvas.mpl_connect('figure_enter_event', enter_figure)
    #fig.canvas.mpl_connect('pick_event', onpick)
    fig.suptitle(f"Rooms for plotting from source node: {source_node}, core block: {room_map.core_block}")

    id = 0
    rgb_array_len = len(all_rgb_arrays)
    for c in range(0, subplot_col):
        for r in range(0, subplot_row):
            if id > rgb_array_len -1:
                ax[c][r].imshow(room_map.get_empty_rgb())
            else:
                ax[c][r].imshow(all_rgb_arrays[id])
            ax[c][r].set_axis_off()
            id += 1
    plt.axis('off')


def get_paths_from_source(source_node, room_map, room_graph, all_nodes, core_connected_blocks, return_as_rgb = True):
    cutoff = int(math.ceil((room_map.cols*room_map.rows)/2))
    result = []
    for path in networkx.all_simple_paths(room_graph, source=source_node, target=room_map.core_block_node, cutoff=cutoff):
        current_room_plan: List[Coordinate] = get_room_plan(all_nodes, core_connected_blocks, room_map, path, -1)
        if len(current_room_plan) != 0:
                for cp in current_room_plan:
                    if return_as_rgb:
                        rgb_box = cp.get_rgb_array()
                        if not rgb_box in result:
                            result.append(rgb_box)
                    else:
                        if not cp in result:
                            result.append(cp)
    return result


def main():
    room_map = Coordinate(3,3, (2,2))
    room_graph: networkx.Graph = room_map.convert_to_graph()
    all_nodes = room_graph.nodes()
    core_connected_blocks = room_graph[room_map.core_block_node]
    print("core_connected_blocks", list(core_connected_blocks.keys()))
    print(room_map.node_map)

    all_rgb_arrays = []
    for source_node in [7,5]:
        rgb_array = get_paths_from_source(source_node, room_map, room_graph, all_nodes, core_connected_blocks)
        plot_on_graph(room_map, source_node, rgb_array)
        all_rgb_arrays.append(rgb_array)

    plt.show()


if __name__ == "__main__":
    main()
