from dataclasses import dataclass, asdict

pipe_map = list(filter(bool, """""".split("\n")))


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

# part 1 only
starting_locations = {(line_index, line.index("S")) for line_index, line in enumerate(pipe_map) if "S" in line}
distance_from_start = [[None]*len(line) for line in pipe_map]
for x, y in starting_locations:
    distance_from_start[x][y] = 0

all_search_locations = set(starting_locations)
while all_search_locations:
    next_all_search_locations = set()

    for x, y in all_search_locations:
        print(f"searching connections at {(x, y)}")
        print("\n".join(map(lambda l: l[y-1:y+2], pipe_map[x-1:x+2])))
        connected_locations = []
        location_connections = symbol_connections[pipe_map[x][y]]
        if location_connections.up and x > 0:
            if symbol_connections[pipe_map[x - 1][y]].down:
                connected_locations.append((x - 1, y))
        if location_connections.down and x + 1 < len(pipe_map):
            if symbol_connections[pipe_map[x + 1][y]].up:
                connected_locations.append((x + 1, y))
        if location_connections.right and y + 1 < len(pipe_map[x]):
            if symbol_connections[pipe_map[x][y + 1]].left:
                connected_locations.append((x, y + 1))
        if location_connections.left and y > 0:
            if symbol_connections[pipe_map[x][y - 1]].right:
                connected_locations.append((x, y - 1))
        print(f"connected to {connected_locations}")
        
        for con_x, con_y in connected_locations:
            if distance_from_start[con_x][con_y] is None or distance_from_start[con_x][con_y] > distance_from_start[x][y] + 1:
                distance_from_start[con_x][con_y] = distance_from_start[x][y] + 1
                next_all_search_locations.add((con_x, con_y))
        
    all_search_locations = next_all_search_locations

print(max([dist for line in distance_from_start for dist in line if dist is not None]))

