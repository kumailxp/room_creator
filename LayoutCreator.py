from collections import OrderedDict
from typing import Dict
from Rooms.Room import *


class LayoutCreator:
    def __init__(self, all_room_layouts: Dict[int, Room]) -> None:
        self.all_room_layouts = all_room_layouts
        self.unique_layouts = self.create_unique_layouts()

    def create_unique_layouts(self):
        result = []
        for _, rooms in self.all_room_layouts.items():
            for room in rooms:
                room: Room
                result.append(list_to_tuple(
                    room.cols, room.room_matrix.get_coordinate_map_as_tuple()))
        return list(OrderedDict.fromkeys(result))

    def get(self):
        return self.unique_layouts
