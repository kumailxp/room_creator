#!/bin/python
from concurrent.futures import ThreadPoolExecutor
from RoomMaker import *
from GraphPlotterFromTuple import *
from Rooms.Room import *
from LayoutCreator import *


def main():
    room = Room(3, 3, (1, 2))
    source_nodes = room.get_source_nodes()

    all_room_layouts: Dict[int, Room] = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        for source_node in source_nodes:
            rm = RoomMaker(room, source_node)
            future = executor.submit(rm.get_paths_from_source, source_node)
            all_room_layouts[source_node] = future

        for source_node, future in all_room_layouts.items():
            r = future.result()
            all_room_layouts[source_node] = r
            print(f"layout for {source_node}: {len(r)}")

    unique_layouts = LayoutCreator(all_room_layouts).get()
    print(f"Unique number of layouts: {len(unique_layouts)}")

    G = GraphPlotterFromTuple(unique_layouts)
    G.plot()
    G.show()

    # for source_node in source_nodes:
    #     GraphPlotter(all_room_layouts[source_node], room_map, source_node).plot()
    # plt.show()


if __name__ == "__main__":
    main()
