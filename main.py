#!/bin/python


from queue import Empty


class Color:
    R = '\033[91m'
    G = '\033[92m'
    B = '\033[94m'
    W = '\u001b[37m'


class BoxInfo:
    Occupied = 0
    Empty = 1


class RoomPartitioner:
    def __init__(self, box_array, box_info = []) -> None:
        self.box_array = box_array
        self.box_info = box_info

    def __str__(self) -> str:
        r = ""
        for row in self.box_array:
            for b in row:
                r = r + b + "X" if b != 0 else r + Color.W + "X"
            r = r + "\n"
        return r


class RoomGenerator:
    all_rooms = []
    x = 0
    y = 0
    def __init__(self, width, height, core_block = ()) -> None:
        box_array = []
        box_info = []
        self.height = height
        self.width = width
        for _ in range(0,height):
            box_array.append([0] * width)
            box_info.append([BoxInfo.Empty] * width)
        
        self.x,self.y = core_block
        box_array[self.x][self.y] = Color.R
        box_info[self.x][self.y] = Color.R 
        room_partition = RoomPartitioner(box_array, box_info)

        self.all_rooms.append(room_partition)


    def generate_partitions(self):
        origin = (self.x, self.y)
        box_array = []
        box_info = []

        for room in self.all_rooms:
            box_array = room.box_array
            box_info = room.box_info

        current_block_x, current_block_y = (self.x,self.y)
        print("starting: ", current_block_x, current_block_y)
        end_loop = False
        while(end_loop == False):
            if current_block_x > 0 and box_info[current_block_x - 1][current_block_y] == BoxInfo.Empty:
                current_block_x = current_block_x - 1
                box_array[current_block_y][current_block_x] = Color.G
                box_info[current_block_y][current_block_x] = BoxInfo.Occupied
                print(current_block_x, current_block_y)
                room_partition = RoomPartitioner(box_array, box_info)
                self.all_rooms.append(room_partition)
                return
            elif current_block_x == 0 and current_block_y > 0 and box_info[current_block_x][current_block_y - 1] == BoxInfo.Empty:
                current_block_y = current_block_y - 1
                box_array[current_block_y][current_block_x] = Color.G
                box_info[current_block_y][current_block_x] = BoxInfo.Occupied
            elif current_block_x == 0 and current_block_y == 0:
                end_loop = True
            
            print(current_block_x, current_block_y)
            room_partition = RoomPartitioner(box_array, box_info)
            self.all_rooms.append(room_partition)
    







rg = RoomGenerator(3,3, (1,2))
rg.generate_partitions()
for room in rg.all_rooms:
    print(room)

# rm = RoomPartitioner( 
#                       [ 
#                         [0,0,0],
#                         [0,0,0],
#                         [0,0,0],
#                       ],
#                       [ 
#                         [Color.R,0,0],
#                         [0,Color.G,0],
#                         [0,Color.R,0],
#                       ],

#                     )

# print(rm)