from dataclasses import dataclass
from itertools import chain, count
from typing import Tuple


raw_instructions = """""" # fill this with input

path, raw_edges = raw_instructions.split('\n\n')
all_edges = {}
for node, raw_out_nodes in map(lambda line: line.split("="), filter(bool, raw_edges.split("\n"))):
    all_edges[node.strip()] = tuple(map(lambda s: s.strip(), raw_out_nodes.strip(" ()").split(",")))

##############
# part 1
current_location = 'AAA'
step_count = 0
while current_location != 'ZZZ':
    new_current_location = all_edges[current_location][0 if path[step_count % len(path)] == 'L' else 1]
    step_count += 1
    current_location = new_current_location
print(f"reached destination after {step_count}")


##############
# part 2
@dataclass(frozen=True)
class CycleData:
    """Contains required information to know the sequence of Z elements"""
    #  →→→→→→→→z→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→z→→→→→→↓
    #  <- starting_sequence_len ->↑ <- cycle length   ->  ↓
    #                             ↑←←←←←←←←←←z←←←←←←←←←←←←←
    #  z_indexes : indexes as they appeared during the first iteration
    starting_sequence_len: int
    cycle_length: int
    z_indexes: Tuple[int, ...]

def make_z_indexes_generators(cycle_data: CycleData):
    starting_z_indexes = [i for i in cycle_data.z_indexes if i < cycle_data.starting_sequence_len]
    infite_z_indexes_generator = ( i + cycle_count * cycle_data.cycle_length for cycle_count in count() for i in cycle_data.z_indexes if i >= cycle_data.starting_sequence_len)
    return iter(chain(starting_z_indexes, infite_z_indexes_generator))
    

starting_locations = [node for node in all_edges.keys() if node.endswith('A')]
location_pattern_length = []
all_node_Z_patterns = []
for node in starting_locations:
    print(f"Studying path starting from {node}")
    path_index = 0
    node_patterns = []
    while (path_index, node) not in node_patterns:
        node_patterns.append((path_index, node))
        node = all_edges[node][0 if path[path_index] == 'L' else 1]
        path_index = (path_index + 1) % len(path)
    starting_sequence_length=node_patterns.index((path_index, node)) # + 1 - 1
    all_node_Z_patterns.append(CycleData(
        starting_sequence_len=starting_sequence_length,
        cycle_length=len(node_patterns)-starting_sequence_length,
        z_indexes=tuple(step_count for step_count, (_, node) in enumerate(node_patterns) if node.endswith('Z')),
    ))
    print(f"Found cycle {all_node_Z_patterns[-1]}")

z_indexes_generator = [make_z_indexes_generators(cycle_data) for cycle_data in all_node_Z_patterns]
z_indexes = [next(generate_z) for generate_z in z_indexes_generator]
powers = set()
while not len(set(z_indexes)) == 1:
    current_max_z_indexes = max(z_indexes)
    for i, z_index in enumerate(z_indexes):
        while z_index < current_max_z_indexes:
            z_index = next(z_indexes_generator[i])
        z_indexes[i] = z_index
    # still not fast enough T_T

print(f"All reached destination ending in Z after {z_indexes[0]}")
