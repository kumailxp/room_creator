#!/bin/python
from typing import List
import networkx
import math
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed

from GraphPlotterFromTuple import *
from Coordinate import *

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


def get_paths_from_source(source_node, room_map, room_graph, all_nodes, core_connected_blocks):
    cutoff = int(math.ceil((room_map.cols*room_map.rows)/2))
    result = []
    for path in networkx.all_simple_paths(room_graph, source=source_node, target=room_map.core_block_node, cutoff=cutoff):
        current_room_plan: List[Coordinate] = get_room_plan(all_nodes, core_connected_blocks, room_map, path, -1)
        if len(current_room_plan) != 0:
                for cp in current_room_plan:
                    if not cp in result:
                        result.append(cp)
    return result


def main():
    room_map = Coordinate(5,5, (1,1))
    room_graph: networkx.Graph = room_map.convert_to_graph()
    all_nodes = room_graph.nodes()
    core_connected_blocks = room_graph[room_map.core_block_node]
    print("core_connected_blocks", list(core_connected_blocks.keys()))
    #print(room_map.node_map)

    all_room_layouts = {}
    source_nodes = list(all_nodes.keys())
    for b in core_connected_blocks:
        source_nodes.remove(b)
    source_nodes.remove(room_map.core_block_node)
    print("s:", source_nodes)
    num_threads = len(source_nodes)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for source_node in source_nodes:
            future = executor.submit(get_paths_from_source, source_node, room_map, room_graph, all_nodes, core_connected_blocks)
            all_room_layouts[source_node] = future

        for source_node, future in all_room_layouts.items():
            r = future.result()
            all_room_layouts[source_node] = r
            print(f"layout for {source_node}: {len(r)}")

    result = []
    for _, rooms in all_room_layouts.items():
        for room in rooms:
            room:Coordinate
            result.append(room.get_data_as_tuple(room.rows, room.get_coordinate_map_as_tuple()))

    result_without_dups = list(OrderedDict.fromkeys(result))
    print(f"Unique number of layouts: {len(result_without_dups)}")
    G = GraphPlotterFromTuple(result_without_dups)
    G.plot()
    G.show()

    # for source_node in source_nodes:
    #     GraphPlotter(all_room_layouts[source_node], room_map, source_node).plot()
    # plt.show()


if __name__ == "__main__":
    main()