from enum import Enum, auto
from itertools import chain

import numpy as np

part_1 = True


class Direction(Enum):
    right = auto()
    down = auto()
    left = auto()
    up = auto()


if __name__ == '__main__':
    print("Enter/Paste your puzzle input :")  # since there are a lot of \ I found it easier to pass by an input
    raw_layout = []
    while True:
        line = input()
        if not line:
            break
        raw_layout.append(line)
    print(f"Using layout :\n\n" + "\n".join(raw_layout))
  
    layout = np.full((len(raw_layout), len(raw_layout[0])), '.')
    for i in range(layout.shape[0]):
        for j in range(layout.shape[1]):
            if raw_layout[i][j] != '.':
                layout[i, j] = raw_layout[i][j]
    
    max_energised = 0
    for input_tile in chain(
            [(i, -1, Direction.right) for i in range(layout.shape[0])],
            [(-1, i, Direction.down) for i in range(layout.shape[1])],
            [(i, layout.shape[1], Direction.left) for i in range(layout.shape[0])],
            [(layout.shape[0], i, Direction.up) for i in range(layout.shape[1])]):
        energized_tiles = np.zeros(layout.shape, dtype=bool)
        diffusing = [input_tile]
        seen_diffusions = set()
        while diffusing:
            studied_point = diffusing.pop(0)
            i, j, direction = studied_point
            seen_diffusions.add(studied_point)
            if direction == Direction.right:
                seen_chars = layout[i, j+1:]
                try:
                    char_index, diffusing_char = next((ci, c) for ci, c in enumerate(seen_chars) if c not in {'-', '.'})
                    point_location = [i, j+1 + char_index]
                    for ci in range(char_index+1):
                        energized_tiles[i, j+1+ci] = True
                    if diffusing_char == '|':
                        potential_diffusing_points = [tuple(point_location + [d]) for d in [direction.up, direction.down]]
                    elif diffusing_char == '/':
                        potential_diffusing_points = [tuple(point_location + [Direction.up])]
                    else:  # diffusing_char == '\\':
                        potential_diffusing_points = [tuple(point_location + [Direction.down])]
                except StopIteration:
                    potential_diffusing_points = []
                    for k in range(j, layout.shape[1]):
                        energized_tiles[i, k] = True
            elif direction == Direction.down:
                seen_chars = layout[i+1:, j]
                try:
                    char_index, diffusing_char = next((ci, c) for ci, c in enumerate(seen_chars) if c not in {'|', '.'})
                    point_location = [i+1 + char_index, j]
                    for ci in range(char_index+1):
                        energized_tiles[i+1 + ci, j] = True
                    if diffusing_char == '-':
                        potential_diffusing_points = [tuple(point_location + [d]) for d in [direction.left, direction.right]]
                    elif diffusing_char == '/':
                        potential_diffusing_points = [tuple(point_location + [Direction.left])]
                    else:  # diffusing_char == '\\':
                        potential_diffusing_points = [tuple(point_location + [Direction.right])]
                except StopIteration:
                    potential_diffusing_points = []
                    for k in range(i, layout.shape[0]):
                        energized_tiles[k, j] = True
            elif direction == Direction.left:
                seen_chars = layout[i, :j][::-1]
                try:
                    char_index, diffusing_char = next((ci, c) for ci, c in enumerate(seen_chars) if c not in {'-', '.'})
                    point_location = [i, j-1-char_index]
                    for ci in range(char_index+1):
                        energized_tiles[i, j-1-ci] = True
                    if diffusing_char == '|':
                        potential_diffusing_points = [tuple(point_location + [d]) for d in [direction.up, direction.down]]
                    elif diffusing_char == '/':
                        potential_diffusing_points = [tuple(point_location + [Direction.down])]
                    else:  # diffusing_char == '\\':
                        potential_diffusing_points = [tuple(point_location + [Direction.up])]
                except StopIteration:
                    potential_diffusing_points = []
                    for k in range(j):
                        energized_tiles[i, k] = True
            else:  # Direction.up
                seen_chars = layout[:i, j][::-1]
                try:
                    char_index, diffusing_char = next((ci, c) for ci, c in enumerate(seen_chars) if c not in {'|', '.'})
                    point_location = [i-1-char_index, j]
                    for ci in range(char_index + 1):
                        energized_tiles[i-1-ci, j] = True
                    if diffusing_char == '-':
                        potential_diffusing_points = [tuple(point_location + [d]) for d in [direction.left, direction.right]]
                    elif diffusing_char == '/':
                        potential_diffusing_points = [tuple(point_location + [Direction.right])]
                    else:  # diffusing_char == '\\':
                        potential_diffusing_points = [tuple(point_location + [Direction.left])]
                except StopIteration:
                    potential_diffusing_points = []
                    for k in range(i):
                        energized_tiles[k, j] = True
            diffusing.extend(p for p in potential_diffusing_points if p not in seen_diffusions)
        energy = energized_tiles.sum()
        max_energised = max(max_energised, energy)
        if part_1:
            break
        print(f"Found for input {input_tile} energy of {energy}" + (" (max so far)" if energy == max_energised else ""))
    print(f"Found max energy of {max_energised}")
