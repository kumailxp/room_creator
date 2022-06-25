from typing import Dict, List, Tuple
from Rooms.RoomMatrix import *

class RoomNodes:
    def __init__(self, room_matrix: RoomMatrix) -> None:
        self.room_matrix = room_matrix
        self.node_map = self.generate_node_map()

    def generate_node_map(self) -> Dict:
        result = {}
        for y in range(0,  self.room_matrix.cols):
            for x in range(0,  self.room_matrix.rows):
                result[x + (self.room_matrix.rows * y)] = (x, y)
        return result

    def coordinate_to_node_number(self, coordinate: Tuple):
        x, y = coordinate
        return x + (self.room_matrix.get_num_rows() * y)

    def node_number_to_edge(self, node: int) -> Tuple:
        return self.node_map[node]

    def get(self) -> Dict:
        return self.node_map

    def get_all_nodes(self) -> List:
        return list(self.node_map.keys())

    def __iter__(self):
        return iter(self.get_all_nodes())