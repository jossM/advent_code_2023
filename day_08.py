from dataclasses import dataclass
import math
from typing import Tuple, Dict


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
    

# Since there is no end to the process and the number of location & associated point in the path, there has to be cycles
# this may be why this is a desert analogy (because you roam in circles).
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


# This grants us the ability to know which step_count will correspond to a location ending in Z per start point
# step_to_z_location = z_first_seen_position + cycle_length * cycle_count
# Brute forcing the exploration is still not fast enough
# It seems there is a trick in the exercise where z indexes only appear once and at a position which correspond ee
for cycle in all_node_Z_patterns:
    assert len(cycle.z_indexes) == 1
    assert cycle.z_indexes[0] == cycle.cycle_length
    assert cycle.z_indexes[0] > cycle.starting_sequence_len
print("property was checked out for every cycle. Rest of the program should work.")

# now that we know those properties, the question is :
# what is the smallest number of step so that it belongs to all the z_locations series that follow this pattern : 
# step_to_z_location = cycle_length * (cycle_count + 1)
# Simple lcm of cycle length is the answer
macro_cycle = math.lcm(*[cycle.cycle_length for cycle in all_node_Z_patterns]) 
print(f"Final solutions should be {macro_cycle} (power {int(math.log(macro_cycle, 10))})")
# don't know what this could be for just yet
