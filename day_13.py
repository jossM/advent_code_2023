import numpy as np


raw_patterns = """"""  # fill this with input
part_1 = True

comparison_diff = 0 if part_1 else 1

total = 0
for pattern in raw_patterns.strip().split("\n\n"):
    print(f"initial pattern:\n{pattern}")
    pattern_line = pattern.split("\n")
    line_count = len(pattern_line)
    line_size = len(pattern_line[0])
    pattern_matrix = np.zeros((line_count, line_size), dtype=bool)
    for i in range(line_count):
        for j in range(line_size):
            if pattern_line[i][j] == "#":
                pattern_matrix[i][j] = True
    
    found_symetry = False
    for i in range(1, line_count):
        reversed_matrix = np.flipud(pattern_matrix[:i, :])
        diff = np.logical_xor(reversed_matrix[:line_count-i, :], pattern_matrix[i:i+reversed_matrix.shape[0], :])
        if diff.sum() == comparison_diff:
            found_symetry = True 
            total += i * 100
            break
    
    if found_symetry:
        continue
    for i in range(1, line_size):
        reversed_matrix = np.fliplr(pattern_matrix[:, :i])
        diff = np.logical_xor(reversed_matrix[:, :line_size - i], pattern_matrix[:, i:i + reversed_matrix.shape[1]])
        if diff.sum() == comparison_diff:
            total += i
            break
print(f"total {total}")
