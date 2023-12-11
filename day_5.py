from collections import OrderedDict

raw_almanach = """"" # fill this
part_1 = False

almanach_parts = raw_almanach.split("\n\n")
raw_seeds, raw_mappings = almanach_parts[0], almanach_parts[1:]

seeds = list(map(int, filter(bool, raw_seeds.split(":")[1].split())))
if part_1:
    seeds_ranges = [(s, s) for s in seeds]
else:
    seeds_ranges = [(seeds[2 * i], seeds[2 * i] + seeds[2 * i + 1] - 1) for i in range(int(len(seeds) / 2))]

mappings = OrderedDict()
for raw_map in raw_mappings:
    map_lines = list(filter(bool, raw_map.split("\n")))
    categories = map_lines[0].strip(":")
    categories_range_mapping = []
    for line in map_lines[1:]:
        destination_start, source_start, range_len = tuple(map(int, filter(bool, line.split())))
        categories_range_mapping.append((
            (source_start, source_start + range_len - 1),
            destination_start
        ))
    mappings[categories] = sorted(categories_range_mapping)

mapped_ranges = seeds_ranges
for mapping_name, range_mappings in mappings.items():
    print("-"* 3 + ">" + mapping_name)

    # join ranges if they are consecutives (this should be a function but this is an advent code)
    mapped_ranges = sorted(mapped_ranges)
    minimised_ranges = []
    min_range, max_range = mapped_ranges[0]
    for next_min_range, next_max_range in mapped_ranges[1:]:
        if next_min_range > max_range + 1:
            minimised_ranges.append((min_range, max_range))
            min_range, max_range = next_min_range, next_max_range
        else:
            max_range = max(max_range, next_max_range)
    minimised_ranges.append((min_range, max_range))

    next_mapped_ranges = []
    mapping_index = 0
    while minimised_ranges:
        first_minimised_range = minimised_ranges[0]
        # supposes that mappings do not overlap
        try:
            step, range_map, destination_start = next(
                (i, r, d) for i, (r, d) in enumerate(range_mappings[mapping_index:]) if r[1] >= first_minimised_range[0]
            )
            mapping_index += step
        except StopIteration:
            next_mapped_ranges.extend(minimised_ranges)
            minimised_ranges = []
            break

        map_range = lambda r: tuple(map(lambda x: x - range_map[0] + destination_start, r))

        # this should be split into a function but this is an advent code ;)
        if range_map[0] <= first_minimised_range[0] and range_map[1] < first_minimised_range[1]:  # |xx|xyxy|yy|
            next_mapped_ranges.append(map_range((first_minimised_range[0], range_map[1])))
            minimised_ranges[0] = (range_map[1] + 1, first_minimised_range[1])
        elif range_map[0] <= first_minimised_range[0] and first_minimised_range[1] <= range_map[1]:  # |xx|xyxy|xx|
            next_mapped_ranges.append(map_range(first_minimised_range))
            minimised_ranges.pop(0)
        elif first_minimised_range[0] < range_map[0] <= first_minimised_range[1] \
                and first_minimised_range[1] < range_map[1]:  # |yy|xyxy|xx|
            next_mapped_ranges.extend([
                (first_minimised_range[0], range_map[0]),
                map_range((range_map[0] + 1, first_minimised_range[1]))
            ])
            minimised_ranges.pop(0)
        elif first_minimised_range[0] < range_map[0] and range_map[1] < first_minimised_range[1]:  # |yy|xyxy|yy|
            next_mapped_ranges.extend([
                (first_minimised_range[0], range_map[0]),
                map_range((range_map[0], range_map[1])),
            ])
            minimised_ranges[0] = (range_map[1] + 1, first_minimised_range[1])
        else:  # |yyy| |xxx|
            next_mapped_ranges.append(first_minimised_range)
            minimised_ranges.pop(0)
        
    mapped_ranges = next_mapped_ranges

print(min(r[0] for r in mapped_ranges))

    
