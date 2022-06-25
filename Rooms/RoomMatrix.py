from Utils import *
from colored import fg, bg, attr

class RoomMatrix:

    def __init__(self, rows, cols):
        self.coordinate_map = [[BlockType.Empty]
                               * rows for _ in range(0, cols)]
        self.rows = rows
        self.cols = cols

    def __eq__(self, __o):
        return self.coordinate_map == __o.coordinate_map

    def get_coordinate_map_as_tuple(self):
        result = []
        for row_data in self.coordinate_map:
            result.append(list_to_tuple(self.rows, row_data))
        return result

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
                        print(
                            f"{func.__name__}: Error::Coordinate out of range. Aborting.")
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

    def __str__(self) -> str:
        r = ""
        i = 0
        for row in self.coordinate_map:
            for b in row:
                r += f"{fg(b)}{bg(b)}.{attr(0)}"
                i += 1
            r += "\n"
        return r