from enum import Enum, auto
from typing import Tuple

import numpy as np

PatternSpec = Tuple[int, ...]

raw_spring_patterns = """""".strip()  # fill this with input
part_1 = True


class Direction(Enum):
    north = auto()
    west = auto()
    south = auto()
    east = auto()


def slide(pattern_to_slide: np.matrix, direction: Direction):
    if not any(pattern_to_slide.shape):
        return pattern_to_slide
    if direction in {Direction.north, Direction.south}:
        pattern_to_slide = np.transpose(pattern_to_slide)
    if direction in {Direction.east, Direction.south}:
        pattern_to_slide = np.fliplr(pattern_to_slide)

    slided_input = np.full(pattern_to_slide.shape, '.')
    for i in range(pattern_to_slide.shape[0]):
        last_free_slot = 0
        for j in range(pattern_to_slide.shape[1]):
            char = pattern_to_slide[i, j]
            if char == "#":
                last_free_slot = j + 1
                slided_input[i, j] = '#'
            elif char == "O":
                slided_input[i, last_free_slot] = 'O'
                last_free_slot += 1

    if direction in {Direction.east, Direction.south}:
        slided_input = np.fliplr(slided_input)
    if direction in {Direction.north, Direction.south}:
        slided_input = np.transpose(slided_input)
    return slided_input


slide_orders = [Direction.north] if part_1 else [Direction.north, Direction.west, Direction.south, Direction.east]
target_cycle_count = 1 if part_1 else 1000000000
if __name__ == "__main__":
    spring_patterns = raw_spring_patterns.split('\n')
    pattern = np.full((len(spring_patterns), len(spring_patterns[0])), '.')
    for i, line in enumerate(spring_patterns):
        for j, c in enumerate(line):
            if c != '.':
                pattern[i, j] = c

    pattern_key = tuple(map(tuple, pattern))
    has_loop = False
    cycle_count = 0
    seen_patterns = [pattern_key]
    for cycle_count in range(target_cycle_count):
        for direction in slide_orders:
            pattern = slide(pattern, direction)
        pattern_key = tuple(map(tuple, pattern))
        if pattern_key in seen_patterns:
            print(f"cycle found after {cycle_count} iteration")
            has_loop = True
            break
        seen_patterns.append(pattern_key)

    if has_loop:
        print(f'Operation loops skipping from step {cycle_count}')
        loop_start = seen_patterns.index(pattern_key)
        cycle_size = len(seen_patterns) - loop_start
        final_pattern_key = seen_patterns[loop_start + ((target_cycle_count - loop_start) % cycle_size)]
        pattern = np.full((len(spring_patterns), len(spring_patterns[0])), '.')
        for i, line in enumerate(final_pattern_key):
            for j, c in enumerate(line):
                if c != '.':
                    pattern[i, j] = c
    round_rock_position = np.full(pattern.shape, 0)
    for i in range(pattern.shape[0]):
        for j in range(pattern.shape[1]):
            if pattern[i, j] == 'O':
                round_rock_position[i, j] = 1
    total = 0
    for i in range(pattern.shape[0]):
        total += round_rock_position[i, :].sum() * (pattern.shape[0] - i)
    print(f"Found total of {total}")
