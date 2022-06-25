from os import remove
import networkx
from Utils import *
from .RoomMatrix import *
from .RoomNodes import *
from .RoomGraph import *


class Room:
    def __init__(self, width, height, core_block_coordinate):
        self.core_block_coordinate = core_block_coordinate
        self.room_matrix = RoomMatrix(width, height)
        self.room_graph = RoomGraph(self.room_matrix)
        self.room_nodes = RoomNodes(self.room_matrix)
        self.rows: int = width
        self.cols: int = height

    def __str__(self) -> str:
        return self.room_matrix

    def get_graph(self) -> networkx.Graph:
        return self.room_graph.get()

    def get_core_node(self) -> int:
        return self.room_nodes.coordinate_to_node_number(self.core_block_coordinate)

    def get_core_connected_nodes(self) -> int:
        return self.room_graph.get_connected_edges_to_node(self.get_core_node())

    def get_all_nodes(self) -> Dict:
        return self.room_nodes.get_all_nodes()

    def get_source_nodes(self) -> List:
        source_nodes = self.get_all_nodes()
        source_nodes.remove(self.get_core_node())
        return source_nodes

    def get_room_outer_nodes(self):
        outer_nodes = []
        for s in self.room_nodes:
            nodes = self.room_graph.get_connected_edges_to_node(s)
            if len(nodes) < 4:
                outer_nodes.append(s)
        core_node = self.get_core_node()
        if core_node in outer_nodes:
            outer_nodes.remove(core_node)
        return outer_nodes

    def create_empty_room(self):
        return Room(self.rows, self.cols, self.core_block_coordinate)

    def fill_in_room(self, *kwargs):
        for area_info in kwargs:
            for colour, area in area_info.items():
                for node in area:
                    x, y = self.room_nodes.node_number_to_edge(node)
                    self.room_matrix.set_value(x, y, colour)

        x, y = self.core_block_coordinate
        self.room_matrix.set_value(x, y, BlockType.Core)
