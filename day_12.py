from typing import List, Tuple, Iterable

raw_spring_patterns = list(filter(bool, """""".split("\n"))) # fill this with input
part_1 = True


def describe_pattern(springs_pattern: str) -> List[Tuple[str, int]]:
    group_description = []
    while springs_pattern:
        start_char = springs_pattern[0]
        start_group = next(re.finditer(re.escape(start_char) + "+", springs_pattern))
        group_description.append((start_char, start_group.end()))
        springs_pattern = springs_pattern[start_group.end():]
    return group_description


def start_pattern_could_match(springs_pattern: List[Tuple[str, int]], broken_springs_spec: List[int]) -> bool:
    next_group_index = None
    broken_spring_pattern = []
    has_unknown_block = False
    
    for group_index, (char, group_size) in enumerate(springs_pattern):
        if char == "#":
            broken_spring_pattern.append(group_size)
            next_group_index = group_index + 1
        if char == "?":
            has_unknown_block = True
            break
    
    if not has_unknown_block:
        return broken_spring_pattern == broken_springs_spec
    
    if next_group_index is None:
        return True

    exact_match_length = len(broken_spring_pattern)
    if springs_pattern[next_group_index][0] == "?":
        exact_match_length -= 1
    
    return (
        broken_spring_pattern[:exact_match_length] == broken_springs_spec[:exact_match_length]
        and len(broken_spring_pattern) <= len(broken_springs_spec)
        and (exact_match_length == len(broken_spring_pattern) or broken_spring_pattern[exact_match_length] <= broken_springs_spec[exact_match_length])
    )


def fuse_same_adjacent_groups(spring_pattern: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    result = []
    previous_group_char = None
    for group_char, group_size in spring_pattern:
        if group_char == previous_group_char:
            result[-1] = (group_char, group_size + result[-1][1])
        elif group_size > 0:
            result.append((group_char, group_size))
            previous_group_char = group_char
    return result


def find_patterns(spring_pattern: List[Tuple[str, int]], broken_springs_spec: List[int]) -> Iterable[str]:
    if not start_pattern_could_match(spring_pattern, broken_springs_spec):
        return
    if not any("?" == char for char, _ in spring_pattern):
        yield ''.join(char * group_size for char, group_size in spring_pattern)
        return
    first_question_group_index, question_group_size = next(
        (group_index, group_size) for group_index, (group_char, group_size) in enumerate(spring_pattern) if group_char == "?")
    if question_group_size > 1:
        remainging_question_group = [('?', question_group_size - 1)]
    else:
        remainging_question_group = []
    
    for group_choice in [("#", 1), (".", 1)]:
        pattern = fuse_same_adjacent_groups(
            spring_pattern[:first_question_group_index]
            + [group_choice]
            + remainging_question_group
            + spring_pattern[first_question_group_index + 1:]
        )
        yield from find_patterns(pattern, broken_springs_spec)

multiplier = 1 if part_1 else 5

total = 0
for pattern, raw_spec in map(lambda s: s.split(), raw_spring_patterns):
    spec = list(map(lambda s: int(s), raw_spec.split(',')))
    pattern = '?'.join([pattern] * multiplier)
    spec *= multiplier
    print(f"Studying {pattern}, {spec}")
    possibilities = len(list(find_patterns(describe_pattern('?'.join(pattern for i in range(5))), spec*5)))
    print(f"Found {possibilities} for pattern {pattern}")
    total += possibilities

        
