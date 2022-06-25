import networkx
from typing import Tuple
from Rooms.RoomMatrix import *

class RoomGraph:

    def __init__(self, room_matrix: RoomMatrix) -> None:
        self.room_matrix = room_matrix
        self.graph = self.get()

    def is_left_block(self, x):
        block_x = x - 1
        return not (block_x < 0)

    def is_right_block(self, x):
        block_x = x + 1
        return block_x < (self.room_matrix.get_num_rows())

    def is_down_block(self, y):
        block_y = y - 1
        return not (block_y < 0)

    def is_up_block(self, y):
        block_y = y + 1
        return block_y < (self.room_matrix.get_num_cols())

    def get_connected_edges(self):
        paths = []

        def is_in_path_list(p_to):
            for pfrom, _ in paths:
                if pfrom == p_to:
                    return True
            return False

        for y in range(0, self.room_matrix.get_num_cols()):
            for x in range(0, self.room_matrix.get_num_rows()):
                if self.is_left_block(x):
                    p_to = (x-1, y)
                    if not is_in_path_list(p_to):
                        paths.append(((x, y), p_to))
                if self.is_right_block(x):
                    p_to = (x+1, y)
                    if not is_in_path_list(p_to):
                        paths.append(((x, y), p_to))
                if self.is_up_block(y):
                    p_to = (x, y+1)
                    if not is_in_path_list(p_to):
                        paths.append(((x, y), p_to))
                if self.is_down_block(y):
                    p_to = (x, y-1)
                    if not is_in_path_list(p_to):
                        paths.append(((x, y), p_to))
        return paths

    def get_edges_as_nodes(self):
        paths = self.get_connected_edges()
        path_as_nodes = []
        for p_from, p_to in paths:
            p_fx, p_fy = p_from
            p_tx, p_ty = p_to
            node_from = p_fx + (p_fy * self.room_matrix.get_num_rows())
            node_to = p_tx + (p_ty * self.room_matrix.get_num_rows())
            path_as_nodes.append((node_from, node_to))
        return path_as_nodes

    def get(self) -> networkx.Graph:
        G = networkx.Graph()
        G.add_edges_from(self.get_edges_as_nodes())
        return G

    def get_connected_edges_to_node(self, edge: Tuple):
        return list(self.graph[edge].keys())
