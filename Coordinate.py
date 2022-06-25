from Utils import *
from colored import fg, bg, attr
import networkx
import pprint


class Coordinate:

    def __init__(self, rows, cols, core_block):
        self.coordinate_map = [ [BlockType.Empty] * rows for _ in range(0, cols)]
        cb_x, cb_y = core_block
        self.core_block = core_block
        self.core_block_node = cb_x + (rows * cb_y)
        self.rows = rows
        self.cols = cols
        self.node_map = {}

        for y in range(0, cols):
            for x in range(0, rows):
                self.node_map[x + (rows * y)] = (x,y)


    def __eq__(self, __o):
        return self.coordinate_map == __o.coordinate_map


    @staticmethod
    def get_data_as_tuple(num_rows, row_data):
        if num_rows == 2:
            (r1, r2) = row_data
            return (r1, r2)
        elif num_rows == 3:
            (r1, r2, r3) = row_data
            return (r1, r2, r3)
        elif num_rows == 4:
            (r1, r2, r3, r4) = row_data
            return (r1, r2, r3, r4)
        elif num_rows == 5:
            (r1, r2, r3, r4, r5) = row_data
            return (r1, r2, r3, r4, r5) 
        elif num_rows == 6:
            (r1, r2, r3, r4, r5, r6) = row_data
            return (r1, r2, r3, r4, r5, r6)
        else:
            raise ValueError(f"upsupport rows. rows should be less than 7")


    def get_coordinate_map_as_tuple(self):
        result = []
        for row_data in self.coordinate_map:
            result.append(self.get_data_as_tuple(self.rows, row_data))

        return result

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

        for y in range(0,self.get_num_cols()):
            for x in range(0, self.get_num_rows()):
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
            node_from = p_fx + (p_fy * self.get_num_rows())
            node_to = p_tx + (p_ty * self.get_num_rows())
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
