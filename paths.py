#!/bin/python
from audioop import tomono
import networkx
import matplotlib.pyplot as plt
import math
from colored import fg, bg, attr

class BlockType:
    Core = 1
    Green = 2
    Blue = 4
    Empty = 15


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

    class BlockTypes:
        outside_map = (-1,-1)
        inside_map = 1


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


def print_layouts(layout):
    cols = int(math.ceil(len(layout)/3))
    rows = 3
    print(len(layout))
    for room in layout:
        print(room)
    # for i in range(0, 3):
    #     room_0 = layout[i]
    #     room_1 = layout[i+1]
    #     room_2 = layout[i+2]

    #     for col in range(0, 3):
    #         print(f"{room_0.get_row_info_as_color(col)}*{room_1.get_row_info_as_color(col)}*{room_2.get_row_info_as_color(col)}", end='')
        
    #     print("\n")

def main():
    room_map = Coordinate(3,3, (1,2))
    # print(room_map.set_value(1, 0, BlockType.Core))
    # print(room_map)

    room_graph: networkx.Graph = room_map.convert_to_graph()
    # print(room_graph.size())
    all_nodes = room_graph.nodes()
    core_connected_blocks = room_graph[room_map.core_block_node]
    print("core_connected_blocks", list(core_connected_blocks.keys()))
    # networkx.draw_networkx(room_graph, with_labels=True)
    # plt.show()
    print(room_map.node_map)
    #print(list(networkx.bfs_tree(room_graph, 5).edges()))
    all_layouts = []
    tmp_b_rooms = []
    new_room = Coordinate(room_map.rows, room_map.cols, room_map.core_block)
    new_room_graph: networkx.Graph = room_map.convert_to_graph()
    for path in networkx.all_simple_paths(room_graph, source=0, target=room_map.core_block_node):
        new_room.clean_map()
        area_for_room_a = path
        area_for_room_b = list(set(all_nodes) - set(area_for_room_a))
        if room_map.core_block_node in area_for_room_b:
            area_for_room_b.remove(room_map.core_block_node)
        room_b_graph: networkx.Graph =new_room_graph.subgraph(area_for_room_b)
        # room_b_graph.add_node(room_map.core_block_node)
        #room_a_graph: networkx.Graph =new_room_graph.subgraph(area_for_room_a)
        r = set(area_for_room_b).intersection(set(core_connected_blocks.keys()))
        if len(r) == 0:
            continue

        if not networkx.is_connected(room_b_graph):
            continue


        room_b_is_there = False
        for x in tmp_b_rooms:
            #print("x ", x, " area_for_room_b ", area_for_room_b)
            if area_for_room_b == x:
                room_b_is_there = True
                break
        if room_b_is_there:
            continue
        print("A:", area_for_room_a, " B: ", area_for_room_b)
        tmp_b_rooms.append(area_for_room_b)
       
        #print(networkx.is_connected(room_a_graph))
        for node in area_for_room_a:
            x, y = new_room.node_map[node]
            new_room.set_value(x, y, BlockType.Green)
        for node in area_for_room_b:
            x, y = new_room.node_map[node]
            new_room.set_value(x, y, BlockType.Blue)
        
        x, y = new_room.node_map[area_for_room_a[-1]]
        new_room.set_value(x, y, BlockType.Core)
        all_layouts.append(new_room)
        print(new_room)

    print("num layouts", len(all_layouts))
    #print_layouts(all_layouts)
    #print(room_graph[1])


if __name__ == "__main__":
    main()
