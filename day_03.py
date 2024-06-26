from collections import defaultdict
from itertools import chain
import re


schema = list(filter(bool, """""".split("\n"))) # fill this with input
part_2 = False

all_symbols = {i: [match.start() for match in re.finditer('[^\d.]', line)] for i, line in enumerate(schema)}
total = 0
star_neighbors = defaultdict(list)
for line_index, line in enumerate(schema):
    line_symbols = sorted(
        list(chain(*[[(line_index + i - 1, symbol_index) for symbol_index in all_symbols.get(line_index + i - 1, [])] for i in range(3)])),
        key=lambda x: x[1]
    )
    if not line_symbols:
        continue
    match_offset = 0
    for line_number in re.finditer('\d+', line):
        neighbor_symbols = []
        for line_symbol_index, col_symbol_index in line_symbols[match_offset:]:
            if col_symbol_index < line_number.start() - 1:
                match_offset += 1
            else:
                if col_symbol_index <= line_number.end():
                    neighbor_symbols.append((line_symbol_index, col_symbol_index))
                elif col_symbol_index > line_number.end():
                    break
        if not neighbor_symbols:
            continue
        if not part_2:
            total += int(line_number.group())
        else:
            for line_symbol_index, col_symbol_index in neighbor_symbols:
                if schema[line_symbol_index][col_symbol_index] != "*":
                    continue
                star_neighbors[(line_symbol_index, col_symbol_index)].append(
                    (line_index, line_number.start(), line_number.end())
                )

if part_2:
    gears = set()
    for star_position, neighbors in star_neighbors.items():
        if len(neighbors) <= 1:
            continue
        if len(neighbors) > 2:
            raise ValueError(f"* at line {star_position[0]}, index {star_position[1]} has more than 2 neighbors :"
                             + "\n".join(schema[n[0]][n[1]:n[2]] + f" at line {n[0]} index {n[1]}" for n in neighbors ))
        gears.add(tuple(sorted(neighbors)))
    link_per_gear = defaultdict(lambda:0)
    for g1, g2 in gears:
        link_per_gear[g1] += 1
        link_per_gear[g2] +=1
    if any(presence_count > 1 for presence_count in link_per_gear.values()):
        raise ValueError("One gear is involved in more than one chain. What computation should be taken then ?")
    for g1, g2 in sorted(gears, key=lambda gg: gg[0]):
        total += int(schema[g1[0]][g1[1]:g1[2]]) * int(schema[g2[0]][g2[1]:g2[2]]) 
print(total)
