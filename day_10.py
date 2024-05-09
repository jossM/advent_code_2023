from dataclasses import dataclass, asdict

pipe_map = list(filter(bool, """""".split("\n")))
part_1 = True


@dataclass(frozen=True)
class Connection:
    up: bool = False
    right: bool = False
    down: bool = False
    left: bool = False


symbol_connections = {
    "|": Connection(up=True, down=True),
    "-": Connection(left=True, right=True),
    "L": Connection(up=True, right=True),
    "J": Connection(up=True, left=True),
    "7": Connection(down=True, left=True),
    "F": Connection(down=True, right=True),
    ".": Connection(),
    "S": Connection(up=True, down=True, right=True, left=True),
}

starting_locations = {(line_index, line.index("S")) for line_index, line in enumerate(pipe_map) if "S" in line}
distance_from_start = [[None] * len(line) for line in pipe_map]
for x, y in starting_locations:
    distance_from_start[x][y] = 0

main_tiles_connections = [[Connection()] * len(line) for line in pipe_map]

all_search_locations = set(starting_locations)
while all_search_locations:
    next_all_search_locations = set()

    for x, y in all_search_locations:
        connected_locations = []
        location_connections = symbol_connections[pipe_map[x][y]]
        local_connections = dict()
        if location_connections.up and x > 0:
            if symbol_connections[pipe_map[x - 1][y]].down:
                connected_locations.append((x - 1, y))
                local_connections['up'] = True
        if location_connections.down and x + 1 < len(pipe_map):
            if symbol_connections[pipe_map[x + 1][y]].up:
                connected_locations.append((x + 1, y))
                local_connections['down'] = True
        if location_connections.right and y + 1 < len(pipe_map[x]):
            if symbol_connections[pipe_map[x][y + 1]].left:
                connected_locations.append((x, y + 1))
                local_connections['right'] = True
        if location_connections.left and y > 0:
            if symbol_connections[pipe_map[x][y - 1]].right:
                connected_locations.append((x, y - 1))
                local_connections['left'] = True
        main_tiles_connections[x][y] = Connection(**local_connections)

        for con_x, con_y in connected_locations:
            if distance_from_start[con_x][con_y] is None or distance_from_start[con_x][con_y] > distance_from_start[x][
                y] + 1:
                distance_from_start[con_x][con_y] = distance_from_start[x][y] + 1
                next_all_search_locations.add((con_x, con_y))

    all_search_locations = next_all_search_locations
if part_1:
    print(max([dist for line in distance_from_start for dist in line if dist is not None]))
else:
    # to analyse things easily let us imagine an interlocked tiles in between the intersections of each point.
    # in the figure below + is the original points and x the interlocked ones :
    # index interlocked 0 : x   x   x
    # index main 0        :   +   +
    # index interlocked 1 : x   x   x
    # index main 1        :   +   +
    external_interlocked_tiles = (
            {(0, i) for i in range(len(pipe_map) + 1)}
            | {(len(pipe_map), i) for i in range(len(pipe_map) + 1)}
            | {(i, 0) for i in range(len(pipe_map[0]) + 1)}
            | {(i, len(pipe_map[0])) for i in range(len(pipe_map[0]) + 1)}
    )
    previous_additional_tiles = set(external_interlocked_tiles)
    while previous_additional_tiles:
        new_external_interlocked_tiles = set()
        for x, y in previous_additional_tiles:
            # up left
            if 0 < x and 0 < y:
                up_left = main_tiles_connections[x - 1][y - 1]
                if not up_left.down:
                    new_external_interlocked_tiles.add((x, y - 1))
                if not up_left.right:
                    new_external_interlocked_tiles.add((x - 1, y))
            elif 0 < x:
                up_right = main_tiles_connections[x - 1][y]
                if not up_right.left:
                    new_external_interlocked_tiles.add((x - 1, y))
            elif 0 < y:
                down_left = main_tiles_connections[x][y - 1]
                if not down_left.up:
                    new_external_interlocked_tiles.add((x, y - 1))
            # down right
            if x < len(main_tiles_connections) and y < len(main_tiles_connections[x]):
                down_right = main_tiles_connections[x][y]
                if not down_right.up:
                    new_external_interlocked_tiles.add((x, y + 1))
                if not down_right.left:
                    new_external_interlocked_tiles.add((x + 1, y))
            elif x < len(main_tiles_connections):
                down_left = main_tiles_connections[x][y - 1]
                if not down_left.right:
                    new_external_interlocked_tiles.add((x + 1, y))
            elif y < len(main_tiles_connections[0]):
                up_right = main_tiles_connections[x - 1][y]
                if not up_right.down:
                    new_external_interlocked_tiles.add((x, y + 1))
        new_external_interlocked_tiles -= external_interlocked_tiles
        previous_additional_tiles = new_external_interlocked_tiles - external_interlocked_tiles
        external_interlocked_tiles |= new_external_interlocked_tiles

    belonging_tiles_count = sum(
        int(not len(external_interlocked_tiles.intersection([(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)])))
        for x, line in enumerate(pipe_map) for y, char in enumerate(line)
    )
    print(f"tiles in the loop {belonging_tiles_count}")
    # useless bit of code but displays pretty map
    main_tiles_belonging = []
    for x, line in enumerate(pipe_map):
        belonging_line = ""
        for y, char in enumerate(line):
            local_external_interlocked_tiles = external_interlocked_tiles.intersection(
                [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)])
            if len(local_external_interlocked_tiles) == 0:
                belonging_line += "*"

            elif len(local_external_interlocked_tiles) == 4:
                belonging_line += "O"
            else:
                belonging_line += char

        main_tiles_belonging.append(belonging_line)

    print("\n".join(main_tiles_belonging))
