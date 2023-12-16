import math

raw_instructions = """""" # fill this with input

path, raw_edges = raw_instructions.split('\n\n')
all_edges = {}
for node, raw_out_nodes in map(lambda line: line.split("="), filter(bool, raw_edges.split("\n"))):
    all_edges[node] = tuple(map(lambda s: s.strip(), raw_out_nodes.strip(" ()").split(",")))

# part 1
current_location = 'AAA'
step_count = 0
while current_location != 'ZZZ':
    new_current_location = all_edges[current_location][0 if path[step_count % len(path)] == 'L' else 1]
    step_count += 1
    current_location = new_current_location
print(step_count)

# part 2
def find_smallest_repeating_pattern(sequence: list) -> list:
    for sub_seq_len in range(1, int(len(sequence)/2)):
        if len(sequence) % sub_seq_len != 0:
            continue
        if sequence[:sub_seq_len] * int(len(sequence)/sub_seq_len) == sequence:
            return sequence[:sub_seq_len]
    return sequence

shortest_path = find_smallest_repeating_pattern(path)

starting_locations = [node for node in all_edges.keys() if node.endswith('A')]
location_pattern_length = []
node_Z_patterns = []

for node in starting_locations:
    continue
    # to be continued
