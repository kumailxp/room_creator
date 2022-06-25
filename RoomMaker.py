from typing import List
import networkx
import math
from Rooms.Room import *
from Utils import *


class RoomMaker:

    def __init__(self, room: Room, source_node: int) -> None:
        self.room = room
        self.room_graph = room.get_graph()
        self.core_node = room.get_core_node()
        self.source_node = source_node

    def create_other_area(self, custom_area):
        return list(set(self.room.get_all_nodes()) - set(custom_area) - {self.core_node})

    def area_has_outer_node(self, custom_area):
        found_outer_node = False
        outer_nodes = self.room.get_room_outer_nodes()
        for node in custom_area:
            if node in outer_nodes:
                found_outer_node = True
                break
        return found_outer_node

    def do_blocks_meet_criteria(self, custom_area):
        room_b_graph: networkx.Graph = self.room_graph.subgraph(custom_area)

        if not networkx.is_connected(room_b_graph):
            return False

        if not self.area_has_outer_node(custom_area):
            return False
        return True

    def get_room_plan(self, area_for_room_a):

        if not self.area_has_outer_node(area_for_room_a):
            return []

        r = set(area_for_room_a).intersection(
            self.room.get_core_connected_nodes())
        if r == set(self.room.get_core_connected_nodes()):
            return []

        area_for_room_b = self.create_other_area(area_for_room_a)
        all_rooms = []

        if self.do_blocks_meet_criteria(area_for_room_b):
            room_plan = self.create_room(area_for_room_a, area_for_room_b)
            all_rooms.append(room_plan)

        return all_rooms

    def create_room(self, custom_area_1, custom_area_2):
        new_room: Room = self.room.create_empty_room()
        new_room.fill_in_room({BlockType.Green: custom_area_1},
                              {BlockType.Blue: custom_area_2})
        return new_room

    def get_paths_from_source(self, source_node):
        cutoff = int(math.ceil((self.room.cols * self.room.rows)/2)
                     ) + abs(self.room.cols - self.room.rows)
        result = []
        for area_of_a in networkx.all_simple_paths(self.room_graph, source=source_node, target=self.core_node, cutoff=cutoff):
            current_room_plan: List[Room] = self.get_room_plan(area_of_a)
            for cp in current_room_plan:
                if not cp in result:
                    result.append(cp)
        return result
