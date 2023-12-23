from functools import cache
from typing import List, Tuple, Iterable

PatternDesc = Tuple[Tuple[str, int], ...]
PatternSpec = Tuple[int, ...]

raw_spring_patterns = list(filter(bool, """""".split("\n"))) # fill this with input
part_1 = True


def describe_pattern(springs_pattern: str) -> PatternDesc:
    group_description = []
    while springs_pattern:
        start_char = springs_pattern[0]
        start_group = next(re.finditer(re.escape(start_char) + "+", springs_pattern))
        group_description.append((start_char, start_group.end()))
        springs_pattern = springs_pattern[start_group.end():]
    return tuple(group_description)


def deduce_pattern(spec: PatternSpec, spec_to_remove: PatternSpec) -> PatternSpec:
    if not spec_to_remove:
        return spec
    if spec_to_remove[-1] == spec[len(spec_to_remove) - 1]:
        return spec[len(spec_to_remove):]
    return tuple(chain([spec[len(spec_to_remove) - 1] - spec_to_remove[-1]], spec[len(spec_to_remove):])), 


@cache
def max_spec_part_in_pattern(pattern_part: str, spec: PatternSpec) -> Tuple[PatternSpec, bool]:
    """Find the maximum spec that can be fitted in a given pattern."""
    if not spec:
        return spec
    
    all_broken_pattern_desc = []
    previous_group_char = None
    for group_char, group_size in describe_pattern(pattern_part):
        if group_char == "?":
            group_char = "#"
        if group_char == previous_group_char:
            all_broken_pattern_desc[-1] = (group_char, group_size + result[-1][1])
        else:
            all_broken_pattern_desc.append((group_char, group_size))
            previous_group_char = group_char

    max_broken_spec = tuple(group_size for char, group_size in all_broken_pattern_desc if char == "#")
    spec_iterator = iter(spec)
    max_spec = []
    try:
        current_spec = next(spec_iterator)
        for group_size in max_broken_spec:
            while True:
                if current_spec < group_size:
                    max_spec.append(current_spec)
                    group_size -= current_spec +1
                    current_spec = next(spec_iterator)
                elif current_spec == group_size:
                    max_spec.append(current_spec)
                    current_spec = next(spec_iterator)
                    break
                else:
                    break
    except StopIteration:
        return spec
    return tuple(max_spec)


def spec_range(min_spec: PatternSpec, max_spec: PatternSpec)-> Iterable[PatternSpec]:
    last_comparable_index = max(len(min_spec) - 1, 0)
    max_spec = list(max_spec)
    if (
        len(max_spec) < len(min_spec) 
        or min_spec[:last_comparable_index] != max_spec[:last_comparable_index] 
        or min_spec[last_comparable_index] >= max_spec[last_comparable_index]
    ):
        raise ValueError(f"min spec is not lower than max_spec: ! {min_spec} < {max_spec}")
    for spec_index in range(last_comparable_index, len(max_spec)):
        min_range = 1 if spec_index != last_comparable_index else min_spec[last_comparable_index]
        for last_elem_value in range(min_range, max_spec[spec_index] + 1):
            yield tuple(max_spec[:spec_index] + [last_elem_value])


@cache
def find_compatible_choices(spring_pattern: str, broken_springs_spec: PatternSpec) -> Tuple[str]:
    raw_spring_pattern = spring_pattern
    spring_pattern = spring_pattern.strip(".")
    question_count = spring_pattern.count("?")
    if question_count == 0:
        if tuple(group_size for char, group_size in describe_pattern(spring_pattern) if char == "#") == broken_springs_spec:
            return tuple([raw_spring_pattern])
        else:
            return tuple()
    if not broken_springs_spec:
        if "#" not in spring_pattern:
            return tuple([raw_spring_pattern.replace("?", ".")])
        else:
            return tuple()
    elif len(spring_pattern) <= 1:
        if len(broken_springs_spec) > 1 or broken_springs_spec[0] > 1:
            return tuple()
        if broken_springs_spec and spring_pattern:
            return tuple([raw_spring_pattern.replace("?", "#")])
        if not spring_pattern and not broken_springs_spec:
            return tuple([raw_spring_pattern.replace("?", "."))])
        return tuple([])
    
    middel = int(len(spring_pattern)/2)
    pattern_part_left, pattern_part_right =  spring_pattern[:middel], spring_pattern[middel:]
    
    max_left_pattern = max_max_spec_part_in_pattern(pattern_part_left, broken_springs_spec)
    max_right_pattern_inverted = max_max_spec_part_in_pattern(pattern_part_right[::-1], broken_springs_spec[::-1])
    max_right_pattern = max_right_pattern_inverted[::-1]
    min_left_pattern = deduce_pattern(spec=broken_springs_spec[::-1], spec_to_remove=max_right_pattern_inverted)[::-1]

    number_pattern_left = max(left_pattern[::-1].replace("?", "#").index('.'), 0)
    number_pattern_right = max(pattern_part_right.replace("?", "#").index('.'), 0)

    result = []

    for spec_left in spec_range(min_left_pattern, max_right_pattern):
        spec_right = spec[len(spec_left):]
        if spec_left[-1] != spec[len(spec_left) - 1]:
            if spec_left[-1] > number_pattern_left or spec[len(spec_left) - 1] - spec_left[-1] > number_pattern_right:
                continue
            imposed_left = "#" * spec_left[-1]
            if pattern_part_left[-len(imposed_left):].count('.') != 0:
                continue
            imposed_right = "#" * (spec[len(spec_left) - 1] - spec_left[-1])
            if pattern_part_right[:-len(imposed_right)].count('.') != 0:
                continue
        else:
            imposed_left = ""
            imposed_right = ""
        patterns_left = find_compatible_choices(pattern_part_left[:-len(imposed_left)], spec_left[:(-1 if imposed_left else len(spec_left)])
        patterns_right = find_compatible_choices(pattern_part_left[len(imposed_right):], spec[len(spec_left) + (1 if imposed_right else 0):])
        result.extend([
            raw_spring_pattern[:len(raw_spring_pattern)-len(found_left)] 
            + found_left 
            + imposed_left 
            + imposed_right 
            + found_right 
            + raw_spring_pattern[-len(raw_spring_pattern)+len(found_right):]
            for found_left in patterns_left
            for found_right in patterns_right
        ])
    return tuple(result)

multiplier = 1 if part_1 else 5

total = 0
for pattern, raw_spec in map(lambda s: s.split(), raw_spring_patterns):
    spec = list(map(lambda s: int(s), raw_spec.split(',')))
    pattern = '?'.join([pattern] * multiplier)
    spec *= multiplier
    print(f"Studying {pattern}, {spec}")
    possibilities = len(list(find_patterns(simplify_groups(describe_pattern('?'.join(pattern for i in range(5)))), tuple(spec*5))))
    print(f"Found {possibilities} for pattern {pattern}")
    total += possibilities

# wip
