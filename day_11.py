import math
import numpy as np

# WIP

raw_galaxy_image = list(filter(bool, """""".split("\n"))) # fill this with input


galaxies_index = [(row_index, column_index) for row_index, line in enumerate(raw_galaxy_image) for column_index, char in enumerate(line) if char == "#"]
if not galaxies_index:
    raise ValueErrors('No galaxies in the image')

galaxy_image = np.full((len(raw_galaxy_image), len(raw_galaxy_image[0])), False, dtype=np.bool_)
for x, y in galaxies_index:
    galaxy_image[x, y] = True

empty_rows = {row_index for row_index in range(galaxy_image.shape[0]) if not galaxy_image[row_index, :].sum()}
empty_cols = {col_index for col_index in range(galaxy_image.shape[1]) if not galaxy_image[:, col_index].sum()}

galaxy_distances = np.full((len(galaxies_index), len(galaxies_index)), np.NaN)

for g_index_1, (x1, y1) in zip(range(len(galaxies_index) - 1), galaxies_index[:-1]):
    for g_index_2, (x2, y2) in zip(range(g_index_1 + 1, len(galaxies_index)), galaxies_index[g_index_1 + 1:]):
        galaxy_distances[g_index_1, g_index_2] = int(
                abs(x2 - x1) + abs(y2 - y1)
                + len(empty_rows.intersection(range(min(x1, x2), max(x1, x2))))  # space distorsion in x
                + len(empty_rows.intersection(range(min(y1, y2), max(y1, y2))))  # space distorsion in y
        )
total_min_dist = 0
for g_index_1 in range(len(galaxies_index)):
    total_min_dist += np.nanmin(np.concatenate((galaxy_distances[g_index_1, :], galaxy_distances[:, g_index_1]), axis=None))
print(total_min_dist)
