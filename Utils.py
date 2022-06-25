class BlockType:
    Core = 1
    Green = 2
    Blue = 4
    Empty = 15
    Yellow = 3
    Gray = 8


class RGB:
    Red = (245, 84, 66)
    Green = (66, 245, 78)
    Blue = (43, 120, 227)
    White = (255, 255, 255)
    Yellow = (245, 237, 12)
    Gray = (112, 112, 109)


converter_dictionary = {
    BlockType.Core: RGB.Red,
    BlockType.Green: RGB.Green,
    BlockType.Blue: RGB.Blue,
    BlockType.Empty: RGB.White,
    BlockType.Yellow: RGB.Yellow,
    BlockType.Gray: RGB.Gray
}


def list_to_tuple(num_list_elements, info):
    if num_list_elements == 2:
        (r1, r2) = info
        return (r1, r2)
    elif num_list_elements == 3:
        (r1, r2, r3) = info
        return (r1, r2, r3)
    elif num_list_elements == 4:
        (r1, r2, r3, r4) = info
        return (r1, r2, r3, r4)
    elif num_list_elements == 5:
        (r1, r2, r3, r4, r5) = info
        return (r1, r2, r3, r4, r5)
    elif num_list_elements == 6:
        (r1, r2, r3, r4, r5, r6) = info
        return (r1, r2, r3, r4, r5, r6)
    elif num_list_elements == 7:
        (r1, r2, r3, r4, r5, r6, r7) = info
        return (r1, r2, r3, r4, r5, r6, r7)
    elif num_list_elements == 8:
        (r1, r2, r3, r4, r5, r6, r7, r8) = info
        return (r1, r2, r3, r4, r5, r6, r7, r8)
    elif num_list_elements == 9:
        (r1, r2, r3, r4, r5, r6, r7, r8, r9) = info
        return (r1, r2, r3, r4, r5, r6, r7, r8, r9)

    else:
        raise ValueError(f"un-supported list: list must have less than 10 elements")
