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
        BlockType.Core : RGB.Red,
        BlockType.Green : RGB.Green,
        BlockType.Blue : RGB.Blue,
        BlockType.Empty : RGB.White,
        BlockType.Yellow : RGB.Yellow,
        BlockType.Gray : RGB.Gray
}
