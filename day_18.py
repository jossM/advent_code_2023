from dataclasses import dataclass
from enum import Enum

raw_instructions = """""".strip()
part_1 = True


class Direction(Enum):
    right = "R"
    down = "D"
    left = "L"
    up = "U"


part2_code_to_dir = {
    0: Direction.right,
    1: Direction.down,
    2: Direction.left,
    3: Direction.up,
}


@dataclass(frozen=True)
class Location:
    x: int
    y: int


if __name__ == '__main__':
    all_instructions = map(lambda s: s.split(), raw_instructions.split("\n"))

    # Parse the instructions
    if part_1:
        all_instructions = [(Direction(raw_direction), int(path_length))for raw_direction, path_length, _ in all_instructions]
    else:
        all_instructions = [(part2_code_to_dir[int(code[-2])], int(code[2:-2], 16)) for _, __, code in all_instructions]

    # figure out the map operated on and where instructions start from
    double_area = 0
    on_edge_verticies = 0
    location = Location(0, 0)
    for direction, path_length in all_instructions:
        previous_location = location
        if direction == Direction.right:
            location = Location(x=location.x+path_length, y=location.y)
        elif direction == Direction.left:
            location = Location(x=location.x-path_length, y=location.y)
        elif direction == Direction.down:
            location = Location(x=location.x, y=location.y - path_length)
        else:  # Direction.up
            location = Location(x=location.x, y=location.y + path_length)
        on_edge_verticies += path_length
        double_area += previous_location.x * location.y - previous_location.y * location.x
    assert location == Location(0, 0), 'Failed to get back to the original point'
    area = abs(double_area) / 2  # shoelace formula
    print(f"Found area of {area} with {on_edge_verticies} outside vertices")
    inside_dots = area + 1 - on_edge_verticies/2  # Pick theorem
    print(f'Found {inside_dots} inside')
    print(f"Total area = {int(inside_dots + on_edge_verticies)}")
